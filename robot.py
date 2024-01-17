import wpilib
import commands2
from robotContainer import RobotContainer

class MyRobot(commands2.TimedCommandRobot):
    
    def __init__(self, period = 0.02) -> None:
        super().__init__(period) # setting the robot code to run every 0.02 seconds (every 20 milliseconds)
        
    def robotInit(self):
        """ Robot initation code goes here, though the vast majority will be in the robot container file. """
        self.robotContainer = RobotContainer()
        self.autoCommand = commands2.Command()
        
    def disabledInit(self) -> None:
        """ Runs when the robot is disabled. """
        ''''''
        return super().disabledInit()
            
    def testInit(self) -> None:
        """ Runs once at the beginning of test mode. """
        return super().testInit()
    
    def testPeriodic(self) -> None:
        """ Loops during test mode. """
        return super().testPeriodic()
    
    def autonomousInit(self):
        """ Runs once when autonomous mode is initiated. """
        self.robotContainer.autonomousInit()
        self.autoCommand = self.robotContainer.getAutonomousCommand()
        if (self.autoCommand != commands2.Command()):
            self.autoCommand.schedule()
    
    def disabledExit(self) -> None:
        """ Runs once when the robot exits disabled mode, so essentially runs when entering any mode. """
        self.robotContainer.disabledExit()
        
    def autonomousPeriodic(self):
        """ Loops during autonomous, nothing should really go here as autonomous is all auto-commnand based. """
        pass
    
    def autonomousExit(self) -> None:
        """ Runs once when autonomous mode is ended. """
        if (self.autoCommand != commands2.Command()):
            self.autoCommand.cancel()
        
    def teleopInit(self):
        """ Runs once when teleop is started """
        self.robotContainer.teleopInit()
        
    def teleopPeriodic(self):
        '''This function is called periodically during operator control. Nothing should be needed here as the default commands assigned
        in the robot container should suffice. '''
        pass
    
    def disabledPeriodic(self):
        ''' Runs while the robot is idle '''
        self.robotContainer.disabledPeriodic()
        
    def disabledInit(self) -> None:
        '''self.driveTrain.coast()'''
        self.robotContainer.disabledInit()
    
    def testInit(self) -> None:
        self.robotContainer.testInit()
    
    def testPeriodic(self) -> None:
        self.robotContainer.testPeriodic()
    
if __name__ == "__main__":
    wpilib.run(MyRobot)