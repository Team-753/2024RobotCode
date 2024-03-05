
import commands2
from subsystems.climber import ClimberSubsystem

class climberGoesUp(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem
        
    def initialize(self):
        self.climber.goUp()
    
    def execute(self):
        print ("going up")

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
       
        

