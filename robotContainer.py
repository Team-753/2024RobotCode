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
from commands.defaultDriveCommand import DefaultDriveCommand, ResetNavx
from subsystems.arm import ArmSubsystem
from subsystems.climber import ClimberSubsystem
from subsystems.grabber import grabberSubsystem
from commands.climberCommands import oneClimberGoesDown, oneClimberGoesUp, bothClimbersGoUp, bothClimbersGoDown, JoystickControl, climberDoesntMove
from commands.ArmCommands import ArmSpeaker
#from commands.ArmCommands import grabberEvents
from commands.ArmCommands import grab, empty, emptySlow, ArmDown, ampEmpty, ArmUp, manualShoot, ArmConfirmUp, AutoShootSpeaker
from wpilib.cameraserver import CameraServer
#from commands.ArmCommands import empty
#from commands.ArmCommands import armEvents
from pathplannerlib.auto import PathPlannerAuto
<<<<<<< HEAD
'''
from commands.basicAuto import simpleAutoDrive, ModificationDrive
'''
=======
from commands.HardAuto import simpleAutoDrive, HardAuto
>>>>>>> 0af38724656fa1fb1e4ff316890592552a392f38
import RobotConfig as config
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
        self.rightClimber = ClimberSubsystem(config.Climber.rightMotorCanID, 0, False)
        self.leftClimber = ClimberSubsystem(config.Climber.leftMotorCanID, 1, True)
        self.rightClimber.stationary()
        self.leftClimber.stationary()
        self.driveTrain.setDefaultCommand(DefaultDriveCommand(self.driveTrain))
        
<<<<<<< HEAD
        #self.leftClimber.setDefaultCommand(JoystickControl(self.leftClimber, self.checkJoystickInput(self.auxController.getLeftY())))
        #self.rightClimber.setDefaultCommand(JoystickControl(self.rightClimber, self.checkJoystickInput(self.auxController.getRightY())))
=======
        #s elf.leftClimber.setDefaultCommand(JoystickControl(self.leftClimber, self.checkJoystickInput(self.auxController.getLeftY())))
        # self.rightClimber.setDefaultCommand(JoystickControl(self.rightClimber, self.checkJoystickInput(self.auxController.getRightY())))
>>>>>>> 0af38724656fa1fb1e4ff316890592552a392f38
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
        self.autonomousChooser.addOption("E Taxi", "E Taxi")
        self.autonomousChooser.addOption("E Right Blue Auto", "E Right Blue Auto")
        self.autonomousChooser.addOption("E Left Blue Auto", "E Left Blue Auto")
        self.autonomousChooser.addOption("E Right Red Auto", "E Right Red Auto")
        self.autonomousChooser.addOption("E Left Red Auto", "E Left Red Auto")
        self.autonomousChooser.addOption("Experimental", "Experimental")
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
        # self.auxController.b().whileTrue(manualShoot(self.grabber)) NOTE: This code causes the robot code to error, the root lies in the shoot() function in the grabber code.
        self.buttonA = self.auxController.a()
        self.buttonA.whileTrue(ArmDown(self.arm))
        
        self.buttonY = self.auxController.y()
        self.buttonY.whileTrue(ArmUp(self.arm))

        self.auxController.pov(0).whileTrue(bothClimbersGoUp(self.rightClimber, self.leftClimber))
        self.auxController.pov(45).whileTrue(oneClimberGoesUp(self.leftClimber))
        self.auxController.pov(135).whileTrue(oneClimberGoesDown(self.leftClimber))
        self.auxController.pov(180).whileTrue(bothClimbersGoDown(self.rightClimber, self.leftClimber))
        self.auxController.pov(225).whileTrue(oneClimberGoesDown(self.rightClimber))
        self.auxController.pov(315).whileTrue(oneClimberGoesUp(self.rightClimber))
        
        self.auxController.axisGreaterThan(0, 0.2).onTrue(oneClimberGoesUp(self.leftClimber))
        self.auxController.axisLessThan(0, -0.2).onTrue(oneClimberGoesDown(self.leftClimber))
        self.auxController.axisGreaterThan(1, 0.2).onTrue(oneClimberGoesUp(self.rightClimber))
        self.auxController.axisLessThan(1, -0.2).onTrue(oneClimberGoesDown(self.rightClimber))

        self.joystickButtonFour = self.joystick.button(4)
        self.joystickButtonFour.onTrue(ResetNavx(self.driveTrain))
    #-----------------------------------------------------------------------------------------------   
    #Autonomous Start Protocol
    def getAutonomousCommand(self):
        pass
        '''
        """ Logic for what will run in autonomous mode. Returning anything but a command will result in nothing happening in autonomous. """
        pathName = self.autonomousChooser.getSelected()
        if pathName == "OnlyForward": 
        
            return commands2.SequentialCommandGroup(commands2.WaitCommand(12), simpleAutoDrive(self.driveTrain))
        
        
        #Experimental Auto, X,Y,Z values in ModificationDrive determine joystick input, and the final float is to determine how long it is executed. 
        #TODO, Add field orient reset
        elif pathName == "E Taxi": # Ryan Modification Area
             
            return commands2.SequentialCommandGroup ( HardAuto(self.driveTrain, 0, 0, 0, 2), HardAuto(self.driveTrain, 0.7, 0, 0, 1), HardAuto) #Ryan's Modifications... Man, I love sketchy modifications
        
        elif pathName == "E Right Blue Auto": 
            return cmd.none() #commands2.SequentialCommandGroup (ArmConfirmUp, AutoShootSpeaker, HardAuto(self.driveTrain, -1, 0, 0, 1.5),HardAuto(self.driveTrain, 0, 0, .3, 1 )) 
        
        elif pathName == "E Left Blue Auto": 
            return cmd.none()
        elif pathName == "E Right Red Auto": 
            return cmd.none() # commands2.SequentialCommandGroup (ArmConfirmUp, AutoShootSpeaker, HardAuto(self.driveTrain, -1, 0, 0, 3),HardAuto(self.driveTrain, 0, 0, 1, .5 )) 
        elif pathName == "E Left Red Auto": 
            return cmd.none()
        elif pathName == "Experimental":
            return commands2.SequentialCommandGroup (ArmConfirmUp(self.grabber), AutoShootSpeaker(self.grabber))
            
        else:
            return PathPlannerAuto(pathName)
        '''
    #-----------------------------------------------------------------------------------------------   
    def checkJoystickInput(self, kInput: float):
        if abs(kInput) < 0.1:
            kInput = 0
        else:
            kInput = kInput/2
        return(kInput)

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
   
    
