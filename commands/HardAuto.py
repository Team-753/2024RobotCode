import commands2
from subsystems.driveTrain import DriveTrainSubsystem
import wpilib

class simpleAutoDrive(commands2.Command):
    
    def __init__(self, driveTrainSubsysten: DriveTrainSubsystem):
        super().__init__()
        self.addRequirements(driveTrainSubsysten)
        self.driveTrain = driveTrainSubsysten
        self.timer = wpilib.Timer()
    
    def initialize(self):
        self.timer.start()
        
    def execute(self):
        self.driveTrain.joystickDrive((0.5, 0, 0))

    def isFinished(self) -> bool:
         if self.timer.hasElapsed(1):
            self.timer.stop()
            self.timer.reset()
            return True
    
    def end(self, interrupted: bool):
        self.driveTrain.joystickDrive((0, 0, 0))

#----------------------------------------------------------------------
#Ryans modification for Hard Auto 
#HardAuto reffers to autos built into the machine, not using PathPlanner
#This modification is designed to create "easy" HardAuto

class ModificationDrive(commands2.Command):
    
    def __init__(self, driveTrainSubsysten: DriveTrainSubsystem, X: float, Y: float, Z: float, Duration: float):
        super().__init__()
        self.addRequirements(driveTrainSubsysten) 
        self.driveTrain = driveTrainSubsysten
        self.timer = wpilib.Timer() # Used to keep track of time. use Distance = Speed*Time to best use this. WIP is to mesure speed of the robot at 100% speed
        self.X = X # User input for X 
        self.Y = Y # User input for Y
        self.Z = Z # User input for Z
        self.Duration = Duration # User defined time. When set, it compares to timer to stop the Auto. PLEASE SET THIS LOW 
    
    def initialize(self):
        self.timer.reset()
        self.timer.start() # Start the timer so that isFinsihed can compare Duration and the Timer Command.
        
    def execute(self):
        self.driveTrain.joystickDrive((self.X, self.Y, self.Z)) # Take in user inputs for the robot
        # Use the speed of the device to calculate distance, Distance = Speed*Time

    def isFinished(self) -> bool:
         if self.timer.hasElapsed(self.Duration): # Compares Duration and WPILIB Timer to end command after user specified time 
            return True # start the end 
            
    
    def end(self, interrupted: bool):
        self.driveTrain.joystickDrive((0, 0, 0)) # Stop all movement
        self.timer.stop() # Safety precaution? 