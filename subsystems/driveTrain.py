import commands2

class DriveTrainSubsystem(commands2.Subsystem):
    
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config # inhereting the robot config json from the robot container
        
    def periodic(self) -> None:
        if self.llTable.getNumber('getpipe', 0) == 0: # 0 being our apriltag pipeline
            if self.llTable.getNumber('tv', 0) == 1: # are there any valid targets
                if self.alliance == wpilib.DriverStation.Alliance.kBlue:
                    botPoseData = self.llTable.getNumberArray('botpose_wpiblue', [0,0,0,0,0,0,0])
                else:
                    botPoseData = self.llTable.getNumberArray('botpose_wpired', [0,0,0,0,0,0,0])
                botPose2D = geometry.Pose2d(geometry.Translation2d(botPoseData[0], botPoseData[1]), geometry.Rotation2d(botPoseData[5]))
                latency = botPoseData[6]
                self.poseEstimator.addVisionMeasurement(botPose2D, latency)
        self.poseEstimator.update(
            self.getNAVXRotation2d(),
            self.getSwerveModulePositions())