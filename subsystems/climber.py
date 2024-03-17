# haha we're using neos
import wpilib
from rev import _rev
import commands2
import RobotConfig

#note to self invert the LEFT motor

class ClimberSubsystem(commands2.Subsystem):

    #motorRatio = 4:1
    #zeroed = False

    def __init__(self, motorID: int, solenoidID: int, isReversed: bool):
        super().__init__()
        self.targetValue = 0
        self.isInverted = isReversed
        self.Soleniod = wpilib.Solenoid(moduleType=wpilib.PneumaticsModuleType.CTREPCM, channel= solenoidID)
        #self.rightSoleniod = wpilib.Solenoid(moduleType= wpilib.PneumaticsModuleType.CTREPCM, channel= 0)
        self.encoderConversionFactor = 20 # this is just a temporary number need to find the real one
        self.gearRatio = 4 #gears are 4 to 1 so im assuming that this is four. will need to expierment with this to find the one inch of travel ratio
        self.config = RobotConfig
        #self.xboxController = xboxController
        #self.limitSwitch = wpilib.DigitalInput(self.config.Climber.limitSwitchID)
        self.Motor = _rev.CANSparkMax(motorID, _rev.CANSparkMax.MotorType.kBrushless)
        #self.leftMotor = _rev.CANSparkMax(self.config.Climber.leftMotorCanID, _rev.CANSparkMax.MotorType.kBrushless)

        self.Motor.restoreFactoryDefaults()
        #self.leftMotor.restoreFactoryDefaults()
        
        self.Motor.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast)
        #self.leftMotor.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast)
        if self.isInverted == True:
            self.Motor.setInverted(True)
        
        self.Encoder = self.Motor.getEncoder()
        #self.leftEncoder = self.leftMotor.getEncoder()
        self.Encoder.setPositionConversionFactor(self.encoderConversionFactor)
        #self.leftEncoder.setPositionConversionFactor(self.encoderConversionFactor)
        
        self.PIDController = self.Motor.getPIDController()
        #self.leftPIDController = self.leftMotor.getPIDController()
        self.PIDController.setFeedbackDevice(self.Encoder)
        #self.leftPIDController.setFeedbackDevice(self.leftEncoder)

        self.PIDController.setP(self.config.climberPIDs.rightMotorPIDs.kP)
        self.PIDController.setI(self.config.climberPIDs.rightMotorPIDs.kI)
        self.PIDController.setD(self.config.climberPIDs.rightMotorPIDs.kD)
        self.PIDController.setFF(self.config.climberPIDs.rightMotorPIDs.kF)
        self.PIDController.setOutputRange(-1, 1)

        '''self.leftPIDController.setP(self.config.climberPIDs.leftMotorPIDs.kP)
        self.leftPIDController.setI(self.config.climberPIDs.leftMotorPIDs.kI)
        self.leftPIDController.setD(self.config.climberPIDs.leftMotorPIDs.kD)
        self.leftPIDController.setFF(self.config.climberPIDs.leftMotorPIDs.kF)
        self.leftPIDController.setOutputRange(-1, 1)'''

        self.Motor.setSmartCurrentLimit(50)
        #self.leftMotor.setSmartCurrentLimit(50)

        self.Motor.burnFlash()
        #self.leftMotor.burnFlash()
        self.desiredPosition = 0
        self.Encoder.setPosition(self.desiredPosition)
        #self.leftEncoder.setPosition(self.desiredPosition)

        # TODO add zeroing code
        '''if self.limitSwitch.get():
            self.leftMotor.set(0)
            self.rightMotor.set(0)
            self.zeroed = True
        
        else:
            self.leftMotor.set(-0.2)
            self.rightMotor.set(-0.2)'''

    def periodic (self):
        #wpilib.SmartDashboard.putBoolean("Climber Limit Switch", self.limitSwitch.get())
        #else:
        #self.rightMotor.set_control(self.request.with_position(self.targetValue * self.gearRatio))
        #self.leftMotorMotor.set_control(self.request.with_position(self.targetValue * self.gearRatio))
        pass

    def preGoUp (self):
        self.Motor.set(-0.1)
        #self.leftMotor.set(0.1)
        
        

    '''def goUp(self):
        #print (self.leftMotorController.with_velocity(10))
        # TODO add solenoid code
        #self.Position += 10.0
        #print (str(self.Position) + "from up")
        #self.rightMotor.set_control(self.rightMotorController.with_output(0.5))
        #self.rightMotor.set_control(self.rightMotorController.with_position(self.Position))
        #print(str(self.rightMotor.get_position))
        #self.rightMotor.set_control(self.rightMotorController.with_position(self.Position)) #assuming this is not too fast and positive is up
        
        self.rightSoleniod.set(True)
        self.leftSoleniod.set(True)
        print('setting solenoid')
        self.rightMotor.set(0.5) # assuming positive is up
        self.leftMotor.set(-0.5)
        print("going up")'''

    '''def goDown(self):
        #self.Position -= 10.0
        #print(str(self.Position) + "from down")
        self.leftMotor.set_control(self.leftMotorController.with_output(self.Position))
        self.rightMotor.set_control(self.rightMotorController.with_output(self.Position))
        self.rightSoleniod.set(False)
        self.leftSoleniod.set(False)
        self.rightMotor.set(-0.5)
        self.leftMotor.set(0.5)
        print("going down")'''

    def getPosition(self):
        #print(self.Position)
        #self.Position = float(self.leftMotor.get_position())
        #return self.Position
        pass
    
    def stationary(self):
        '''self.rightMotor.set_control(phoenix6.controls.NeutralOut)
        self.leftMotor.set_control(self.leftMotorController.with_output(0))'''
        #self.Position = self.getPosition()
        self.Motor.setIdleMode(_rev.CANSparkBase.IdleMode.kCoast)
        self.Motor.set(0)
        #self.leftMotor.setIdleMode(_rev.CANSparkBase.IdleMode.kCoast)
        #self.leftMotor.set(0)

    def goUp(self):
        self.Soleniod.set(True)
        self.Motor.set(0.5)

    '''def leftGoUp(self):
        self.leftSoleniod.set(True)
        self.leftMotor.set(-0.5)'''

    def goDown(self):
        self.Soleniod.set(False)
        self.Motor.set(-0.5)

    '''def leftGoDown(self):
        self.leftSoleniod.set(False)
        self.leftMotor.set(0.5)'''

    '''def PreGoUp (self):
        self.Motor.set(-0.1)
        #self.leftMotor.set(0.1)'''
        

    '''def leftPreGoUp (self):
        #self.rightMotor.set(-0.1)
        self.leftMotor.set(0.1)
        pass'''

    

    '''def reZero(self):
        self.zeroed = False'''

    def setVelocity(self, kvelocity):
        self.Motor.set(kvelocity)
        #self.leftMotor.set(kvelocity)
    '''def joystickControl(self, speed):
        if speed'''
