
import commands2
from subsystems.climber import ClimberSubsystem
import wpilib

class climberGoesUp(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem
        self.timer = wpilib.Timer()
        
    def initialize(self):
        self.climber.preGoUp()
        self.timer.start()


    def execute(self):
        if  self.timer.hasElapsed(0.2):
            self.climber.goUp()
            self.timer.stop()
            self.timer.reset()

        print ("going up")

    def end(self, interrupted: bool):
        self.climber.stationary()

class rightClimberGoesUp(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem
        self.timer = wpilib.Timer()
        
    def initialize(self):
        self.climber.rightPreGoUp()
        self.timer.start()


    def execute(self):
        if  self.timer.hasElapsed(0.2):
            self.climber.rightGoUp()
            self.timer.stop()
            self.timer.reset()

        print ("right going up")

    def end(self, interrupted: bool):
        self.climber.stationary()

class leftClimberGoesUp(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem
        self.timer = wpilib.Timer()
        
    def initialize(self):
        self.climber.leftPreGoUp()
        self.timer.start()


    def execute(self):
        if  self.timer.hasElapsed(0.2):
            self.climber.leftGoUp()
            self.timer.stop()
            self.timer.reset()

        print ("left going up")

    def end(self, interrupted: bool):
        self.climber.stationary()
      
    
class climberGoesDown(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem

    def initialize(self):
        self.climber.goDown()

    def execute(self):
        print("going down")

    def end(self, interrupted: bool):
        self.climber.stationary()
    
class rightClimberGoesDown(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem

    def initialize(self):
        self.climber.rightGoDown()

    def execute(self):
        print("right going down")

    def end(self, interrupted: bool):
        self.climber.stationary()

class leftClimberGoesDown(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem

    def initialize(self):
        self.climber.leftGoDown()

    def execute(self):
        print("left going down")

    def end(self, interrupted: bool):
        self.climber.stationary()

class climberDoesntMove(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements (kClimberSubsystem)
        self.climber = kClimberSubsystem

    def initialize(self):
        self.climber.stationary()
    
    def execute(self):
        print("stopping")

    def end(self, interrupted: bool):
        self.climber.stationary()
