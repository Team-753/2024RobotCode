# assuming that we are using the krakens
import wpilib
import phoenix6
import commands2
from commands2 import button
from wpimath import controller
import RobotConfig

class ClimberSubsystem(commands2.subsystemBase):

    def __init__(self):
        super().__init__():
        #self.xboxController = xboxController
        self.rightMotor = phoenix6.hardware.talon_fx.TalonFX(11, 11) # i have no idea what these values should be, will come back later
        self.leftMotor = phoenix6.hardware.talon_fx.TalonFX(12, 12)
        #self.rightMotor.configurator.
        self.leftPIDController 

    def setPosition(self, ):
        pass
