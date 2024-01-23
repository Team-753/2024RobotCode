import os
import json
import commands2

class RobotContainer:
    """ Basically does everything. Yeah... """
    
    def __init__(self) -> None:
        # importing our JSON settings and converting it to global python dictionary.
        folderPath = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(folderPath, 'config.json')
        with open (filePath, "r") as f1:
            self.config = json.load(f1)
        
        
    def configureButtonBindings(self):
        """ Sets up the button command bindings for the controllers. """
        
    def getAutonomousCommand(self):
        """ Logic for what will run in autonomous mode. Returning anything but a command will result in nothing happening in autonomous. """
        
    def disabledInit(self):
        pass
    
    def autonomousInit(self):
        pass
    
    def autonomousPeriodic(self):
        pass
    
    def teleopInit(self):
        pass
    
    def teleopPeriodic(self):
        pass
    
    def testInit(self):
        pass
    
    def testPeriodic(self):
        pass
    
    