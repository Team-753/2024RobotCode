import rev
from wpimath import kinematics, geometry
import math
import wpilib

class SwerveModule:
    
    countsPerRotation = 2048
    wheelDiameter = 0.0762
    drivingGearRatio = 1
    turningGearRatio = 1
    motorEncoderConversionFactor = 1
    wheelVelocityThreshold = 0.1
    
    def __init__(self, config: dict, moduleName: str ) -> None:
        self.driveMotor = rev.CANSparkMax(config["driveMotorID"], rev._rev.CANSparkLowLevel.MotorType.kBrushless) # defines the motor that drives the wheel, will need to be changed if we get krakens
        self.turnMotor = rev.CANSparkMax(config["turnMotorID"], rev._rev.CANSparkLowLevel.MotorType.kBrushless) # defines the motor that turns the wheel
        wpilib.AnalogInput(config["encoderID"]).setSampleRate(125)
        self.absoluteEncoder = wpilib.AnalogEncoder(config['encoderID'])
        self.encoderOffeset = config["encoderOffest"]
        self.turningGearRatio = 1
        self.drivingGearRatio = 1
        self.driveMotor.getEncoder (rev._rev.CANSparkBase, rev._rev.SparkMaxRelativeEncoder.Type, countsPerRev = 42)
        self.turnMotor.getEncoder (rev._rev.CANSparkBase, rev._rev.SparkMaxRelativeEncoder.Type, countsPerRev = 42)
        self.driveMotor.setIdleMode (rev._rev.CANSparkBase.IdleMode.kCoast)
        self.turnMotor.setIdleMode (rev._rev.CANSparkBase.IdleMode.kCoast)
        
    def getAbsolutePositionRadians (self):
        return (self.turnMotor.TelemetryID.kPosition * math.tau)
    
    def getWheelAngleRadians (self):
        adjustedRelValueDegrees = ((self.turnMotor.TelemetryID.kPosition % (self.countsPerRotation * self.turningGearRatio))* math.tau) / (self.countsPerRotation * self.turningGearRatio) # might not return the number of spins of the motor, might be the point in the wheel rotation that we're at
        return adjustedRelValueDegrees 
   
    def getTurnWheelState (self):
        return geometry.Rotation2d(self.getWheelAngleRadians())

    def getSwerveModulePosition(self):
        distanceMeters = self.turnMotor.TelemetryID.kPosition * self.wheelDiameter * math.pi / (self.countsPerRotation * self.drivingGearRatio)
        angle = self.getTurnWheelState()
        return kinematics.SwerveModulePosition(distanceMeters, angle)

    def getSwerveModuleState (self):
        velocityMetersPerSecond = (self.driveMotor.TelemetryID.kVelocity * 10 * self.wheelDiameter * math.pi) / (self.countsPerRotation * self.drivingGearRatio)
        angle = self.getTurnWheelState()
        return kinematics.SwerveModuleState(velocityMetersPerSecond, angle)

    def setStateTurnOnly(self, desiredStateAngle):

        desiredAngleRadians = angle.radians()
        if desiredStateAngle > 0:
            desiredStateAngle -= math.pi
        else:
            desiredStateAngle += math.pi
        
        angle = geometry.Rotation2d(math.radians(desiredStateAngle))
        if desiredAngleRadians < 0:
            desiredAngleRadians += math.tau
        motorEncoderTickTarget = (self.turnMotor.TelemetryID.kPosition - (self.turnMotor.TelemetryID.kPosition() % (self.countsPerRotation * self.turningGearRatio))) + desiredAngleRadians * self.countsPerRotation * self.turningGearRatio / math.tau
        self.turnMotor.set (rev.CANSparkLowLevel.ControlType.kPosition, motorEncoderTickTarget)
        

    def setState (self, state: kinematics.SwerveModuleState): 
        state = kinematics.SwerveModuleState.optimize (state)
        desiredStateAngle = state.angle()
        #state.angle.rotateBy(geometry.Rotation2d(math.pi)) Migt be worth testing, but I don't know what's happening here
        if desiredStateAngle > 0:
            desiredStateAngle -= math.pi
        else:
            desiredStateAngle += math.pi
        state.angle = geometry.Rotation2d(desiredStateAngle)
        if abs(state.speed) < self.wheelVelocityThreshold:
            self.driveMotor.set(rev.CANSparkLowLevel.ControlType.kVelocity, 0)
            self.driveMotor.setIdleMode(rev._rev.CANSparkBase.setIdleMode)
        else:
            velocity = (state.speed * self.drivingGearRatio * self.countsPerRotation) / (self.wheelDiameter * math.pi * 10) # make sure that this is the correct number of ticks per secs
            self.driveMotor.set(rev._rev.CANSparkLowLevel.ControlType.kVelocity, velocity)
        
        desiredAngleRadians = state.angle
        if desiredAngleRadians < 0:
            desiredAngleRadians += math.tau
        motorEncoderTickTarget = (self.turnMotor.TelemetryID.kPosition() - (self.turnMotor.TelemetryID.kPosition() % (self.countsPerRotation * self.turningGearRatio))) + desiredAngleRadians * self.countsPerRotation * self.turningGearRatio / math.tau
        self.turnMotor.set(rev._rev.CANSparkLowLevel.ControlType.kPosition, motorEncoderTickTarget)
        
    def setNeutralMode (self, mode):
        self.driveMotor.setIdleMode (mode)
        self.turnMotor.setIdleMode (mode)

    def stop (self):
        self.driveMotor.set(rev._rev.CANSparkLowLevel.ControlType.kVoltage, 0)
        self.turnMotor.set(rev._rev.CANSparkLowLevel.ControlType.kVoltage, 0)

    '''def reZeroMotors (self):
        self.driveMotor.set (rev._rev.CAN)
        self.turnMotor.set ()'''
