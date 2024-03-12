#from networktables import NetworkTables
import commands2
from commands2 import button
from subsystems.swerveModule import SwerveModule
import RobotConfig
import wpilib 
import math
import navx
from wpimath import geometry, kinematics, estimator, controller
import wpimath
import wpiutil
from rev import _rev

from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import HolonomicPathFollowerConfig, ReplanningConfig, PIDConstants
from wpilib import DriverStation

class DriveTrainSubsystem(commands2.Subsystem):

    stateStdDevs = 0.1, 0.1, 0.1
    visionMeasurementStdDevs = 0.9, 0.9, 0.9 * float(math.pi)
    def __init__(self, joystick: button.CommandJoystick) -> None:
        super().__init__()
        
        self.joystick = joystick
        '''NetworkTables.initialize() # you use networktables to access limelight data
        self.LimelightTable = NetworkTables.getTable('limelight')''' # giving us access to the limelight's data as a variable

        self.navx = navx.AHRS.create_spi(update_rate_hz=60)

        self.kMaxSpeed = RobotConfig.DriveConstants.RobotSpeeds.maxSpeed
        self.kMaxAngularVelocity = RobotConfig.DriveConstants.RobotSpeeds.maxSpeed / math.hypot(RobotConfig.RobotDimensions.trackWidth / 2, RobotConfig.RobotDimensions.wheelBase / 2)
        self.wheelBase = RobotConfig.RobotDimensions.wheelBase
        self.trackWidth = RobotConfig.RobotDimensions.trackWidth

        self.frontLeft = SwerveModule(RobotConfig.SwerveModules.frontLeft.driveMotorID, RobotConfig.SwerveModules.frontLeft.turnMotorID)
        self.frontRight = SwerveModule(RobotConfig.SwerveModules.frontRight.driveMotorID, RobotConfig.SwerveModules.frontRight.turnMotorID)
        self.rearLeft = SwerveModule(RobotConfig.SwerveModules.rearLeft.driveMotorID, RobotConfig.SwerveModules.rearLeft.turnMotorID)
        self.rearRight = SwerveModule(RobotConfig.SwerveModules.rearRight.driveMotorID, RobotConfig.SwerveModules.rearRight.turnMotorID)

        teleopConstants = RobotConfig.DriveConstants.PoseConstants
        
        rotationConstants = RobotConfig.DriveConstants.thetaPIDConstants.translationPIDConstants
        self.rotationPID = controller.PIDController(rotationConstants.kP, rotationConstants.kI, rotationConstants.kD, rotationConstants.period)
        self.rotationPID.enableContinuousInput(-math.pi, math.pi)

        self.poseTolerance = geometry.Pose2d(geometry.Translation2d(x=teleopConstants.xPoseToleranceMeters, y=teleopConstants.yPoseToleranceMeters), geometry.Rotation2d(teleopConstants.thetaPoseToleranceRadians))
        self.alliance = wpilib.DriverStation.Alliance.kBlue

        #self.KINEMATICS2 = kinematics._kinematics.SwerveDrive4KinematicsBase(geometry.Translation2d(self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d(self.trackWidth / 2, -self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, -self.wheelBase / 2))
        self.KINEMATICS = kinematics.SwerveDrive4Kinematics(geometry.Translation2d(float(self.trackWidth / 2), float(self.wheelBase / 2)), geometry.Translation2d(float(self.trackWidth / 2), float(-self.wheelBase / 2)), geometry.Translation2d(float(-self.trackWidth / 2), float(self.wheelBase / 2)), geometry.Translation2d(float(-self.trackWidth / 2), float(-self.wheelBase / 2)))
        self.poseEstimator = estimator.SwerveDrive4PoseEstimator(kinematics._kinematics.SwerveDrive4Kinematics(geometry.Translation2d(self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d(self.trackWidth / 2, -self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, -self.wheelBase / 2)), 
                                                                self.getNAVXRotation2d(), 
                                                                self.getSwerveModulePositions(), 
                                                                geometry.Pose2d(0, 0, geometry.Rotation2d(math.pi)), 
                                                                self.stateStdDevs,
                                                                self.visionMeasurementStdDevs)
        
        # i just stole this from here verbatum: https://pathplanner.dev/pplib-build-an-auto.html#configure-autobuilder
        
        AutoBuilder.configureHolonomic(
            self.getPose, # Robot pose supplier
            self.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.getRobotRelativeChassisSpeeds, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            self.autoDrive, # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds
            HolonomicPathFollowerConfig( # HolonomicPathFollowerConfig, this should likely live in your Constants class
                PIDConstants(5.0, 0.0, 0.0), # Translation PID constants
                PIDConstants(5.0, 0.0, 0.0), # Rotation PID constants
                self.kMaxSpeed, # Max module speed, in m/s
                math.sqrt(self.trackWidth**2 + self.wheelBase**2), # Drive base radius in meters. Distance from robot center to furthest module.
                ReplanningConfig() # Default path replanning config. See the API for the options here
            ),
            self.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self # Reference to this subsystem to set requirements
        )
    
    def getNAVXRotation2d(self):
        return self.navx.getRotation2d()
    
    def getPose(self):
        return self.poseEstimator.getEstimatedPosition()
    
    def resetPose(self, poseToset: geometry.Pose2d) -> None:
        self.poseEstimator.resetPosition(self.getNAVXRotation2d(), self.getSwerveModulePositions(), poseToset)
    
    def shouldFlipPath(self):
        # Boolean supplier that controls when the path will be mirrored for the red alliance
        # This will flip the path being followed to the red side of the field.
        # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed
    
    
    def getJoystickInput(self) -> tuple[float]:
        """ Returns all 3 axes on a scale from -1 to 1, if the robot driving 
        is inverted, make all these values positive instead of negative. """
        constants = RobotConfig.DriveConstants.Joystick
        return (
            -wpimath.applyDeadband(self.joystick.getY(), constants.yDeadband),
            -wpimath.applyDeadband(self.joystick.getX(), constants.xDeadband),
            -wpimath.applyDeadband(self.joystick.getZ(), constants.thetaDeadband)
        )
    
    def autoDrive(self, chassisSpeeds: kinematics.ChassisSpeeds):
        swerveModuleStates = self.KINEMATICS.toSwerveModuleStates(chassisSpeeds)
        self.frontLeft.setState(swerveModuleStates[0])
        self.frontRight.setState(swerveModuleStates[1])
        self.rearLeft.setState(swerveModuleStates[2])
        self.rearRight.setState(swerveModuleStates[3])

    def joystickDrive(self, inputs: tuple[float]) -> None:
        xSpeed, ySpeed, zSpeed = (inputs[0] * self.kMaxSpeed, 
                                  inputs[1] * self.kMaxSpeed, 
                                  inputs[2] * self.kMaxAngularVelocity * RobotConfig.DriveConstants.RobotSpeeds.manualRotationSpeedFactor)
        self.setSwerveStates(xSpeed, ySpeed, zSpeed, self.poseEstimator.getEstimatedPosition())
            
    #this was used for the auto place last yeaer, I think, so we might not use this, but it could be good for an auto score function
    def joystickDriveThetaOverride (self, inputs: list, currentPose: geometry.Pose2d, rotationOverride: geometry.Rotation2d, inverted = False):
        rotationOverridePose = geometry.Pose2d(geometry.Translation2d(), rotationOverride)
        yScalar, xScalar = inputs[0], inputs[1]
        poseError = currentPose.relativeTo(rotationOverridePose) # how far we are from where the axes setpoints were before
        xSpeed = xScalar
        ySpeed = yScalar
        if inverted:
            ySpeed = -ySpeed
            xSpeed = -xSpeed
        angularVelocityFF = poseError.rotation().radians() / math.pi  #* self.maxAngularVelocity
        if (abs(poseError.rotation().radians()) > self.poseTolerance.rotation().radians()):
            zSpeed = self.rotationPID.calculate(currentPose.rotation().radians(), rotationOverride.radians()) # this is a speed, not a scalar
        else:
            zSpeed = 0
        if xSpeed == 0 and ySpeed == 0 and zSpeed == 0:
            self.stationary()
        else:
            self.setSwerveStates(xSpeed, ySpeed, angularVelocityFF + zSpeed, False)

    def setSwerveStates(self, xSpeed: float, ySpeed: float, zSpeed: float, fieldOrient = True):
        if fieldOrient:
            swerveModuleStates = self.KINEMATICS.toSwerveModuleStates(kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(kinematics.ChassisSpeeds(xSpeed, ySpeed, zSpeed), self.poseEstimator.getEstimatedPosition().rotation()))
        else:
            swerveModuleStates = self.KINEMATICS.toSwerveModuleStates(kinematics.ChassisSpeeds(xSpeed, ySpeed, zSpeed))
        
        #self.KINEMATICS.desaturateWheelSpeeds(swerveModuleStates, self.kMaxSpeed)
        self.frontLeft.setState(swerveModuleStates[0])
        self.frontRight.setState(swerveModuleStates[1])
        self.rearLeft.setState(swerveModuleStates[2])
        self.rearRight.setState(swerveModuleStates[3])

    def stationary(self):
         #better to not use this as it is unhealthy for the motors and the drivetrain
        self.frontLeft.setNeutralMode(_rev.CANSparkBase.IdleMode.kBrake)
        self.frontLeft.stop()
        self.frontRight.setNeutralMode(_rev.CANSparkBase.IdleMode.kBrake)
        self.frontRight.stop()
        self.rearLeft.setNeutralMode(_rev.CANSparkBase.IdleMode.kBrake)
        self.rearLeft.stop()
        self.rearRight.setNeutralMode(_rev.CANSparkBase.IdleMode.kBrake)
        self.rearRight.stop()
    
    def coast (self):
         self.frontLeft.setNeutralMode(_rev.CANSparkBase.IdleMode.kCoast)
         self.frontLeft.stop()
         self.frontRight.setNeutralMode(_rev.CANSparkBase.IdleMode.kCoast)
         self.frontRight.stop()
         self.rearLeft.setNeutralMode(_rev.CANSparkBase.IdleMode.kCoast)
         self.rearLeft.stop()
         self.rearRight.setNeutralMode(_rev.CANSparkBase.IdleMode.kCoast)
         self.rearRight.stop()

    def getSwerveModulePositions (self):
        return self.frontLeft.getPosition(), self.frontRight.getPosition(), self.rearLeft.getPosition(), self.rearRight.getPosition()
    
    def getRobotRelativeChassisSpeeds(self):
        states = (self.frontLeft.getState(), self.frontRight.getState(), self.rearLeft.getState(), self.rearRight.getState())
        return self.KINEMATICS.toChassisSpeeds(states)
    
    def getCurrentPose(self):
        return self.poseEstimator.getEstimatedPosition()

    def periodic(self) -> None:
        '''if self.LimelightTable.getNumber('getpipe', 0) == 0: # 0 being our apriltag pipeline
            if self.LimelightTable.getNumber('tv', 0) == 1: # are there any valid targets
                if self.alliance == wpilib.DriverStation.Alliance.kBlue:
                    botPoseData = self.LimelightTable.getNumberArray('botpose_wpiblue', [0,0,0,0,0,0,0])
                else:
                    botPoseData = self.LimelightTable.getNumberArray('botpose_wpired', [0,0,0,0,0,0,0])
                botPose2D = geometry.Pose2d(geometry.Translation2d(botPoseData[0], botPoseData[1]), geometry.Rotation2d(botPoseData[5]))
                latency = botPoseData[6]
                self.poseEstimator.addVisionMeasurement(botPose2D, latency)'''
        self.poseEstimator.update(
            self.getNAVXRotation2d(),
            self.getSwerveModulePositions())