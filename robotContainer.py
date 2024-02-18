import RobotConfig
import commands2
from commands2 import button, cmd
from subsystems.driveTrain import DriveTrainSubsystem
from subsystems.arm import ArmSubsystem
from commands.defaultDriveCommand import DefaultDriveCommand
from subsystems.arm import ArmSubsystem
from subsystems.climber import ClimberSubsystem
from commands.climberCommands import climberEvents
from commands.ArmCommands import ArmSpeaker
from commands.ArmCommands import grabberEvents
class RobotContainer:
    """ Basically does everything. Yeah... """
    
    def __init__(self) -> None:
        # importing our JSON settings and converting it to global python dictionary.
        
        # initializing controllers
        self.joystick = button.CommandJoystick(RobotConfig.DriveConstants.Joystick.USB_ID)
        self.auxController = button.CommandXboxController(RobotConfig.DriveConstants.XBOX.USB_ID)
        # initializing subsystems
        self.driveTrain = DriveTrainSubsystem(self.joystick)
        self.arm = ArmSubsystem()
        self.climber = ClimberSubsystem()
        self.grabber = grabberSubsystem()
        """
        Setting our default commands, these are commands similar to the "periodic()" functions that 
        are ran every loop but only when another command IS NOT running on the subsystem hence the
        "default" keyword.
        """
        self.configureButtonBindings()
        
    def configureButtonBindings(self):
        """ Sets up the button command bindings for the controllers. """
        self.auxController.leftTrigger().whileTrue(empty(self.grabber))
        self.auxController.rightTrigger().whileTrue(grab(self.grabber))
        # TODO: Check presets
        # For now, arm uses A for Amp preset
        self.auxController.A().onTrue(armEvents.amp())
        #self.auxController.A(armEvents.amp(self))
        # For now, arm uses B for Home preset
        self.auxController.B().onTrue(armEvents.home())
        # For now, arm uses X for Speaker preset
        self.auxController.X().onTrue(armEvents.speaker())
        # For now, arm uses Y for Source preset
        self.auxController.Y().onTrue(armEvents.source())
        #temporary climber controls
        self.auxController.rightBumper().whileTrue(climberEvents.climberGoesUp())
        self.auxController.leftBumper().whileTrue(climberEvents.climberGoesDown())
        
    def getAutonomousCommand(self):
        """ Logic for what will run in autonomous mode. Returning anything but a command will result in nothing happening in autonomous. """
        
    def disabledInit(self):
        pass
    
    def autonomousInit(self):
        self.driveTrain.setDefaultCommand(cmd.run(lambda: None, [self.driveTrain])) # otherwise the robot will respond to joystick inputs during autonomous
    
    def autonomousPeriodic(self):
        pass
    
    def teleopInit(self):
        self.driveTrain.setDefaultCommand(DefaultDriveCommand(self.driveTrain))     
    
    def teleopPeriodic(self):
        pass
    
    def testInit(self):
        self.driveTrain.setDefaultCommand(DefaultDriveCommand(self.driveTrain))
    
    def testPeriodic(self):
        pass
    
    
