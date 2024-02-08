import commands2
from subsystems.driveTrain import DriveTrainSubsystem

class DefaultDriveCommand(commands2.Command):
    
    def __init__(self, driveTrainSubsysten: DriveTrainSubsystem):
        super().__init__()
        self.addRequirements(driveTrainSubsysten)
        self.driveTrain = driveTrainSubsysten
    
    
    def execute(self):
        self.driveTrain.joystickDrive(self.driveTrain.getJoystickInput())
    