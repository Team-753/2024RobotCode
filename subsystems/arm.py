# Imports for arm.
import wpilib
import commands2
import RobotConfig
import rev
from rev import _rev

class ArmSubsystem(commands2.Subsystem):
    kMotorToArmDegrees = 360 / (2.5 * 20) # each rotation of the motor is 7.2 degrees
    kMotorToArmDegreeVelocity = kMotorToArmDegrees / 60 # each rotation of the motor is 7.2 degrees
    def __init__(self) -> None:
        """ This is ran once, it returns NOTHING """
        super().__init__()
        # Sets motors for arm commands
        self.leftArm = rev.CANSparkMax(RobotConfig.Arm.leftMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        self.rightArm = rev.CANSparkMax(RobotConfig.Arm.rightMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        
        self.leftArm.restoreFactoryDefaults()
        self.leftArm.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast)
        self.leftEncoder = self.leftArm.getEncoder()
        self.leftEncoder.setPositionConversionFactor(self.kMotorToArmDegrees)
        self.leftEncoder.setVelocityConversionFactor(self.kMotorToArmDegreeVelocity)
        self.leftPIDController = self.leftArm.getPIDController()
        self.leftPIDController.setFeedbackDevice(self.leftEncoder)
        self.leftPIDController.setP(0.1)
        self.leftPIDController.setI(0)
        self.leftPIDController.setD(0)
        self.leftPIDController.setFF(0)
        self.leftPIDController.setOutputRange(-1,1)
        self.leftArm.setSmartCurrentLimit(35)
        self.leftArm.burnFlash()
        
        self.rightArm.restoreFactoryDefaults()
        self.rightArm.setIdleMode(_rev.CANSparkMax.IdleMode.kCoast) # change to brake in final
        self.rightArm.setInverted(True)
        self.rightEncoder = self.rightArm.getEncoder()
        self.rightEncoder.setPositionConversionFactor(self.kMotorToArmDegrees)
        self.rightEncoder.setVelocityConversionFactor(self.kMotorToArmDegreeVelocity)
        self.rightPIDController = self.rightArm.getPIDController()
        self.rightPIDController.setFeedbackDevice(self.rightEncoder)
        self.rightPIDController.setP(0.1)
        self.rightPIDController.setI(0)
        self.rightPIDController.setD(0)
        self.rightPIDController.setFF(0)
        self.rightPIDController.setOutputRange(-1,1)
        self.rightArm.setSmartCurrentLimit(35)
        self.rightArm.burnFlash()
        
        self.desiredAngle = 5 # degrees above the floor, this is a arbitrary guess
        self.leftEncoder.setPosition(self.desiredAngle / self.kMotorToArmDegrees)
        self.rightEncoder.setPosition(self.desiredAngle / self.kMotorToArmDegrees)
        
    def periodic(self) -> None:
        # updates the PID controllers to go to the wanted position
        '''self.leftPIDController.setReference(self.desiredAngle, _rev.CANSparkMax.ControlType.kPosition)
        self.rightPIDController.setReference(self.desiredAngle, _rev.CANSparkMax.ControlType.kPosition)'''
        
        wpilib.SmartDashboard.putNumber("Left Motor Angle Degrees: ", self.leftEncoder.getPosition())
        wpilib.SmartDashboard.putNumber("Right Motor Angle Degrees: ", self.rightEncoder.getPosition())
    
    def setDesiredAngle(self, kDesiredAngle: float):
        self.desiredAngle = kDesiredAngle

    