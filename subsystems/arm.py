from commands2.timedcommandrobot import seconds
import wpilib
from wpilib import TimedRobot
import wpilib.drive
import commands2
import rev
from rev import _rev
import phoenix5
import wpimath
from wpimath import kinematics
class ArmSubsystem(commands2.TimedCommandRobot):
    def __init__(self, period: float = TimedRobot.kDefaultPeriod / 1000) -> None:
        super().__init__(period)
        self.leftArm = rev.CANSparkMax(9, _rev.CANSparkLowLevel.MotorType.kBrushless)
        self.rightArm = rev.CANSparkMax(10, _rev.CANSparkLowLevel.MotorType.kBrushless)
        if(self.leftArm != 0):
            spark1 = wpilib.Spark(9)
            spark1.set(0)
            spark2 = wpilib.Spark(10)
            spark2.set(0)
        return self.leftArm.getAbsoluteEncoder(), self.rightArm.getAbsoluteEncoder()
    