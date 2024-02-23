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
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self) -> None:
        pass
    def execute(self) -> None:
        self.grabber.intake()
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()
class emptyFast(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self) -> None:
        pass
    def execute(self) -> None:
        self.grabber.outtakeFast()
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()    
class emptySlow(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self) -> None:
        pass
    def execute(self) -> None:
        self.grabber.outtakeSlow()
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()    
class armEvents(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def home(self) -> None:
        self.arm.home()
        print("arm home")
    def speaker(self) -> None:
        self.arm.speaker()
        print("arm speaker")
    def source(self) -> None:
        self.arm.source()
        print("arm source")
    def amp(self) -> None:
        self.arm.amp()
        print('arm amp')
        
