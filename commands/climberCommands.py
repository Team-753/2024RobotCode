
import commands2
from subsystems.climber import ClimberSubsystem

class climberEvents(commands2.command):
    def __init__(self):
        super().__init__()
        self.climber = ClimberSubsystem
    
    def climberGoesUp(self):
        self.climber.goUp()
    
    def climberGoesDown(self):
        self.climber.goDown()

