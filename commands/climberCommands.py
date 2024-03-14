
import commands2
from subsystems.climber import ClimberSubsystem
import wpilib

class bothClimbersGoUp(commands2.Command):
    def __init__(self, kRightClimberSubsystem: ClimberSubsystem, kLeftClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kRightClimberSubsystem)
        self.addRequirements(kLeftClimberSubsystem)
        self.rightClimber = kRightClimberSubsystem
        self.leftClimber = kLeftClimberSubsystem
        self.timer = wpilib.Timer()
        
    def initialize(self):
        self.rightClimber.preGoUp()
        self.leftClimber.preGoUp()
        self.timer.start()


    def execute(self):
        if  self.timer.hasElapsed(0.2):
            self.rightClimber.goUp()
            self.leftClimber.goUp()
            self.timer.stop()
            self.timer.reset()

        print ("going up")

    def end(self, interrupted: bool):
        self.leftClimber.stationary()
        self.rightClimber.stationary()

class oneClimberGoesUp(commands2.Command):
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

        print ("right going up")

    def end(self, interrupted: bool):
        self.climber.stationary()

class JoystickControl(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem, kspeed: float):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem
        self.timer = wpilib.Timer()
        self.kspeed = kspeed

    def initialize(self):
        if self.kspeed > 0.0:
            self.climber.preGoUp()
            self.timer.start()
        elif self.kspeed == 0.0:
            self.climber.stationary()
        else:
            self.climber.setVelocity(self.kspeed)
    
    def execute(self):
        if self.timer.hasElapsed(0.2):
            self.climber.setVelocity(self.kspeed)
            self.timer.stop()
            self.timer.reset()
        if abs(self.kspeed) > 0.1:
            print(self.kspeed)
        print(self.kspeed)
    

        

'''class leftClimberGoesUp(commands2.Command):
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
        self.climber.stationary()'''
      
    
class bothClimbersGoDown(commands2.Command):
    def __init__(self, kRightClimberSubsystem: ClimberSubsystem, kLeftClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kRightClimberSubsystem)
        self.addRequirements(kLeftClimberSubsystem)
        self.rightClimber = kRightClimberSubsystem
        self.leftClimber = kLeftClimberSubsystem

    def initialize(self):
        self.rightClimber.goDown()
        self.leftClimber.goDown()

    def execute(self):
        print("one going down")

    def end(self, interrupted: bool):
        self.rightClimber.stationary()
        self.leftClimber.stationary()
    
class oneClimberGoesDown(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem

    def initialize(self):
        self.climber.goDown()

    def execute(self):
        print("one going down")

    def end(self, interrupted: bool):
        self.climber.stationary()

'''class leftClimberGoesDown(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem

    def initialize(self):
        self.climber.leftGoDown()

    def execute(self):
        print("left going down")

    def end(self, interrupted: bool):
        self.climber.stationary()'''

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

