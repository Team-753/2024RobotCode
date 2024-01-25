import os
import json
from networktables import NetworkTables
import commands2
import swerveModule
import wpilib 
import math
import navx
from wpimath import geometry, kinematics


class RobotContainer:
    """ Basically does everything. Yeah... """

    NetworkTables.initialize() # you use networktables to access limelight data

    def __init__(self) -> None:
        # importing our JSON settings and converting it to global python dictionary.
        folderPath = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(folderPath, 'config.json')
        with open (filePath, "r") as f1:
            self.config = json.load(f1)
        self.LimelightTable = NetworkTables.getTable('limelight') # giving us access to the limelight's data as a variable


    def configureButtonBindings(self):
        """ Sets up the button command bindings for the controllers. """


class DriveTrainSubsystem(commands2.Subsystem):

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config # inhereting the robot config json from the robot container

        self.navx = navx.AHRS.create_spi(update_rate_hz=100)

        self.kMaxSpeed = self.config ["RobotDefaultSettings"]["wheelVelocityLimit"]
        self.kmaxAutoSpeed = self.config ["autonomousSettings"]["autoVelLimit"]
        self.wheelBase = self.config["RobotDimensions"]["wheelBase"]
        self.trackWidth = self.config["RobotDimensions"]["trackWidth"]

        self.frontLeft = swerveModule(self.config ["swerveModules"]['frontLeft'], "frontLeft")
        self.frontRight = swerveModule(self.config ["swerveModules"]['frontRight'], 'frontRight')
        self.rearLeft = swerveModule(self.config ["serveModules"]['rearLeft'], 'rearLeft')
        self.rearRight = swerveModule(self.config ["swerveModules"]["rearRight"], "rearRight")

        self.KINEMATICS = kinematics.SwerveDrive2Kinematics( geometry.Translation2d (self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d (self.trackWidth / 2, -self.wheelBase / 2), geometry.Translation2d(-self.trackWidth / 2, self.wheelBase / 2), geometry.Translation2d (-self.trackWidth / 2, -self.wheelBase /2))

    def joystickDrive (self, joystickX, joystickY, joyStickZ):
        pass