import commands2
import swerveModule
import wpilib 
import math
class DriveTrainSubsystem(commands2.Subsystem):
    
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config # inhereting the robot config json from the robot container
        
        self.frontLeft = swerveModule(self.config ["swerveModules"]['frontLeft'], "frontLeft")
        self.frontRight = swerveModule(self.config ["swerveModules"]['frontRight'], 'frontRight')
        self.rearLeft = swerveModule(self.config ["serveModules"]['rearLeft'], 'rearLeft')
        self.rearRight = swerveModule(self.config ["swerveModules"]["rearRight"], "rearRight")

    def joystickDrive (self, joystickX, joystickY, joyStickZ):
        pass
       

