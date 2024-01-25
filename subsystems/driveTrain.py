
import os
import json
from networktables import NetworkTables
import commands2

class RobotContainer:
    """ Basically does everything. Yeah... """

    NetworkTables.initialize() # you use networktables to access limelight data

    def __init__(self) -> None:
        # importing our JSON settings and converting it to global python dictionary.
        folderPath = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(folderPath, 'config.json')
        with open (filePath, "r") as f1:
            self.config = json.load(f1)
        self.LimelightTable = NetworkTables.getTable('limelight') # giving us access to the limelight's data as a variable


    def configureButtonBindings(self):
        """ Sets up the button command bindings for the controllers. """
 13 changes: 7 additions & 6 deletions13  
subsystems/driveTrain.py
@@ -1,28 +1,29 @@
import commands2
from wpimath import estimator, geometry
from networktables import NetworkTables

class DriveTrainSubsystem(commands2.Subsystem):
    stateStdDevs = 0.1, 0.1, 0.1
    visionMeasurementStdDevs = 0.9, 0.9, 0.9 * math.pi


    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config # inhereting the robot config json from the robot container
        NetworkTables.initialize() # you use networktables to access limelight data
        poseEstimator = estimator.SwerveDrive4PoseEstimator(self.KINEMATICS, 
                                                                self.getNAVXRotation2d(), 
                                                                self.getSwerveModulePositions(), 
                                                                geometry.Pose2d(0, 0, geometry.Rotation2d(math.pi)), 
                                                                self.stateStdDevs,
                                                                self.visionMeasurementStdDevs)

        self.LimelightTable = NetworkTables.getTable('limelight') # giving us access to the limelight's data as a variable
    def periodic(self) -> None:
        if self.llTable.getNumber('getpipe', 0) == 0: # 0 being our apriltag pipeline
            if self.llTable.getNumber('tv', 0) == 1: # are there any valid targets
        if self.LimelightTable.getNumber('getpipe', 0) == 0: # 0 being our apriltag pipeline
            if self.LimelightTable.getNumber('tv', 0) == 1: # are there any valid targets
                if self.alliance == wpilib.DriverStation.Alliance.kBlue:
                    botPoseData = self.llTable.getNumberArray('botpose_wpiblue', [0,0,0,0,0,0,0])
                    botPoseData = self.LimelightTable.getNumberArray('botpose_wpiblue', [0,0,0,0,0,0,0])
                else:
                    botPoseData = self.llTable.getNumberArray('botpose_wpired', [0,0,0,0,0,0,0])
                    botPoseData = self.LimelightTable.getNumberArray('botpose_wpired', [0,0,0,0,0,0,0])
                botPose2D = geometry.Pose2d(geometry.Translation2d(botPoseData[0], botPoseData[1]), geometry.Rotation2d(botPoseData[5]))
                latency = botPoseData[6]
                self.poseEstimator.addVisionMeasurement(botPose2D, latency)