import rev
from wpimath import kinematics, geometry
import math
from rev import _rev


class SwerveModule:
    """ The Swerve Module class. Pretty much all the code here was directly translated from the following github: 
    https://github.com/REVrobotics/MAXSwerve-Java-Template/blob/main/src/main/java/frc/robot/subsystems/MAXSwerveModule.java """
    
    kWheelDiameterMeters = 0.0762
    kDrivingMotorPinionTeeth = 14
    kDrivingMotorReduction = (45 * 22) / (kDrivingMotorPinionTeeth * 15)
    kDrivingEncoderPositionFactor = (kWheelDiameterMeters * math.pi) / kDrivingMotorReduction # meters
    kDrivingEncoderVelocityFactor = ((kWheelDiameterMeters * math.pi) / kDrivingMotorReduction) / 60 # meters per second
    
    kTurningEncoderPositionFactor = math.tau # radians
    kTurningEncoderVelocityFactor = math.tau / 60 # radians per second
    
    def __init__(self, config) -> None:
        
        # creating an empty, default desired state
        self.desiredState = kinematics.SwerveModuleState(0.0, geometry.Rotation2d())
        
        # initializing main motors
        self.driveMotor = _rev.CANSparkMax(config.driveMotorID, _rev.CANSparkLowLevel.MotorType.kBrushless) # defines the motor that drives the wheel, will need to be changed if we get krakens
        self.turnMotor = _rev.CANSparkMax(config.turnMotorID, _rev.CANSparkLowLevel.MotorType.kBrushless) # defines the motor that turns the wheel
        
        # Factory reset, just in case a motor or module is swapped out
        self.driveMotor.restoreFactoryDefaults()
        self.turnMotor.restoreFactoryDefaults()
        
        # Setup encoders and PID controllers for the driving and turning SPARK MAX(s)
        self.drivingEncoder = self.driveMotor.getEncoder()
        self.turningEncoder = self.turnMotor.getAbsoluteEncoder(_rev.SparkAbsoluteEncoder.Type.kDutyCycle)
        self.drivingPIDController = self.driveMotor.getPIDController()
        self.turningPIDController = self.turnMotor.getPIDController()
        self.drivingPIDController.setFeedbackDevice(self.drivingEncoder)
        self.turningPIDController.setFeedbackDevice(self.turningEncoder)
        
        """        
        Apply position and velocity conversion factors for the driving encoder. 
        The native units for position and velocity are rotations and RPM, respectively,
        but we want meters and meters per second to use with WPILib's swerve APIs.
        """
        
        self.drivingEncoder.setPositionConversionFactor(self.kDrivingEncoderPositionFactor)
        self.drivingEncoder.setVelocityConversionFactor(self.kDrivingEncoderVelocityFactor)
        
        """
        Apply position and velocity conversion factors for the turning encoder. 
        We want these in radians and radians per second to use with WPILib's swerve APIs.
        """
        
        self.turningEncoder.setPositionConversionFactor(self.kTurningEncoderPositionFactor)
        self.turningEncoder.setVelocityConversionFactor(self.kTurningEncoderVelocityFactor)
        
        """
        Invert the turning encoder, since the output shaft rotates in the opposite direction of
        the steering motor in the MAXSwerve Module.
        """
        
        self.turningEncoder.setInverted(True)
        
        """
        Enable PID wrap around for the turning motor. This will allow the PID
        controller to go through 0 to get to the setpoint i.e. going from 350 degrees
        to 10 degrees will go through 0 rather than the other direction which is a longer route.
        """
        
        self.turningPIDController.setPositionPIDWrappingEnabled(True)
        self.turningPIDController.setPositionPIDWrappingMinInput(0) # radians
        self.turningPIDController.setPositionPIDWrappingMaxInput(self.kTurningEncoderPositionFactor) # radians
        
        """
        Set the PID gains for the driving motor. These are example PID gains and actual values will need to be obtained from testing.
        """
        
        self.drivingPIDController.setP(0.04)
        self.drivingPIDController.setI(0)
        self.drivingPIDController.setD(0)
        self.drivingPIDController.setFF(1)
        self.drivingPIDController.setOutputRange(-1, 1)
        
        """
        Set the PID gains for the turning motor. These are example PID gains and actual values will need to be obtained from testing.
        """
        
        self.turningPIDController.setP(1)
        self.turningPIDController.setI(0)
        self.turningPIDController.setD(0)
        self.turningPIDController.setFF(0)
        self.turningPIDController.setOutputRange(-1, 1)
        
        # additional tuning of settings.
        
        self.driveMotor.setIdleMode(_rev.CANSparkBase.IdleMode.kCoast)
        self.turnMotor.setIdleMode(_rev.CANSparkBase.IdleMode.kCoast)
        self.driveMotor.setSmartCurrentLimit(50) # amps
        self.turnMotor.setSmartCurrentLimit(20) # amps
        
        """
        Save the SPARK MAX configurations. If a SPARK MAX browns out during
        operation, it will maintain the above configurations.
        """
        
        self.driveMotor.burnFlash()
        self.turnMotor.burnFlash()
        
        # setting the angle in radians   
        self.desiredState.angle = geometry.Rotation2d(self.turningEncoder.getPosition()) 
        
    def getState(self) -> kinematics.SwerveModuleState:
        """ Returns the current state of the module. """
        return kinematics.SwerveModuleState(self.drivingEncoder.getVelocity(),
                                            geometry.Rotation2d(self.turningEncoder.getPosition()))
        
    def getPosition(self) -> kinematics.SwerveModulePosition:
        """ Returns the current position of the module for autonomous tracking. """
        return kinematics.SwerveModulePosition(self.drivingEncoder.getPosition(),
                                               geometry.Rotation2d(self.turningEncoder.getPosition()))
        
    def setState(self, desiredState: kinematics.SwerveModuleState) -> None:
        """ Sets the swerve module's desired state. """
        
        # Optimize the reference state to avoid spinning further than 90 degrees.
        optimizedDesiredState = kinematics.SwerveModuleState.optimize(desiredState, 
                                                                      geometry.Rotation2d(self.turningEncoder.getPosition()))
        # Command driving and turning SPARKS MAX towards their respective setpoints.
        self.drivingPIDController.setReference(optimizedDesiredState.speed, _rev.CANSparkMax.ControlType.kVelocity)
        self.turningPIDController.setReference(optimizedDesiredState.angle.radians(), _rev.CANSparkMax.ControlType.kPosition)
        self.desiredState = desiredState
        
    def resetEncoders(self) -> None:
        """ Resets the driving encoder position, useful for testing multiple autos. """
        self.drivingEncoder.setPosition(0)
        
    '''def getAbsolutePositionRadians (self):
        return (self.turnMotor.TelemetryID.kPosition * math.tau)
    
    def getWheelAngleRadians (self):
        adjustedRelValueDegrees = ((self.turnMotor.TelemetryID.kPosition % (self.countsPerRotation * self.turningGearRatio))* math.tau) / (self.countsPerRotation * self.turningGearRatio) # might not return the number of spins of the motor, might be the point in the wheel rotation that we're at
        return adjustedRelValueDegrees '''
   
    '''def getTurnWheelState (self):
        return geometry.Rotation2d(self.getWheelAngleRadians())

    def getSwerveModulePosition(self):
        distanceMeters = self.turnMotor.TelemetryID.kPosition * self.wheelDiameter * math.pi / (self.countsPerRotation * self.drivingGearRatio)
        angle = self.getTurnWheelState()
        return kinematics.SwerveModulePosition(distanceMeters, angle)'''

    '''def getSwerveModuleState (self):
        velocityMetersPerSecond = (self.driveMotor.TelemetryID.kVelocity * 10 * self.wheelDiameter * math.pi) / (self.countsPerRotation * self.drivingGearRatio)
        angle = self.getTurnWheelState()
        return kinematics.SwerveModuleState(velocityMetersPerSecond, angle)

    def setStateTurnOnly(self, desiredStateAngle):

        desiredAngleRadians = angle
        if desiredStateAngle > 0:
            desiredStateAngle -= math.pi
        else:
            desiredStateAngle += math.pi
        
        angle = geometry.Rotation2d(math.radians(desiredStateAngle))
        if desiredAngleRadians < 0:
            desiredAngleRadians += math.tau
        motorEncoderTickTarget = (self.turnMotor.TelemetryID.kPosition - (self.turnMotor.TelemetryID.kPosition() % (self.countsPerRotation * self.turningGearRatio))) + desiredAngleRadians * self.countsPerRotation * self.turningGearRatio / math.tau
        self.turnMotor.set (_rev.CANSparkLowLevel.ControlType.kPosition, motorEncoderTickTarget)
        

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
        self.turnMotor.set(rev._rev.CANSparkLowLevel.ControlType.kPosition, motorEncoderTickTarget)'''
        
    def setNeutralMode (self, mode):
        self.driveMotor.setIdleMode (mode)
        self.turnMotor.setIdleMode (mode)

    def stop (self):
        self.driveMotor.set(_rev.CANSparkLowLevel.ControlType.kVoltage, 0)
        self.turnMotor.set(_rev.CANSparkLowLevel.ControlType.kVoltage, 0)

    '''def reZeroMotors (self):
        self.driveMotor.set (rev._rev.CAN)
        self.turnMotor.set ()'''
