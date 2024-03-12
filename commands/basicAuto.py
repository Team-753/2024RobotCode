import commands2
from subsystems.driveTrain import DriveTrainSubsystem
import wpilib

class simpleAutoDrive(commands2.Command):
    
    def __init__(self, driveTrainSubsysten: DriveTrainSubsystem):
        super().__init__()
        self.addRequirements(driveTrainSubsysten)
        self.driveTrain = driveTrainSubsysten
        self.timer = wpilib.Timer()
    
    def initialize(self):
        self.timer.start()
        
    def execute(self):
        self.driveTrain.joystickDrive((0.5, 0, 0))

    def isFinished(self) -> bool:
         if self.timer.hasElapsed(1):
            self.timer.stop()
            self.timer.reset()
            return True
    
    def end(self, interrupted: bool):
        self.driveTrain.joystickDrive((0, 0, 0))