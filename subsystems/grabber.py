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
        self.rearMotor.IdleMode(_rev.CANSparkMax.IdleMode.kBrake)
        self.shooterEncoder = self.frontMotor.getEncoder()
        #self.topMotor.follow(self.bottomMotor, False)
        self.sensor = wpilib.DigitalInput(RobotConfig.grabber.sensorDIOID)
        self.readyToShoot = False
        #self.myTimer = wpilib.Timer()
        #self.myTimer.restart()
    def grabberMotorInverted(self, speed):
        self.frontMotor.set(speed)
        self.rearMotor.set(speed*-1)
    def periodic(self) -> None:
        # TODO: code to get commands from drive station joysticks
        # sets bottom motor position and tells top motor to follow. Top motor IS inverted.
        self.shooterVelocity = self.shooterEncoder.getVelocity()
        if abs(self.shooterVelocity) >= 540:
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
        if (abs(self.shooterEncoder.getVelocity()) > 0):
            self.ringIn = False
            wpilib.SmartDashboard.putBoolean("Ring in wrist", False)
            self.rearMotor.set(RobotConfig.grabber.intake*(1/9))
            self.frontMotor.set(RobotConfig.grabber.intake*-1)
        else:
            self.ringIn = True
            wpilib.SmartDashboard.putBoolean("Ring in wrist", True)
            self.rearMotor.set(RobotConfig.grabber.idle)
            self.frontMotor.set(RobotConfig.grabber.idle)
    def intakeSlow(self) -> None:
        self.frontMotor.set(RobotConfig.grabber.intakeS)
        self.rearMotor.set(RobotConfig.grabber.intakeS)
        sleep(0.5)
        self.grabberMotorInverted(RobotConfig.grabber.idle)
    def ampShoot(self) -> None:
        # TODO: Code to intake ring
        self.grabberMotorInverted(RobotConfig.grabber.outtakeS*1)
        '''
        self.rearMotor.set(RobotConfig.grabber.outtakeS*-1)
        self.frontMotor.set(RobotConfig.grabber.outtakeS)
        '''
    def speedUpShoot(self) -> None:
        # TODO: Code to shoot the ring based on command speed
        self.frontMotor.set(RobotConfig.grabber.outtakeF*-1)
        print(self.shooterVelocity)
    def speakerShoot(self) -> None:
        self.grabberMotorInverted(RobotConfig.grabber.outtakeF*-1)
        '''
            self.frontMotor.set(RobotConfig.grabber.outtakeF*-1)
            self.rearMotor.set(RobotConfig.grabber.outtakeF)
            '''
        # Ramp up with button, then shoot after 3+ seconds on button press
        #self.bottomMotor.set(RobotConfig.grabber.outtakeF)
    def shoot(self) -> None:
        self.grabberMotorInverted(RobotConfig.grabber.outtakeReallySlow*-1)
        '''
        self.frontMotor.set(RobotConfig.grabber.outtakeS*-.5)
        self.rearMotor.set(RobotConfig.grabber.outtakeS*.5)
        '''
        # Ramp up with button, then shoot after 3+ seconds on button press
        #self.bottomMotor.set(RobotConfig.grabber.outtakeF)
    
    def idle(self) -> None:
        self.grabberMotorInverted(RobotConfig.grabber.idle)
        '''
        self.rearMotor.set(RobotConfig.grabber.idle)
        self.frontMotor.set(RobotConfig.grabber.idle)
        '''


