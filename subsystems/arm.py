# Imports for arm.
import wpilib
import commands2
import RobotConfig
import rev
from rev import _rev

class ArmSubsystem(commands2.Subsystem):
    kMotorToArmDegrees = 360 / (2.5 * 20) # each rotation of the motor is 7.2 degrees
    kMotorToArmDegreeVelocity = kMotorToArmDegrees / 60 # each rotation of the motor is 7.2 degrees
    def __init__(self) -> None:
        """ This is ran once, it returns NOTHING """
        super().__init__()
        # Sets motors for arm commands
        self.leftArm = _rev.CANSparkMax(RobotConfig.Arm.leftMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        self.rightArm = _rev.CANSparkMax(RobotConfig.Arm.rightMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        self.leftArm.follow(self.rightArm, True)
    def home(self) -> None:
        self.rightArm.set(RobotConfig.armConstants.Home)   
    def source(self) -> None:
        self.rightArm.set(RobotConfig.armConstants.Source)  
    def speaker(self) -> None:
        self.rightArm.set(RobotConfig.armConstants.Speaker)   
    def amp(self) -> None:
        self.rightArm.set(RobotConfig.armConstants.Amp)
    def periodic(self) -> None:
        # updates the PID controllers to go to the wanted position
        '''self.leftPIDController.setReference(self.desiredAngle, _rev.CANSparkMax.ControlType.kPosition)
        self.rightPIDController.setReference(self.desiredAngle, _rev.CANSparkMax.ControlType.kPosition)'''
        
       
    def setDesiredAngle(self, kDesiredAngle: float):
        self.desiredAngle = kDesiredAngle

    