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
        print("intaking")
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()
class empty(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self) -> None:
        pass
    def execute(self) -> None:
        print("empty")
        self.grabber.outtakeFast()
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()  
class emptySlow(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber= kGrabber
    def initialize(self):
        pass
    def execute(self):
        self.grabber.outtakeSlow()
        print("empty slow")
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()
class stop(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self):
        pass
    def execute(self):
        self.grabber.idle()
    def end(self):
        pass
class up(commands2.Command):
    def __init__(self, kArm: ArmSubsystem) -> None:
        super().__init__()
        self.arm = kArm
    def initialize(self):
        pass
    def execute(self):
        self.arm.onA()
    def end(self, interuppted: bool) -> None:
        self.arm.stop()
'''
class armEvents(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def home(self) -> None:
        self.arm.home()
    def speaker(self) -> None:
        self.arm.speaker()
    def source(self) -> None:
        self.arm.source()
    def amp(self) -> None:
        self.arm.amp()'''      