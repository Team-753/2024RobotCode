
import commands2
from subsystems.climber import ClimberSubsystem

class climberGoesUp(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem
    
    def execute(self):
        print ("going up")
        self.climber.goUp()
      
    
class climberGoesDown(commands2.Command):
    def __init__(self, kClimberSubsystem: ClimberSubsystem):
        super().__init__()
        self.addRequirements(kClimberSubsystem)
        self.climber = kClimberSubsystem

    def execute(self):
        print("going down")
        self.climber.goDown()
        

