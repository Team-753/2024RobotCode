# Imports modules for code.
import wpilib
import commands2
import RobotConfig
import rev
from rev import _rev
import wpimath
from wpimath import kinematics
from time import sleep
class grabberSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        # sets motors for grabber. For CAN IDs, use RobotConfig
        self.rearMotor = rev.CANSparkMax(RobotConfig.grabber.bottomMotorCANID, _rev.CANSparkMax.MotorType.kBrushless)
        self.frontMotor = rev.CANSparkMax(RobotConfig.grabber.topMotorCANID, _rev.CANSparkMax.MotorType.kBrushless)
        self.shooterEncoder = self.frontMotor.getEncoder()
        #self.topMotor.follow(self.bottomMotor, False)
        self.sensor = wpilib.DigitalInput(RobotConfig.grabber.sensorDIOID)
        self.readyToShoot = False
        #self.myTimer = wpilib.Timer()
        #self.myTimer.restart()
    def periodic(self) -> None:
        # TODO: code to get commands from drive station joysticks
        # sets bottom motor position and tells top motor to follow. Top motor IS inverted.
        self.shooterVelocity = self.shooterEncoder.getVelocity()
        if abs(self.shooterVelocity) >= 400:
            self.readyToShoot = True
            wpilib.SmartDashboard.putBoolean("Ready to shoot", True)
        else:
            wpilib.SmartDashboard.putBoolean("Ready to shoot", False)
            self.readyToShoot = False
        wpilib.SmartDashboard.putNumber("Shooter RPM", self.shooterVelocity)
        return super().periodic()
    def intake(self) -> None:
        print("Intake")
        # TODO: Code to intake ring
        self.rearMotor.set(RobotConfig.grabber.intake)
        self.frontMotor.set(RobotConfig.grabber.intake*-1)
        sleep(.5)
        self.rearMotor.set(0)
        self.frontMotor.set(0)
    def inOuttake(self) -> None:
        print("Intake Direction Shoot")
        # TODO: Code to intake ring
        self.rearMotor.set(RobotConfig.grabber.outtakeS)
        self.frontMotor.set(RobotConfig.grabber.outtakeS*-1)
    def outtakeSlow(self) -> None:
        print("1 Outtake")
        # TODO: Code to shoot the ring based on command speed
        self.frontMotor.set(RobotConfig.grabber.outtakeF*-1)
        print(self.shooterVelocity)
    def outtakeFast(self) -> None:
        print("2 Outtake")
        if self.readyToShoot == True:
            self.frontMotor.set(RobotConfig.grabber.outtakeF*-1)
            self.rearMotor.set(RobotConfig.grabber.outtakeF)
        else:
            print("Not enough RPM")
        # Ramp up with button, then shoot after 3+ seconds on button press
        #self.bottomMotor.set(RobotConfig.grabber.outtakeF)
    def idle(self) -> None:
        self.rearMotor.set(RobotConfig.grabber.idle)
        self.frontMotor.set(RobotConfig.grabber.idle)
