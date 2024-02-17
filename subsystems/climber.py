# assuming that we are using the krakens
import wpilib
import phoenix5
import phoenix6
from phoenix5.sensors import AbsoluteSensorRange
import commands2
import RobotConfig

class ClimberSubsystem(commands2.Subsystem):

    #motorRatio = 4:1
    zeroed = False

    def __init__(self):
        super().__init__()
        self.targetValue = 0
        self.encoderConversionFactor = 2048 # this is just a temporary number need to find the real one
        self.gearRatio = 4 #gears are 4 to 1 so im assuming that this is four. will need to expierment with this to find the one inch of travel ratio
        self.config = RobotConfig
        #self.xboxController = xboxController
        self.limitSwitch = wpilib.DigitalInput(self.config.Climber.limitSwitchID)
        self.rightMotor = phoenix6.hardware.TalonFX(self.config.Climber.rightMotorCanID)
        self.rightMotorController = phoenix6.controls.PositionDutyCycle(0)
        self.motorCoaster = phoenix6.controls.CoastOut()
        self.leftMotor = phoenix5.TalonFX(self.config.Climber.leftMotorCanID)
        motorFeedbackConfigs = phoenix6.configs.talon_fx_configs.FeedbackConfigs()
        motorFeedbackConfigs.feedback_sensor_source = 0
        #self.rightMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        self.leftMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        motorConfig = phoenix6.configs.TalonFXConfiguration()
        leftMotorConfig = phoenix5.TalonFXConfiguration()
        #motorConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
        leftMotorConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
        pidConfig = self.config.climberPIDs

        leftMotorConfig.slot0.kP = pidConfig.leftMotorPIDs.kP
        leftMotorConfig.slot0.kI = pidConfig.leftMotorPIDs.kI
        leftMotorConfig.slot0.kD = pidConfig.leftMotorPIDs.kD
        leftMotorConfig.slot0.kP = pidConfig.leftMotorPIDs.kF
        leftMotorConfig.slot0.allowableClosedloopError = pidConfig.leftMotorPIDs.error
        leftMotorConfig.slot0.integralZone = pidConfig.leftMotorPIDs.izone

        motorConfig.slot0.k_p = pidConfig.rightMotorPIDs.kP
        motorConfig.slot0.k_i = pidConfig.rightMotorPIDs.kI
        motorConfig.slot0.k_d = pidConfig.rightMotorPIDs.kD
        motorConfig.slot0.k_v = pidConfig.rightMotorPIDs.kF
        '''rightMotorConfig.slot0.allowableClosedloopError = pidConfig.leftMotorPIDs.error
        rightMotorConfig.slot0.integralZone = pidConfig.rightMotorPIDs.izone'''

        leftMotorCurrentConfig = phoenix5.SupplyCurrentLimitConfiguration()
        leftMotorCurrentConfig.currentLimit = pidConfig.leftMotorPIDs.currentLimit

        motorCurrentConfig = phoenix6.configs.talon_fx_configs.CurrentLimitsConfigs()
        motorOuputConfig = phoenix6.configs.talon_fx_configs.MotorOutputConfigs()
        #motorOuputConfig.neutral_mode = 
        motorCurrentConfig.supply_current_limit = pidConfig.rightMotorPIDs.currentLimit

        leftMotorConfig.supplyCurrLimit = leftMotorCurrentConfig
        motorConfig.with_current_limits(motorCurrentConfig)

        motorConfig.with_feedback(motorFeedbackConfigs)

        self.leftMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.rightMotor.set_control(phoenix6.controls.CoastOut)

        self.rightMotor.set_control(self.rightMotorController.with_velocity(0))
        self.rightMotor.set_control(self.motorCoaster)
        #self.rightMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        
        self.leftMotor.configAllSettings(leftMotorConfig, 50)
        self.rightMotor.configurator.apply(motorConfig)
        #self.rightMotor.configAllSettings(rightMotorConfig, 50)

    def periodic (self):
        wpilib.SmartDashboard.putBoolean("Climber Limit Switch", self.limitSwitch.get())
        if not self.zeroed:
            if self.limitSwitch.get():
                self.leftMotor.set(phoenix5.ControlMode.PercentOutput, 0.0)
                self.rightMotor.set_control(self.rightMotorController.with_velocity(0))
                self.leftMotor.setSelectedSensorPosition(0.0, 0, 50)
                self.rightMotor.set_control(self.rightMotorController.with_position(self.targetValue/self.gearRatio))
                self.zeroed = True
            else:
                self.leftMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)
                self.rightMotor.set_control(self.rightMotorController.with_velocity(-0.2))
                #self.rightMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)
        else:
            self.rightMotor.set_control(self.rightMotorController.with_position(self.targetValue/self.gearRatio))

    def reZero(self):
        self.zeroed = False

    def setPosition(self):
        pass
