# Imports modules for code.
import wpilib
import commands2
import RobotConfig
import rev
from rev import _rev
import wpimath
from wpimath import kinematics
class grabberSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        # sets motors for grabber. For CAN IDs, use RobotConfig
        self.bottomMotor = rev.CANSparkMax(RobotConfig.grabber.bottomMotorCANID, _rev.CANSparkMax.MotorType.kBrushless)
        self.topMotor = rev.CANSparkMax(RobotConfig.grabber.topMotorCANID, _rev.CANSparkMax.MotorType.kBrushless)
        self.sensor = wpilib.DigitalInput(RobotConfig.grabber.sensorDIOID)
    def periodic(self) -> None:
        # TODO: code to get commands from drive station joysticks
        # sets bottom motor position and tells top motor to follow. Top motor IS inverted.
        self.bottomMotor
        self.topMotor.follow(self.bottomMotor, True)
        return super().periodic()
    def intake(self) -> None:
        # TODO: Code to intake ring
        self.bottomMotor.set(RobotConfig.grabber.intake)
        self.topMotor.follow(self.bottomMotor, True)
        if(self.sensor.get() != False):
            while(self.sensor.get() != False):
                # Stop inputting
                self.bottomMotor.set(RobotConfig.grabber.idle)
                self.topMotor.follow(self.bottomMotor, True)
        else:
            # Stop inputting
            self.bottomMotor.set(RobotConfig.grabber.idle)
            self.topMotor.follow(self.bottomMotor, True)
    def outtake(self) -> None:
        # TODO: Code to shoot the ring based on command speed
        self.bottomMotor.set(RobotConfig.grabber.outtake)
        self.topMotor.follow(self.bottomMotor, True)
    def idle(self) -> None:
        self.bottomMotor.set(RobotConfig.grabber.idle)
        self.topMotor.follow(self.bottomMotor, True)