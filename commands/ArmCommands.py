import wpilib
import commands2
from subsystems.arm import ArmSubsystem
from subsystems.grabber import grabberSubsystem
class ArmSpeaker(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def execute(self) -> None:
        self.arm.goToSpeaker(self)
class grabberEvents(commands2.Command):
    def __init__(self):
        super().__init__()
        self.grabber = grabberSubsystem    
    def grab(self) -> None:
        self.grabber.intake(self)
    def empty(self) -> None:
        self.grabber.outtake(self)
    def idle(self) -> None:
        self.grabber.idle(self)
    
        