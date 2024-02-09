import commands2
from subsystems.driveTrain import DriveTrainSubsystem
from subsystems.arm import ArmSubsystem
import RobotConfig
from wpimath import geometry

class TurnToCommand(commands2.Command):
    """ Takes control of the rotation of the robot and aims it directly at the speaker whilst also raising the shooter. """
    
    def __init__(self, kDriveTrain: DriveTrainSubsystem, kArm: ArmSubsystem):
        super().__init__()
        self.addRequirements(kDriveTrain, kArm)
        self.driveTrain = kDriveTrain
        self.arm = kArm
        self.joystick = kDriveTrain.joystick
        
    def initialize(self):
        return super().initialize()
    
    def execute(self):
        return super().execute()
    
    def end(self, interrupted: bool):
        return super().end(interrupted)
    
    def isFinished(self) -> bool:
        return super().isFinished()