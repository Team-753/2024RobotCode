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
        self.bottomMotor = _rev.CANSparkMax(RobotConfig.grabber.bottomMotorCANID, _rev.CANSparkMax.MotorType.kBrushless)
        self.topMotor = _rev.CANSparkMax(RobotConfig.grabber.topMotorCANID, _rev.CANSparkMax.MotorType.kBrushless)
        self.topMotor.follow(self.bottomMotor, True)
        self.sensor = wpilib.DigitalInput(RobotConfig.grabber.sensorDIOID)
        global released
        released = True
    def periodic(self) -> None:
        # TODO: code to get commands from drive station joysticks
        # sets bottom motor position and tells top motor to follow. Top motor IS inverted.
        return super().periodic()
    def releasedVar(self) -> None:
        released = False
        return released
    def unreleasedVar(self) -> None:
        released = True
        return released
    def intake(self) -> None:
        # TODO: Code to intake ring
        self.bottomMotor.set(RobotConfig.grabber.intake)
        '''if(self.sensor.get() != False):
            while(self.sensor.get() != False):
                # Stop inputting
                self.bottomMotor.set(RobotConfig.grabber.idle)
                self.topMotor.follow(self.bottomMotor, True)
        else:
            # Stop inputting
            self.bottomMotor.set(RobotConfig.grabber.idle)
            self.topMotor.follow(self.bottomMotor, True)'''
        if(self.sensor.get() == False):
            # Wait until false or released
            while((self.sensor.get() == True) or (released == True)):
                self.bottomMotor.set(RobotConfig.grabber.idle)
        else:
            # Stop inputting
            self.bottomMotor.set(RobotConfig.grabber.idle)
    def outtakeSlow(self) -> None:
        # TODO: Code to shoot the ring based on command speed
        self.bottomMotor.set(RobotConfig.grabber.outtakeS)
    def outtakeFast(self) -> None:
        # TODO: Code to shoot the ring based on command speed
        self.bottomMotor.set(RobotConfig.grabber.outtakeF)
    def idle(self) -> None:
        self.bottomMotor.set(RobotConfig.grabber.idle)
        
