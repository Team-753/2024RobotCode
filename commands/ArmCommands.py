import wpilib
import commands2
from subsystems.arm import ArmSubsystem
class ArmSpeaker(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def execute(self) -> None:
        self.arm.goToSpeaker(self)
        