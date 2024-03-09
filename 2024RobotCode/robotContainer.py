import RobotConfig
import commands2
import math
import wpilib
import pathplannerlib
import os
from commands.turnToCommand import TurnToCommand
from wpimath import geometry, kinematics, estimator
from commands2 import button, cmd
from subsystems.driveTrain import DriveTrainSubsystem
from commands.defaultDriveCommand import DefaultDriveCommand
from subsystems.arm import ArmSubsystem
from subsystems.climber import ClimberSubsystem
from subsystems.grabber import grabberSubsystem
from commands.climberCommands import climberGoesUp, climberGoesDown, climberDoesntMove, rightClimberGoesUp, rightClimberGoesDown, leftClimberGoesDown, leftClimberGoesUp
from commands.ArmCommands import ArmSpeaker
#from commands.ArmCommands import grabberEvents
from commands.ArmCommands import grab, empty, emptySlow, up, ampEmpty, down, manualShoot
from wpilib.cameraserver import CameraServer
#from commands.ArmCommands import empty
#from commands.ArmCommands import armEvents
from pathplannerlib.auto import PathPlannerAuto
from commands.basicAuto import simpleAutoDrive

#from commands.ArmCommands import grabberEvents
class RobotContainer:
    """ Basically does everything. Yeah... """
    #--------------------------------------------------------------------------------
    #Autonomous Auto Select
    folderPath = os.path.dirname(os.path.abspath(__file__))
    tempAutoList = os.listdir(os.path.join(folderPath, 'deploy/pathplanner/autos'))
    autoList = []
    for pathName in tempAutoList:
            autoList.append(pathName.removesuffix(".auto"))
    #--------------------------------------------------------------------------------
    def __init__(self) -> None:
        # importing our JSON settings and converting it to global python dictionary.
        
        # initializing controllers
        self.joystick = button.CommandJoystick(RobotConfig.DriveConstants.Joystick.USB_ID)
        self.auxController = button.CommandXboxController(RobotConfig.DriveConstants.XBOX.USB_ID)
        # initializing subsystems
        self.grabber = grabberSubsystem()
        self.driveTrain = DriveTrainSubsystem(self.joystick)
        self.arm = ArmSubsystem()
        self.climber = ClimberSubsystem()
        self.climber.stationary()
        self.driveTrain.setDefaultCommand(DefaultDriveCommand(self.driveTrain))
        """
        Setting our default commands, these are commands similar to the "periodic()" functions that 
        are ran every loop but only when another command IS NOT running on the subsystem hence the
        "default" keyword.
        """
        #self.climber.goUp()
        self.configureButtonBindings()
    #--------------------------------------------------------------------------------
    #Configure Auto Settings
        self.autonomousChooser = wpilib.SendableChooser()
        self.autonomousChooser.setDefaultOption("OnlyForward", "OnlyForward")
        #self.autonomousChooser.addOption("Only Taxi", "Only Taxi")
        for pathName in self.autoList:
            self.autonomousChooser.addOption(pathName, pathName)
        wpilib.SmartDashboard.putData("Autonomous Chooser", self.autonomousChooser)
    #--------------------------------------------------------------------------------    
    def configureButtonBindings(self):
        """ Sets up the button command bindings for the controllers. """
        self.auxController.leftTrigger().whileTrue(grab(self.grabber))
        self.auxController.leftBumper().whileTrue(ampEmpty(self.grabber))
        self.auxController.rightTrigger().whileTrue(empty(self.grabber))
        self.auxController.rightBumper().whileTrue(emptySlow(self.grabber))#self.upJoystick = self.auxController.getLeftY()
        self.auxController.b().whileTrue(manualShoot(self.grabber))
        #self.upJoystick.whileTrue(up(self.arm))
        #self.upJoystick
        #print(self.upJoystick)
        #self.auxController.getAButtonPressed(cmd.runOnce(lambda self.arm.setDesiredAngle(RobotConfig.armConstants.Amp)))
        self.buttonA = self.auxController.a()
        self.buttonA.whileTrue(up(self.arm))
        #.buttonA = self.auxController.a()
        #self.buttonA.whileTrue(up(self.arm))
        #self.buttonA.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Amp)))
        #self.auxController.A(armEvents.amp(self))
        # For now, arm uses B for Home preset
        
        self.buttonY = self.auxController.y()
        #self.buttonB.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Home)))
        self.buttonY.whileTrue(down(self.arm))
        '''
        # For now, arm uses X for Speaker preset
        
        self.buttonX = self.auxController.x()
        self.buttonX.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Speaker)))
        
        # For now, arm uses Y for Source preset
        
        self.buttonY = self.auxController.y()
        self.buttonY.onTrue(cmd.runOnce(lambda: self.arm.setDesiredAngle(RobotConfig.armConstants.Source)))
        '''
        
        #temporary climber controls
        #self.joystickButtonFour.whileTrue(command.RepeatCommand(climberEvents.climberGoesUp()))
        #self.joystickButtonFive.whileTrue(command.RepeatCommand(climberEvents.climberGoesDown()))

        #self.joystickButtonFour.whileTrue(climberGoesUp())
        #self.joystickButtonFive.whileTrue(climberGoesDown())
        
        #these are the semi working climber controls
        '''
        self.auxController.a().onTrue(cmd.runOnce(lambda: self.climber.goUp()))
        self.auxController.a().onFalse(cmd.runOnce(lambda:self.climber.stationary()))
        self.auxController.b().onTrue(cmd.runOnce(lambda: self.climber.goDown()))
        self.auxController.b().onFalse(cmd.runOnce(lambda: self.climber.stationary()))
        #self.auxController.a().whileTrue(cmd.run(lambda: self.climber.goDown(ClimberSubsystem)))
        #self.auxController.b().whileTrue(cmd.run(lambda: self.climber.goUp(ClimberSubsystem)))'''

        #these climber controls might actually work
        '''self.auxController.pov(0).onTrue(cmd.runOnce(lambda: self.climber.goUp()))
        self.auxController.pov(180).onTrue(cmd.runOnce(lambda: self.climber.goDown()))
        self.auxController.pov(-1).onTrue(cmd.runOnce(lambda: self.climber.stationary()))'''
        self.auxController.pov(0).whileTrue(climberGoesUp(self.climber))
        self.auxController.pov(45).whileTrue(leftClimberGoesUp(self.climber))
        self.auxController.pov(135).whileTrue(leftClimberGoesDown(self.climber))
        self.auxController.pov(180).whileTrue(climberGoesDown(self.climber))
        self.auxController.pov(225).whileTrue(rightClimberGoesDown(self.climber))
        self.auxController.pov(315).whileTrue(rightClimberGoesUp(self.climber))
        #self.auxController.pov(-1).onTrue(climberDoesntMove(self.climber))
    #-----------------------------------------------------------------------------------------------   
    #Autonomous Start Protocol
    def getAutonomousCommand(self):
        
        """ Logic for what will run in autonomous mode. Returning anything but a command will result in nothing happening in autonomous. """
        pathName = self.autonomousChooser.getSelected()
        if pathName == "OnlyForward": 
            pass
        #    return commands2.SequentialCommandGroup(ArmConfirmUp, AutoShootSpeaker)
        else:
            return PathPlannerAuto(pathName)
    #-----------------------------------------------------------------------------------------------   
    def disabledInit(self):
        pass
    
    def autonomousInit(self):
        #self.driveTrain.setDefaultCommand(cmd.run(lambda: commands2.Command, [self.driveTrain])) # otherwise the robot will respond to joystick inputs during autonomous
        pass
    
    def autonomousPeriodic(self):
        pass
    
    def teleopInit(self):
        #self.driveTrain.setDefaultCommand(DefaultDriveCommand(self.driveTrain))  
        pass   
    
    def teleopPeriodic(self):
        pass
    
    def testInit(self):
        pass
    
    def testPeriodic(self):
        pass
   
    