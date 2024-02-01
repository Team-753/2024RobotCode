from networktables import NetworkTables
import commands2
from commands2 import button
from subsystems.swerveModule import SwerveModule
import wpilib 
import math
import navx
from wpimath import geometry, kinematics, estimator, controller
import wpimath
import wpiutil
import rev

class DriveTrainSubsystem(commands2.Subsystem):

    stateStdDevs = 0.1, 0.1, 0.1
    visionMeasurementStdDevs = 0.9, 0.9, 0.9 * math.pi
    def __init__(self, config: dict, joystick: button.CommandJoystick) -> None:
        super().__init__()
        
        self.config = config # inhereting the robot config json from the robot container
        self.joystick = joystick
        NetworkTables.initialize() # you use networktables to access limelight data
        self.LimelightTable = NetworkTables.getTable('limelight') # giving us access to the limelight's data as a variable

        self.navx = navx.AHRS.create_spi(update_rate_hz=100)

        self.kMaxSpeed = self.config["DriveConstants"]["maxSpeed"]
        self.kMaxAngularVelocity = self.config["DriveConstants"]["maxSpeed"] / math.hypot(self.config["RobotDimensions"]["trackWidth"] / 2, self.config["RobotDimensions"]["wheelBase"] / 2)
        self.wheelBase = self.config["RobotDimensions"]["wheelBase"]
        self.trackWidth = self.config["RobotDimensions"]["trackWidth"]

        self.frontLeft = SwerveModule(self.config ["swerveModules"]['frontLeft'], "frontLeft")
        self.frontRight = SwerveModule(self.config ["swerveModules"]['frontRight'], 'frontRight')
        self.rearLeft = SwerveModule(self.config ["serveModules"]['rearLeft'], 'rearLeft')
        self.rearRight = SwerveModule(self.config ["swerveModules"]["rearRight"], "rearRight")

        teleopConstants = self.config["driverStation"]["teleoperatedRobotConstants"]

        
        rotationConstants = self.config["autonomousSettings"]["rotationPIDConstants"]
        self.rotationPID = controller.PIDController(rotationConstants["kP"], rotationConstants["kI"], rotationConstants["kD"], rotationConstants["period"])
        self.rotationPID.enableContinuousInput(-math.pi, math.pi)

        self.poseTolerance = geometry.Pose2d(geometry.Translation2d(x=teleopConstants["xPoseToleranceMeters"], y=teleopConstants["yPoseToleranceMeters"]), geometry.Rotation2d(teleopConstants["thetaPoseToleranceRadians"]))
        self.alliance = wpilib.DriverStation.Alliance.kBlue

        self.KINEMATICS = kinematics.SwerveDrive4Kinematics(geometry.Translation2d(self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d(self.trackWidth / 2, -self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, -self.wheelBase / 2))
        self.poseEstimator = estimator.SwerveDrive4PoseEstimator(self.KINEMATICS, 
                                                                self.getNAVXRotation2d(), 
                                                                self.getSwerveModulePositions(), 
                                                                geometry.Pose2d(0, 0, geometry.Rotation2d(math.pi)), 
                                                                self.stateStdDevs,
                                                                self.visionMeasurementStdDevs)
    
    def getNAVXRotation2d(self):
        return self.navx.getRotation2d
    
    def getJoystickInput(self) -> tuple[float]:
        """ Returns all 3 axes on a scale from -1 to 1, if the robot driving 
        is inverted, make all these values positive instead of negative. """
        constants = self.config["DriveConstants"]["Joystick"]
        return (
            -wpimath.applyDeadband(self.joystick.getX(), constants["xDeadband"]),
            -wpimath.applyDeadband(self.joystick.getY(), constants["yDeadband"]),
            -wpimath.applyDeadband(self.joystick.getZ(), constants["thetaDeadband"])
        )
    
    def autoDrive(self, chassisSpeeds: kinematics.ChassisSpeeds, currentPose: geometry.Pose2d, fieldRelative = True):
        if chassisSpeeds == kinematics.ChassisSpeeds(0, 0, 0):
            self.stationary()
        else:
            #chassisSpeeds.omega = -chassisSpeeds.omega (this inverts it, we might not need to use it)
            if fieldRelative:
                swerveModuleStates = self.KINEMATICS.toSwerveModuleStates(kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(chassisSpeeds.vx, chassisSpeeds.vy, chassisSpeeds.omega, currentPose.rotation())) #might need to invert vx
            else:
                swerveModuleStates = self.KINEMATICS.toSwerveModuleStates(chassisSpeeds)

            self.KINEMATICS.desaturateWheelSpeeds(swerveModuleStates, self.kmaxAutoSpeed)
            self.frontLeft(swerveModuleStates[0])
            self.frontRight(swerveModuleStates[1])
            self.rearLeft(swerveModuleStates[2])
            self.rearRight(swerveModuleStates[3])

    def joystickDrive(self, inputs: tuple[float]) -> None:
        xSpeed, ySpeed, zSpeed = (inputs[0] * self.kMaxSpeed, 
                                  inputs[1] * self.kMaxSpeed, 
                                  inputs[2] * self.kMaxAngularVelocity * self.config["DriveConstants"]["RobotSpeeds"]["manualRotationSpeedFactor"])
        self.setSwerveStates(xSpeed, ySpeed, zSpeed)
            
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
            self.setSwerveStates(xSpeed, ySpeed, angularVelocityFF + zSpeed, currentPose, False)

    def setSwerveStates(self, xSpeed: float, ySpeed: float, zSpeed: float, fieldOrient = True):
        if fieldOrient:
            swerveModuleStates = self.KINEMATICS.toSwerveModuleStates(kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(kinematics.ChassisSpeeds(xSpeed, ySpeed, zSpeed), self.getCurrentPose().rotation()))
        else:
            swerveModuleStates = self.KINEMATICS.toSwerveModuleStates(kinematics.ChassisSpeeds(xSpeed, ySpeed, zSpeed))
        
        self.KINEMATICS.desaturateWheelSpeeds(swerveModuleStates, self.kMaxSpeed)
        self.frontLeft.setState(swerveModuleStates[0])
        self.frontRight.setState(swerveModuleStates[1])
        self.rearLeft.setState(swerveModuleStates[2])
        self.rearRight.setState(swerveModuleStates[3])

    """    def stationary(self):
        #better to not use this as it is unhealthy for the motors and the drivetrain
        self.frontLeft.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kBrake)
        self.frontLeft.stop
        self.frontRight.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kBrake)
        self.frontRight.stop
        self.rearLeft.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kBrake)
        self.rearLeft.stop
        self.rearRight.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kBrake)
        self.rearRight.stop
    
    def coast (self):
        self.frontLeft.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kCoast)
        self.frontLeft.stop
        self.frontRight.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kCoast)
        self.frontRight.stop
        self.rearLeft.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kCoast)
        self.rearLeft.stop
        self.rearRight.setNeutralMode(rev._rev.CANSparkBase.IdleMode.kCoast)
        self.rearRight.stop"""

    def getSwerveModulePositions (self):
        return self.frontLeft.getPosition(), self.frontRight.getPosition(), self.rearLeft.getPosition(), self.rearRight.getPosition()
    
    def actualChassisSpeeds(self):
        states = (self.frontLeft.getSwerveModuleState(), self.frontRight.getSwerveModuleState(), self.rearLeft.getSwerveModuleState(), self.rearRight.getSwerveModuleState())
        return self.KINEMATICS.toChassisSpeeds(states[0], states[1], states[2], states[3])
    
    def getCurrentPose(self):
        return self.poseEstimator.getEstimatedPosition()

    def periodic(self) -> None:
        if self.LimelightTable.getNumber('getpipe', 0) == 0: # 0 being our apriltag pipeline
            if self.LimelightTable.getNumber('tv', 0) == 1: # are there any valid targets
                if self.alliance == wpilib.DriverStation.Alliance.kBlue:
                    botPoseData = self.LimelightTable.getNumberArray('botpose_wpiblue', [0,0,0,0,0,0,0])
                else:
                    botPoseData = self.LimelightTable.getNumberArray('botpose_wpired', [0,0,0,0,0,0,0])
                botPose2D = geometry.Pose2d(geometry.Translation2d(botPoseData[0], botPoseData[1]), geometry.Rotation2d(botPoseData[5]))
                latency = botPoseData[6]
                self.poseEstimator.addVisionMeasurement(botPose2D, latency)
        self.poseEstimator.update(
            self.getNAVXRotation2d(),
            self.getSwerveModulePositions())