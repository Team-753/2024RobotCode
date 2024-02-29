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
        #self.topMotor.follow(self.bottomMotor, False)
        #self.sensor = wpilib.DigitalInput(RobotConfig.grabber.sensorDIOID)
        global released
        released = True
        #self.myTimer = wpilib.Timer()
        #self.myTimer.restart()
    def periodic(self) -> None:
        # TODO: code to get commands from drive station joysticks
        # sets bottom motor position and tells top motor to follow. Top motor IS inverted.
        return super().periodic()
    def intake(self) -> None:
        print("Intake")
        # TODO: Code to intake ring
        self.bottomMotor.set(RobotConfig.grabber.intake)
        self.topMotor.set(RobotConfig.grabber.intake*-1)
        '''
        if(self.sensor.get() == False):
            # Wait until false or released
            while((self.sensor.get() == True) or (released == True)):
                self.bottomMotor.set(RobotConfig.grabber.idle)
        else:
            # Stop inputting
            self.bottomMotor.set(RobotConfig.grabber.idle)
        '''
    def outtakeSlow(self) -> None:
        print("1 Outtake")
        # TODO: Code to shoot the ring based on command speed
        self.bottomMotor.set(RobotConfig.grabber.outtakeS)
    def outtakeFast(self) -> None:
        print("2 Outtake")
        # Ramp up with button, then shoot after 3+ seconds on button press
        #self.bottomMotor.set(RobotConfig.grabber.outtakeF)
        '''if var + 3 > wpilib.Timer.get():
            self.topMotor.set(RobotConfig.grabber.outtakeF)
        else:
            print(startTime+3)
            print("Doesn't Work!!!")'''
    def idle(self) -> None:
        self.bottomMotor.set(RobotConfig.grabber.idle)
