# assuming that we are using the krakens
import wpilib
import phoenix5
import phoenix6
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
        self.rightMotor = phoenix6.hardware.TalonFX(self.config.Climber.rightMotorCanID, "rightMotor")
        self.rightMotorController = phoenix6.controls.PositionVoltage(0)
        self.leftMotor = phoenix5.TalonFX(self.config.Climber.leftMotorCanID)
        rightMotorFeedbackConfigs = phoenix6.configs.talon_fx_configs.FeedbackConfigs()
        rightMotorFeedbackConfigs.feedback_sensor_source = 0
        #self.rightMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        self.leftMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        rightMotorConfig = phoenix6.configs.TalonFXConfiguration()
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

        rightMotorConfig.slot0.k_p = pidConfig.rightMotorPIDs.kP
        rightMotorConfig.slot0.k_i = pidConfig.rightMotorPIDs.kI
        rightMotorConfig.slot0.k_d = pidConfig.rightMotorPIDs.kD
        #rightMotorConfig.slot0.k_ff = pidConfig.rightMotorPIDs.kF
        '''rightMotorConfig.slot0.allowableClosedloopError = pidConfig.leftMotorPIDs.error
        rightMotorConfig.slot0.integralZone = pidConfig.rightMotorPIDs.izone'''

        leftMotorCurrentConfig = phoenix5.SupplyCurrentLimitConfiguration()
        leftMotorCurrentConfig.currentLimit = pidConfig.leftMotorPIDs.currentLimit

        rightMotorCurrentConfig = phoenix6.configs.talon_fx_configs.CurrentLimitsConfigs()
        rightMotorCurrentConfig.supply_current_limit = pidConfig.rightMotorPIDs.currentLimit

        leftMotorConfig.supplyCurrLimit = leftMotorCurrentConfig
        rightMotorConfig.with_current_limits (rightMotorCurrentConfig)

        rightMotorConfig.with_feedback

        self.leftMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        #self.rightMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        
        self.leftMotor.configAllSettings(leftMotorConfig, 50)
        self.rightMotor.configurator.apply(rightMotorConfig)
        #self.rightMotor.configAllSettings(rightMotorConfig, 50)

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
