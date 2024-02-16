import wpilib
import commands2
from subsystems.arm import ArmSubsystem
class ArmSpeaker(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def execute(self) -> None:
        #self.arm.goToSpeaker(self)
        pass

# I still do not support this arm control approach. ~ Joe
class armEvents(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def home(self) -> None:
        self.arm.home(self)
    def speaker(self) -> None:
        self.arm.speaker(self)
    def source(self) -> None:
        self.arm.source(self)
    def amp(self) -> None:
        self.arm.amp(self)
        