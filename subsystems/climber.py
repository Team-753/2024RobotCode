# assuming that we are using the krakens
import wpilib
import phoenix6
import commands2
import RobotConfig
from phoenix6 import controls

class ClimberSubsystem(commands2.Subsystem):

    #motorRatio = 4:1
    #zeroed = False

    def __init__(self):
        super().__init__()
        print("climber")
        self.targetValue = 0
        self.soleniod = wpilib.Solenoid()
        self.encoderConversionFactor = 2048 # this is just a temporary number need to find the real one
        self.gearRatio = 4 #gears are 4 to 1 so im assuming that this is four. will need to expierment with this to find the one inch of travel ratio
        self.config = RobotConfig
        #self.xboxController = xboxController
        self.limitSwitch = wpilib.DigitalInput(self.config.Climber.limitSwitchID)
        self.rightMotor = phoenix6.hardware.TalonFX(self.config.Climber.rightMotorCanID)
        self.rightMotorPIDController = phoenix6.controls.PositionVoltage(0)
        self.leftMotorPIDController = phoenix6.controls.PositionVoltage(0)
        self.rightMotorController = phoenix6.controls.DutyCycleOut(0)
        self.leftMotorController = phoenix6.controls.DutyCycleOut(0)
        self.motorCoaster = phoenix6.controls.CoastOut()
        self.leftMotor = phoenix6.hardware.TalonFX(self.config.Climber.leftMotorCanID)
        motorFeedbackConfigs = phoenix6.configs.talon_fx_configs.FeedbackConfigs()
        #motorFeedbackConfigs.feedback_sensor_source = 0 ## this breaks the code, i dont know why it doesnt work but it should just be redundant
        #self.rightMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        #self.leftMotor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.IntegratedSensor, 0, 50)
        motorConfig = phoenix6.configs.TalonFXConfiguration()
        #leftMotorConfig = phoenix5.TalonFXConfiguration()
        #motorConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
        #leftMotorConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
        pidConfig = self.config.climberPIDs

        '''leftMotorConfig.slot0.kP = pidConfig.leftMotorPIDs.kP
        leftMotorConfig.slot0.kI = pidConfig.leftMotorPIDs.kI
        leftMotorConfig.slot0.kD = pidConfig.leftMotorPIDs.kD
        leftMotorConfig.slot0.kP = pidConfig.leftMotorPIDs.kF
        leftMotorConfig.slot0.allowableClosedloopError = pidConfig.leftMotorPIDs.error
        leftMotorConfig.slot0.integralZone = pidConfig.leftMotorPIDs.izone'''

        motorConfig.slot0.k_p = pidConfig.rightMotorPIDs.kP
        motorConfig.slot0.k_i = pidConfig.rightMotorPIDs.kI
        motorConfig.slot0.k_d = pidConfig.rightMotorPIDs.kD
        motorConfig.slot0.k_v = pidConfig.rightMotorPIDs.kF
        '''rightMotorConfig.slot0.allowableClosedloopError = pidConfig.leftMotorPIDs.error
        rightMotorConfig.slot0.integralZone = pidConfig.rightMotorPIDs.izone'''

        '''leftMotorCurrentConfig = phoenix5.SupplyCurrentLimitConfiguration()
        leftMotorCurrentConfig.currentLimit = pidConfig.leftMotorPIDs.currentLimit'''

        motorCurrentConfig = phoenix6.configs.talon_fx_configs.CurrentLimitsConfigs()
        motorOuputConfig = phoenix6.configs.talon_fx_configs.MotorOutputConfigs()
        motorOuputConfig.neutral_mode = 0
        motorCurrentConfig.supply_current_limit = pidConfig.rightMotorPIDs.currentLimit

        #leftMotorConfig.supplyCurrLimit = leftMotorCurrentConfig
        motorConfig.with_current_limits(motorCurrentConfig)

        motorConfig.with_feedback(motorFeedbackConfigs)

        motorConfig.with_motor_output(motorOuputConfig)

        #self.leftMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        '''self.rightMotor.set_control(phoenix6.controls.CoastOut)
        self.leftMotor.set_control(phoenix6.controls.CoastOut)'''

        self.rightMotor.set_control(self.rightMotorController.with_output(0))
        self.rightMotor.set_control(self.motorCoaster)

        self.leftMotor.set_control(self.leftMotorController.with_output(0))
        self.leftMotor.set_control(self.motorCoaster)
        #self.rightMotor.setNeutralMode(phoenix5.NeutralMode.Brake)
        
        #self.leftMotor.configAllSettings(leftMotorConfig, 50)
        self.rightMotor.configurator.apply(motorConfig)
        self.leftMotor.configurator.apply(motorConfig)
        #self.rightMotor.configAllSettings(rightMotorConfig, 50)
        
        # trying something new here
        self.request = controls.PositionVoltage(0).with_slot(0)

        # TODO add zeroing code
        if self.limitSwitch.get():
            self.leftMotor.set_control(self.leftMotorController.with_output(0))
            self.rightMotor.set_control(self.rightMotorController.with_output(0))
            #self.leftMotor.set_control(self.leftMotorController.with_output(self.targetValue/self.gearRatio))
            #self.rightMotor.set_control(self.rightMotorController.with_output(self.targetValue/self.gearRatio))
            self.zeroed = True
        
        else:
            self.leftMotor.set_control(self.leftMotorController.with_output(0.2))
            self.rightMotor.set_control(self.rightMotorController.with_output(-0.2))
            #self.rightMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)''' 

    def periodic (self):
        wpilib.SmartDashboard.putBoolean("Climber Limit Switch", self.limitSwitch.get())
        '''if not self.zeroed:
           
            else:
                self.leftMotor.set_control(self.leftMotorController.with_velocity (-0.2))
                self.rightMotor.set_control(self.rightMotorController.with_velocity(-0.2))
                #self.rightMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)'''
        #else:
        self.rightMotor.set_control(self.request.with_position(self.targetValue * self.gearRatio))
        self.leftMotorMotor.set_control(self.request.with_position(self.targetValue * self.gearRatio))

    def goUp(self):
        #print (self.leftMotorController.with_velocity(10))
        # TODO add solenoid code
        #self.Position += 10.0
        #print (str(self.Position) + "from up")
        self.rightMotor.set_control(self.rightMotorController.with_output(0.5))
        #self.rightMotor.set_control(self.rightMotorController.with_position(self.Position))
        print(str(self.rightMotor.get_position))
        #self.rightMotor.set_control(self.rightMotorController.with_position(self.Position)) #assuming this is not too fast and positive is up

    def goDown(self):
        #self.Position -= 10.0
        #print(str(self.Position) + "from down")
        self.leftMotor.set_control(self.leftMotorController.with_output(self.Position))
        self.rightMotor.set_control(self.rightMotorController.with_output(self.Position))

    def getPosition(self):
        print(self.Position)
        #self.Position = float(self.leftMotor.get_position())
        return self.Position
    
    def stationary(self):
        self.rightMotor.set_control(phoenix6.controls.NeutralOut)
        self.leftMotor.set_control(self.leftMotorController.with_output(0))
        self.Position = self.getPosition()

    '''def reZero(self):
        self.zeroed = False'''

    def setPosition(self):
        pass
