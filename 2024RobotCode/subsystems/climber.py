# haha we're using neos
import wpilib
from rev import _rev
import commands2
import RobotConfig


class ClimberSubsystem(commands2.Subsystem):

    #motorRatio = 4:1
    #zeroed = False

    def __init__(self):
        super().__init__()
        self.targetValue = 0
        self.leftSoleniod = wpilib.Solenoid(moduleType=wpilib.PneumaticsModuleType.CTREPCM, channel= 1)
        self.rightSoleniod = wpilib.Solenoid(moduleType= wpilib.PneumaticsModuleType.CTREPCM, channel= 0)
        self.encoderConversionFactor = 20 # this is just a temporary number need to find the real one
        self.gearRatio = 4 #gears are 4 to 1 so im assuming that this is four. will need to expierment with this to find the one inch of travel ratio
        self.config = RobotConfig
        #self.xboxController = xboxController
        #self.limitSwitch = wpilib.DigitalInput(self.config.Climber.limitSwitchID)
        self.rightMotor = _rev.CANSparkMax(self.config.Climber.rightMotorCanID, _rev.CANSparkMax.MotorType.kBrushless)
        self.leftMotor = _rev.CANSparkMax(self.config.Climber.leftMotorCanID, _rev.CANSparkMax.MotorType.kBrushless)

        self.rightMotor.restoreFactoryDefaults()
        self.leftMotor.restoreFactoryDefaults()
        
        self.rightMotor.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast)
        self.leftMotor.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast)
        
        self.rightEncoder = self.rightMotor.getEncoder()
        self.leftEncoder = self.leftMotor.getEncoder()
        self.rightEncoder.setPositionConversionFactor(self.encoderConversionFactor)
        self.leftEncoder.setPositionConversionFactor(self.encoderConversionFactor)
        
        self.rightPIDController = self.rightMotor.getPIDController()
        self.leftPIDController = self.leftMotor.getPIDController()
        self.rightPIDController.setFeedbackDevice(self.rightEncoder)
        self.leftPIDController.setFeedbackDevice(self.leftEncoder)

        self.rightPIDController.setP(self.config.climberPIDs.rightMotorPIDs.kP)
        self.rightPIDController.setI(self.config.climberPIDs.rightMotorPIDs.kI)
        self.rightPIDController.setD(self.config.climberPIDs.rightMotorPIDs.kD)
        self.rightPIDController.setFF(self.config.climberPIDs.rightMotorPIDs.kF)
        self.rightPIDController.setOutputRange(-1, 1)

        self.leftPIDController.setP(self.config.climberPIDs.leftMotorPIDs.kP)
        self.leftPIDController.setI(self.config.climberPIDs.leftMotorPIDs.kI)
        self.leftPIDController.setD(self.config.climberPIDs.leftMotorPIDs.kD)
        self.leftPIDController.setFF(self.config.climberPIDs.leftMotorPIDs.kF)
        self.leftPIDController.setOutputRange(-1, 1)

        self.rightMotor.setSmartCurrentLimit(50)
        self.leftMotor.setSmartCurrentLimit(50)

        self.rightMotor.burnFlash()
        self.leftMotor.burnFlash()
        self.desiredPosition = 0
        self.rightEncoder.setPosition(self.desiredPosition)
        self.leftEncoder.setPosition(self.desiredPosition)

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
        self.rightMotor.set(-0.1)
        self.leftMotor.set(0.1)
        pass
        

    def goUp(self):
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
        print("going up")

    def goDown(self):
        #self.Position -= 10.0
        #print(str(self.Position) + "from down")
        '''self.leftMotor.set_control(self.leftMotorController.with_output(self.Position))
        self.rightMotor.set_control(self.rightMotorController.with_output(self.Position))'''
        self.rightSoleniod.set(False)
        self.leftSoleniod.set(False)
        self.rightMotor.set(-0.5)
        self.leftMotor.set(0.5)
        print("going down")

    def getPosition(self):
        #print(self.Position)
        #self.Position = float(self.leftMotor.get_position())
        #return self.Position
        pass
    
    def stationary(self):
        '''self.rightMotor.set_control(phoenix6.controls.NeutralOut)
        self.leftMotor.set_control(self.leftMotorController.with_output(0))'''
        #self.Position = self.getPosition()
        self.rightMotor.setIdleMode(_rev.CANSparkBase.IdleMode.kCoast)
        self.rightMotor.set(0)
        self.leftMotor.setIdleMode(_rev.CANSparkBase.IdleMode.kCoast)
        self.leftMotor.set(0)

    def rightGoUp(self):
        self.rightSoleniod.set(True)
        self.rightMotor.set(0.5)

    def leftGoUp(self):
        self.leftSoleniod.set(True)
        self.leftMotor.set(-0.5)

    def rightGoDown(self):
        self.rightSoleniod.set(False)
        self.rightMotor.set(-0.5)

    def leftGoDown(self):
        self.leftSoleniod.set(False)
        self.leftMotor.set(0.5)

    def rightPreGoUp (self):
        self.rightMotor.set(-0.1)
        #self.leftMotor.set(0.1)
        pass

    def leftPreGoUp (self):
        #self.rightMotor.set(-0.1)
        self.leftMotor.set(0.1)
        pass

    

    '''def reZero(self):
        self.zeroed = False'''

    def setVelocity(self, kvelocity):
        self.rightMotor.set(kvelocity)
        self.leftMotor.set(kvelocity)