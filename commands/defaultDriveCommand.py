import commands2
from subsystems.driveTrain import DriveTrainSubsystem
from wpimath import geometry

class DefaultDriveCommand(commands2.Command):
    
    def __init__(self, driveTrainSubsysten: DriveTrainSubsystem):
        super().__init__()
        self.addRequirements(driveTrainSubsysten)
        self.driveTrain = driveTrainSubsysten
    
    
    def execute(self):
        self.driveTrain.joystickDrive(self.driveTrain.getJoystickInput())

class ResetNavx(commands2.Command):
    def __init__(self, driveTrainSubsystem: DriveTrainSubsystem):
        super().__init__()
        self.addRequirements(driveTrainSubsystem)
        self.driveTrain = driveTrainSubsystem
    
    def initialize(self):
        self.driveTrain.resetPose(geometry.Pose2d())
        
    def isFinished(self) -> bool:
        return True