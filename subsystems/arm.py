# Imports for arm.
import wpilib
import commands2
import RobotConfig
import rev
from rev import _rev

class ArmSubsystem(commands2.Subsystem):
    
    kMotorToArmDegrees = 360 / (2.5 * 80) # each rotation of the motor is 7.2 degrees
    kMotorToArmDegreeVelocity = kMotorToArmDegrees / 60 # each rotation of the motor is 7.2 degrees
    def __init__(self) -> None:
        """ This is ran once, it returns NOTHING """
        super().__init__()
        # Sets motors for arm commands
        self.leftArm = _rev.CANSparkMax(RobotConfig.Arm.leftMotorCanID, rev.CANSparkMax.MotorType.kBrushless)
        self.rightArm = _rev.CANSparkMax(RobotConfig.Arm.rightMotorCanID, _rev.CANSparkMax.MotorType.kBrushless)
        self.bottomLimit = wpilib.DigitalInput(RobotConfig.Arm.limitSwitch1RIO)
        self.topLimit = wpilib.DigitalInput(RobotConfig.Arm.limitSwitch2RIO)
        #self.rightArm.follow(self.leftArm, True)
        self.leftArm.restoreFactoryDefaults()
        self.leftArm.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast)
        self.leftEncoder = self.leftArm.getEncoder()
        self.leftEncoder.setPositionConversionFactor(self.kMotorToArmDegrees)
        self.leftEncoder.setVelocityConversionFactor(self.kMotorToArmDegreeVelocity)
        self.leftPIDController = self.leftArm.getPIDController()
        self.leftPIDController.setFeedbackDevice(self.leftEncoder)
        self.leftPIDController.setP(0.05)
        self.leftPIDController.setI(0)
        self.leftPIDController.setD(0)
        self.leftPIDController.setFF(0)
        self.leftPIDController.setOutputRange(-1,1)
        self.leftArm.setSmartCurrentLimit(60)
        self.leftArm.burnFlash()
        
        self.rightArm.restoreFactoryDefaults()
        self.rightArm.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast) # change to brake in final
        self.rightArm.setInverted(True)
        self.rightEncoder = self.rightArm.getEncoder()
        self.rightEncoder.setPositionConversionFactor(self.kMotorToArmDegrees)
        self.rightEncoder.setVelocityConversionFactor(self.kMotorToArmDegreeVelocity)
        self.rightPIDController = self.rightArm.getPIDController()
        self.rightPIDController.setFeedbackDevice(self.rightEncoder)
        self.rightPIDController.setP(0.05)
        self.rightPIDController.setI(0)
        self.rightPIDController.setD(0)
        self.rightPIDController.setFF(0)
        self.rightPIDController.setOutputRange(-1,1)
        self.rightArm.setSmartCurrentLimit(60)
        self.rightArm.burnFlash()
        
        self.desiredAngle = 0 # degrees above the floor, this is a arbitrary guess
        self.leftEncoder.setPosition(self.desiredAngle)
        self.rightEncoder.setPosition(self.desiredAngle)
        
    def periodic(self) -> None:
        # updates the PID controllers to go to the wanted position
        self.leftPIDController.setReference(self.desiredAngle, _rev.CANSparkMax.ControlType.kPosition)
        self.rightPIDController.setReference(self.desiredAngle, _rev.CANSparkMax.ControlType.kPosition)
        
        wpilib.SmartDashboard.putNumber("Left Motor Angle Degrees: ", self.leftEncoder.getPosition())
        wpilib.SmartDashboard.putNumber("Right Motor Angle Degrees: ", self.rightEncoder.getPosition())
        if(self.bottomLimit.get()):
            #self.stop()
            wpilib.SmartDashboard.putBoolean("Bottom Limit", True)
            #pass
        elif(self.topLimit.get()):
            #self.stop()
            wpilib.SmartDashboard.putBoolean("Top Limit", True)
            #pass
    def setDesiredAngle(self, kDesiredAngle: float):
        self.desiredAngle = kDesiredAngle
        print(kDesiredAngle)
    '''
    def __init__(self):
        super().__init__()
        #initialized
        self.right = rev.CANSparkMax(RobotConfig.Arm.rightMotorCanID, _rev.CANSparkMax.MotorType.kBrushless)
        self.leftArm = rev.CANSparkMax(RobotConfig.Arm.leftMotorCanID, _rev.CANSparkMax.MotorType.kBrushless)
        #leftEncoder = self.left.getEncoder()
        #self.right.follow(self.left, True)
    def periodic(self) -> None:
        ''''''
        # print(f"Left Motor Position: {self.leftEncoder.getPosition()}")
        # print(f"Left Motor Voltage: {self.leftArm.getBusVoltage()}")
    def onA(self):
        print("Running arm motors")
        self.leftArm.set(1)
        #self.right.set(-1)
    def onB(self):
        self.leftArm.set(-0.5)
    '''
    def stop(self):
        print("stopping arm motors")
        self.leftArm.set(0)
