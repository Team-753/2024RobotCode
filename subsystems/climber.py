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
        self.leftSoleniod = wpilib.Solenoid(moduleType=wpilib.PneumaticsModuleType.REVPH, channel= 0)
        self.rightSoleniod = wpilib.Solenoid(moduleType= wpilib.PneumaticsModuleType.REVPH, channel= 1)
        self.encoderConversionFactor = 2048 # this is just a temporary number need to find the real one
        self.gearRatio = 4 #gears are 4 to 1 so im assuming that this is four. will need to expierment with this to find the one inch of travel ratio
        self.config = RobotConfig
        #self.xboxController = xboxController
        self.limitSwitch = wpilib.DigitalInput(self.config.Climber.limitSwitchID)
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

        self.rightMotor.setSmartCurrentLimit(35)
        self.leftMotor.setSmartCurrentLimit(35)

        self.rightMotor.burnFlash()
        self.leftMotor.burnFlash()
        self.desiredPosition = 0
        self.rightEncoder.setPosition(self.desiredPosition)
        self.leftEncoder.setPosition(self.desiredPosition)

        # TODO add zeroing code
        if self.limitSwitch.get():
            #self.leftMotor.set_control(self.leftMotorController.with_output(0))
            #self.rightMotor.set_control(self.rightMotorController.with_output(0))
            #self.leftMotor.set_control(self.leftMotorController.with_output(self.targetValue/self.gearRatio))
            #self.rightMotor.set_control(self.rightMotorController.with_output(self.targetValue/self.gearRatio))
            self.zeroed = True
        
        else:
            #self.leftMotor.set_control(self.leftMotorController.with_output(0.2))
            #self.rightMotor.set_control(self.rightMotorController.with_output(-0.2))
            #self.rightMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)''' 
            pass

    def periodic (self):
        wpilib.SmartDashboard.putBoolean("Climber Limit Switch", self.limitSwitch.get())
        '''if not self.zeroed:
           
            else:
                self.leftMotor.set_control(self.leftMotorController.with_velocity (-0.2))
                self.rightMotor.set_control(self.rightMotorController.with_velocity(-0.2))
                #self.rightMotor.set(phoenix5.ControlMode.PercentOutput, -0.2)'''
        #else:
        #self.rightMotor.set_control(self.request.with_position(self.targetValue * self.gearRatio))
        #self.leftMotorMotor.set_control(self.request.with_position(self.targetValue * self.gearRatio))

    def goUp(self):
        #print (self.leftMotorController.with_velocity(10))
        # TODO add solenoid code
        #self.Position += 10.0
        #print (str(self.Position) + "from up")
        #self.rightMotor.set_control(self.rightMotorController.with_output(0.5))
        #self.rightMotor.set_control(self.rightMotorController.with_position(self.Position))
        #print(str(self.rightMotor.get_position))
        #self.rightMotor.set_control(self.rightMotorController.with_position(self.Position)) #assuming this is not too fast and positive is up
        self.leftSoleniod.set(True)
        self.rightSoleniod.set(True)
        self.rightMotor.set(0.5) # assuming positive is up
        self.leftMotor.set(0.5)
        self.leftSoleniod.set(False)
        self.rightSoleniod.set(False)
        print("going up")

    def goDown(self):
        #self.Position -= 10.0
        #print(str(self.Position) + "from down")
        '''self.leftMotor.set_control(self.leftMotorController.with_output(self.Position))
        self.rightMotor.set_control(self.rightMotorController.with_output(self.Position))'''
        self.rightMotor.set(-0.5)
        self.leftMotor.set(-0.5)
        print("going down")

    def getPosition(self):
        print(self.Position)
        #self.Position = float(self.leftMotor.get_position())
        return self.Position
    
    def stationary(self):
        '''self.rightMotor.set_control(phoenix6.controls.NeutralOut)
        self.leftMotor.set_control(self.leftMotorController.with_output(0))'''
        self.Position = self.getPosition()

    '''def reZero(self):
        self.zeroed = False'''

    def setPosition(self):
        pass
