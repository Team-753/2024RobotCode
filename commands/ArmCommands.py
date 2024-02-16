import wpilib
import commands2
from subsystems.arm import ArmSubsystem
from subsystems.grabber import grabberSubsystem
class ArmSpeaker(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def execute(self) -> None:
        #self.arm.goToSpeaker(self)
        pass
class grab(commands2.Command):
    def __init__(self, GrabberSubsystem: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = GrabberSubsystem
    def initialize(self) -> None:
        pass
    def execute(self) -> None:
        self.grabber.intake(self)
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()
class empty(commands2.Command):
    def __init__(self, GrabberSubsystem: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = grabberSubsystem
    def initialize(self) -> None:
        pass
    def execute(self) -> None:
        self.grabber.outtake(self)
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()    
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
        