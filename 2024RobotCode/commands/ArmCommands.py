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
        self.grabber.speakerShoot()
        
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()  
class emptySlow(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber= kGrabber
    def initialize(self):
        pass
    def execute(self):
        self.grabber.speedUpShoot()
        print("empty slow")
    def end(self, interuppted: bool) -> None:
        self.grabber.idle()
class ampEmpty(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self):
        pass
    def execute(self):
        self.grabber.ampShoot()
        print("Amp empty")
    def end(self, interruppted: bool) -> None:
        self.grabber.idle()

class manualShoot(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self):
        self.grabber.shoot()
    def execute(self):
        pass
    def end(self, interrupted: bool):
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
        self.arm.GoUp()
    def execute(self):
        pass
    def end(self, interuppted: bool) -> None:
        self.arm.stop()
class down(commands2.Command):
    def __init__(self, kArm: ArmSubsystem) -> None:
        super().__init__()
        self.arm = kArm
    def initialize(self):
        self.arm.GoDown()
    def execute(self):
        pass
    def end(self, interuppted: bool) -> None:
        self.arm.stop()

###
    class AutoShootSpeaker(commands2.Command):
        def __init(self, kGrabber: grabberSubsystem) -> None:
            super().__init__()
            self.grabber = kGrabber
            self.timer = wpilib.Timer()
        def initialize(self):
            self.grabber.speedUpShoot
        def execute(self) -> None:
            self.grabber.idle()
        def isFinished(self) -> bool:
            if self.grabber.getReadyToShoot() and self.timer.get()==0: 
                self.timer.start()
            return self.timer.hasElapsed(0.5)
###

            

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
