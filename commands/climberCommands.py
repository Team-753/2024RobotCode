
import commands2
from subsystems.climber import ClimberSubsystem

class climberGoesUp(commands2.Command):
    def __init__(self, climberSubsystem=ClimberSubsystem):
        super().__init__()
        self.addRequirements(climberSubsystem)
        self.climber = ClimberSubsystem
    
    def execute(self):
        print ("going up")
        self.climber.goUp(ClimberSubsystem)
      
    
class climberGoesDown(commands2.Command):
    def __init__(self, climberSubsystem=ClimberSubsystem):
        super().__init__()
        self.addRequirements(climberSubsystem)
        self.climber = ClimberSubsystem

    def execute(self):
        print("going down")
        self.climber.goDown()
        

