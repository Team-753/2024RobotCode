import wpilib
import commands2
import RobotConfig
import rev
from rev import _rev
import wpimath
from wpimath import kinematics
class ArmSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        """ This is ran once, it returns NOTHING """
        super().__init__()
        self.leftArm = rev.CANSparkMax(RobotConfig.Arm.leftMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        self.rightArm = rev.CANSparkMax(RobotConfig.Arm.rightMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        
    def periodic(self) -> None:
        """ Put code you want to be looped in here. Nothing is returned here either."""
        return super().periodic()
    