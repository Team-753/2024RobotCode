import RobotConfig
import commands2
from commands2 import button, cmd, command
from subsystems.driveTrain import DriveTrainSubsystem
from subsystems.arm import ArmSubsystem
from commands.defaultDriveCommand import DefaultDriveCommand
from subsystems.arm import ArmSubsystem
from subsystems.grabber import grabberSubsystem
from subsystems.climber import ClimberSubsystem
from commands.climberCommands import climberGoesDown, climberGoesUp
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
        self.grabber = grabberSubsystem()
        self.climber = ClimberSubsystem()
        self.configureButtonBindings()
        """
        Setting our default commands, these are commands similar to the "periodic()" functions that 
        are ran every loop but only when another command IS NOT running on the subsystem hence the
        "default" keyword.
        """
        
        
    def configureButtonBindings(self):
        """ Sets up the button command bindings for the controllers. """
        #self.joystickButtonFour = button.JoystickButton(self.joystick, 4)
        #self.joystickButtonFive = button.JoystickButton(self.joystick, 5)
        '''self.auxController.leftTrigger().onTrue(grabberEvents.empty(self.grabber))
        self.auxController.rightTrigger().onTrue(grabberEvents.grab(self.grabber))
        self.auxController.leftTrigger().onFalse(grabberEvents.idle(self.grabber))
        self.auxController.rightTrigger().onFalse(grabberEvents.idle(self.grabber))'''
        # TODO: Check presets
        # For now, arm uses A for Amp preset
        self.auxController.a().onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Amp)))
        # For now, arm uses B for Home preset
        self.auxController.b().onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Home)))
        # For now, arm uses X for Speaker preset
        self.auxController.x().onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Speaker)))
        # For now, arm uses Y for Source preset
        self.auxController.y().onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Source)))
        #temporary climber controls
        #self.joystickButtonFour.whileTrue(command.RepeatCommand(climberEvents.climberGoesUp()))
        #self.joystickButtonFive.whileTrue(command.RepeatCommand(climberEvents.climberGoesDown()))

        #self.joystickButtonFour.whileTrue(climberGoesUp())
        #self.joystickButtonFive.whileTrue(climberGoesDown())

        self.auxController.a().whileTrue(climberGoesDown(ClimberSubsystem))
        self.auxController.b().whileTrue(climberGoesUp(ClimberSubsystem))
        #self.auxController.a().whileTrue(cmd.run(lambda: self.climber.goDown(ClimberSubsystem)))
        #self.auxController.b().whileTrue(cmd.run(lambda: self.climber.goUp(ClimberSubsystem)))
        
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
    
    