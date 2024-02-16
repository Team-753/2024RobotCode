import commands2
from subsystems.grabber import GrabberSubsystem
from RobotConfig import GrabberConfig

class Intake(commands2.Command):
    def __init__(self, kGrabberSubsystem: GrabberSubsystem) -> None:
        super().__init__()
        self.addRequirements(kGrabberSubsystem)
        self.grabber = kGrabberSubsystem
    def initialize(self) -> None:
        self.grabber.setSpeed(GrabberConfig.intake)
    def end(self, interuppted: bool) -> None:
        self.grabber.setSpeed(GrabberConfig.idle)

class SlowEject(commands2.Command):
    def __init__(self, kGrabberSubsystem: GrabberSubsystem) -> None:
        super().__init__()
        self.addRequirements(kGrabberSubsystem)
        self.grabber = kGrabberSubsystem
    def initialize(self) -> None:
        self.grabber.setSpeed(GrabberConfig.outtake)
    def end(self, interuppted: bool) -> None:
        self.grabber.setSpeed(GrabberConfig.idle)

# Brendan TODO: Make another command here for a fast "eject" like when we are shooting up into the speaker. ~ Joe
