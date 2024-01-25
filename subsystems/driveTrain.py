from networktables import NetworkTables
import commands2
import swerveModule
import wpilib 
import math
import navx
from wpimath import geometry, kinematics, estimator

class DriveTrainSubsystem(commands2.Subsystem):

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config # inhereting the robot config json from the robot container
        NetworkTables.initialize() # you use networktables to access limelight data
        self.LimelightTable = NetworkTables.getTable('limelight') # giving us access to the limelight's data as a variable

        self.navx = navx.AHRS.create_spi(update_rate_hz=100)

        self.kMaxSpeed = self.config ["RobotDefaultSettings"]["wheelVelocityLimit"]
        self.kmaxAutoSpeed = self.config ["autonomousSettings"]["autoVelLimit"]
        self.wheelBase = self.config["RobotDimensions"]["wheelBase"]
        self.trackWidth = self.config["RobotDimensions"]["trackWidth"]

        self.frontLeft = swerveModule(self.config ["swerveModules"]['frontLeft'], "frontLeft")
        self.frontRight = swerveModule(self.config ["swerveModules"]['frontRight'], 'frontRight')
        self.rearLeft = swerveModule(self.config ["serveModules"]['rearLeft'], 'rearLeft')
        self.rearRight = swerveModule(self.config ["swerveModules"]["rearRight"], "rearRight")

        self.KINEMATICS = kinematics.SwerveDrive2Kinematics( geometry.Translation2d (self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d (self.trackWidth / 2, -self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d (-self.trackWidth / 2, -self.wheelBase /2))
        poseEstimator = estimator.SwerveDrive4PoseEstimator(self.KINEMATICS, 
                                                                self.getNAVXRotation2d(), 
                                                                self.getSwerveModulePositions(), 
                                                                geometry.Pose2d(0, 0, geometry.Rotation2d(math.pi)), 
                                                                self.stateStdDevs,
                                                                self.visionMeasurementStdDevs)

    def joystickDrive (self, joystickX, joystickY, joyStickZ):
        pass
    
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