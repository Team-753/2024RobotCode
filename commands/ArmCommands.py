# imports
import wpilib
import commands2
import wpimath
import math
from wpimath import geometry
from subsystems.driveTrain import DriveTrainSubsystem
from subsystems.arm import ArmSubsystem
from subsystems.grabber import grabberSubsystem

# Does nothing
class ArmSpeaker(commands2.Command):
    def __init__(self):
        super().__init__()
        self.arm = ArmSubsystem
    def execute(self) -> None:
        #self.arm.goToSpeaker(self)
        pass
# intakes a note.
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

# empties a note after rev
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
# revs up arm to shoot
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
# empties the other way.
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
# Intakes slowly
class slowIntake(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
    def initialize(self):
        pass
    def execute(self):
        self.grabber.intakeSlow()
        print("Slow Intake")
    def end(self, interruppted: bool) -> None:
        self.grabber.idle()
#  Manually shoots
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
# Stops grabber
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
# Moves arm up
class ArmDown(commands2.Command):
    def __init__(self, kArm: ArmSubsystem) -> None:
        super().__init__()
        self.arm = kArm
    def initialize(self):
        self.arm.goDown()
    def execute(self):
        pass
    def end(self, interuppted: bool) -> None:
        self.arm.stop()
# Moves arm down
class ArmUp(commands2.Command):
    def __init__(self, kArm: ArmSubsystem) -> None:
        super().__init__()
        self.arm = kArm
    def initialize(self):
        print("Up")
        self.arm.GoUp()
    def execute(self):
        pass
    def end(self, interuppted: bool) -> None:
        self.arm.stop()

#######################################################################
class AutoShootSpeaker(commands2.Command):
    def __init__(self, kGrabber: grabberSubsystem) -> None:
        super().__init__()
        self.grabber = kGrabber
        self.timer = wpilib.Timer()
        
    def initialize(self):
        self.timer.reset()
        self.grabber.speedUpShoot()
        self.timer.start()
    def execute(self) -> None:
        if self.timer.get() >= 2:
            self.grabber.speakerShoot()
            
            
    def isFinished(self) -> bool:
        if self.timer.hasElapsed(6):
            return True
    def end(self, interrupted: bool) -> None:
        self.grabber.idle()
        self.timer.stop()
        

#######################################################################
    
class ArmConfirmUp(commands2.Command):
    def __init__(self, kArm: ArmSubsystem) -> None:
        super().__init__()
        self.arm = kArm
    def initialize(self) -> None:
        self.arm.GoUp()
    def isFinished(self) -> bool:
        return self.arm.GetTopLimit()
    def end(self, interuppted: bool) -> None:
        self.arm.stop()
#######################################################################
class ResetOrientation(commands2.Command):
    def __init__(self, kDriveTrain:DriveTrainSubsystem) -> None: 
        super().__init__()
        self.DriveTrain = kDriveTrain
    def initialize(self) -> None:
        self.DriveTrain.resetPose(geometry.Pose2d(0,0,geometry.Rotation2d(math.pi)))
    def isFinished(self) -> bool:
        return True
    def end(self, interuppte: bool)-> None:
        pass


#######################################################################

            

"""
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
        self.arm.amp()   
"""
