# assuming that we are using the krakens
import wpilib
import phoenix5
from phoenix5.sensors import AbsoluteSensorRange
import commands2
import RobotConfig

class ClimberSubsystem(commands2.subsystemBase):

    #motorRatio = 4:1
    zeroed = False

    def __init__(self):
        super().__init__()
        self. config = RobotConfig
        #self.xboxController = xboxController
        self.limitSwitch = wpilib.DigitalInput(self.config.Climber.limitSwitchID)
        self.rightMotor = phoenix5.TalonFX(self.config.Climber.rightMotorCanID)
        self.leftMotor = phoenix5.TalonFX(self.config.Climber.leftMotorCanID)
        self.rightMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        self.leftMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        rightMotorConfig = phoenix5.TalonFXConfiguration()
        leftMotorConfig = phoenix5.TalonFXConfiguration()
        rightMotorConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
        leftMotorConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
        pidConfig = self.config.climberPIDs

        leftMotorConfig.slot0.kP = pidConfig.leftMotorPIDs.kP
        leftMotorConfig.slot0.kI = pidConfig.leftMotorPIDs.kI
        leftMotorConfig.slot0.kD = pidConfig.leftMotorPIDs.kD
        leftMotorConfig.slot0.kP = pidConfig.leftMotorPIDs.kF
        leftMotorConfig.slot0.allowableClosedloopError = pidConfig.leftMotorPIDs.error
        leftMotorConfig.slot0.integralZone = pidConfig.leftMotorPIDs.izone

        rightMotorConfig.slot0.kP = pidConfig.rightMotorPIDs.kP
        rightMotorConfig.slot0.kI = pidConfig.rightMotorPIDs.kI
        rightMotorConfig.slot0.kD = pidConfig.rightMotorPIDs.kD
        rightMotorConfig.slot0.kF = pidConfig.rightMotorPIDs.kF
        rightMotorConfig.slot0.allowableClosedloopError = pidConfig.leftMotorPIDs.error
        rightMotorConfig.slot0.integralZone = pidConfig.rightMotorPIDs.izone

        leftMotorCurrentConfig = phoenix5.SupplyCurrentLimitConfiguration()
        leftMotorCurrentConfig.currentLimit = pidConfig.leftMotorPIDs.currentLimit

        rightMotorCurrentConfig = phoenix5.SupplyCurrentLimitConfiguration()
        rightMotorCurrentConfig.currentLimit = pidConfig.leftMotorPIDs.currentLimit

        leftMotorConfig.supplyCurrLimit = leftMotorCurrentConfig
        rightMotorConfig.supplyCurrLimit = rightMotorConfig

        self.leftMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.rightMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        
        self.leftMotor.configAllSettings(leftMotorConfig, 50)
        self.rightMotor.configAllSettings(rightMotorConfig, 50)

    def periodic (self):
        wpilib.SmartDashboard.putBoolean("Climber Limit Switch", self.limitSwitch.get())
        if not self.zeroed:
            if self.limitSwitch.get():
                self.leftMotor.set(phoenix5.NeutralMode.Coast)
                self.rightMotor.set(phoenix5.NeutralMode.Coast)
                self.leftMotor.setSelectedSensorPosition(0.0, 0, 50)
                self.rightMotor.setSelectedSensorPosition(0.0, 0, 50)
                self.zeroed = True
            else:
                self.leftMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)
                self.rightMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)
        else:
            self.leftMotor



        

    def setPosition(self, ):
        pass
