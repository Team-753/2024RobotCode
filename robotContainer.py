import RobotConfig
import commands2
from commands2 import button, cmd
from subsystems.driveTrain import DriveTrainSubsystem
from subsystems.arm import ArmSubsystem
from commands.defaultDriveCommand import DefaultDriveCommand
from subsystems.arm import ArmSubsystem
from commands.ArmCommands import ArmSpeaker
from commands.ArmCommands import up
#from commands.ArmCommands import armEvents
from commands.ArmCommands import grab, empty, emptySlow, up, ampEmpty, down
from wpilib.cameraserver import CameraServer
import wpilib
from subsystems.grabber import grabberSubsystem
class RobotContainer:
    """ Basically does everything. Yeah... """
    
    def __init__(self) -> None:
        # importing our JSON settings and converting it to global python dictionary.
        # initializing controllers
        self.joystick = button.CommandJoystick(RobotConfig.DriveConstants.Joystick.USB_ID)
        self.auxController = button.CommandXboxController(RobotConfig.DriveConstants.XBOX.USB_ID)
        # initializing subsystems
        self.driveTrain = DriveTrainSubsystem(self.joystick)
        self.grabber = grabberSubsystem()
        self.arm = ArmSubsystem()
        #self.arm.setDesiredAngle(5)
        """
        Setting our default commands, these are commands similar to the "periodic()" functions that 
        are ran every loop but only when another command IS NOT running on the subsystem hence the
        "default" keyword.
        """
        self.configureButtonBindings()
        
    def configureButtonBindings(self):
        """ Sets up the button command bindings for the controllers. """
        self.auxController.leftTrigger().whileTrue(empty(self.grabber))
        #self.auxController.leftTrigger().whileTrue(print("left"))
        #self.auxController.leftTrigger().whileTrue(cmd.run(lambda: self.grabber.outtakeFast))
        self.auxController.leftBumper().whileTrue(emptySlow(self.grabber))
        #self.auxController.leftBumper().whileTrue(cmd.)
        self.auxController.rightTrigger().whileTrue(grab(self.grabber))
        self.auxController.rightBumper().whileTrue(ampEmpty(self.grabber))
        # TODO: Check presets
        # For now, arm uses A for Amp preset
        
        #self.upJoystick = self.auxController.getLeftY()
        #self.upJoystick.whileTrue(up(self.arm))
        #self.upJoystick
        #print(self.upJoystick)
        #self.auxController.getAButtonPressed(cmd.runOnce(lambda self.arm.setDesiredAngle(RobotConfig.armConstants.Amp)))
        self.buttonA = self.auxController.a()
        self.buttonA.onTrue(up(self.arm))
        #.buttonA = self.auxController.a()
        #self.buttonA.whileTrue(up(self.arm))
        #self.buttonA.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Amp)))
        #self.auxController.A(armEvents.amp(self))
        # For now, arm uses B for Home preset
        
        self.buttonY = self.auxController.y()
        #self.buttonB.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Home)))
        self.buttonY.onTrue(down(self.arm))
        '''
        # For now, arm uses X for Speaker preset
        
        self.buttonX = self.auxController.x()
        self.buttonX.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Speaker)))
        
        # For now, arm uses Y for Source preset
        
        self.buttonY = self.auxController.y()
        self.buttonY.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Source)))
        '''
        
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
    
    