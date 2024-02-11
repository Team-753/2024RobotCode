from wpimath import geometry

class RobotDimensions:
    trackWidth = 0.5715
    wheelBase = 0.5969

class SwerveModules:
    class frontLeft:
        driveMotorID = 1
        turnMotorID = 2
        
    class frontRight:
        driveMotorID = 3
        turnMotorID = 4
        
    class rearRight:
        driveMotorID = 5
        turnMotorID = 6
        
    class rearLeft:
        driveMotorID = 7
        turnMotorID = 8

class Arm:
    leftMotorCanID = 9
    rightMotorCanID = 10
    limitSwitch1RIO = 0
    limitSwitch2RIO = 1

class DriveConstants:
    class Joystick:
        USB_ID = 0
        xDeadband = 0.1
        yDeadband = 0.1
        thetaDeadband = 0.15
    class XBOX:
        USB_ID = 1
        # TODO: Add needed information  
    class RobotSpeeds:
        maxSpeed = 4.8
        maxAcceleration = 4
        manualRotationSpeedFactor = 1
        
    class PoseConstants:
        class translationPIDConstants:
            kP = 5.0
            kI = 0.0
            kD = 0.0
            period = 0.025
            
        class rotationPIDConstants:
            kP = 1.0
            kI = 0.0
            kD = 0.0
            period = 0.025
            
        xPoseToleranceMeters = 0.05
        yPoseToleranceMeters = 0.05
        thetaPoseToleranceRadians = 0.01745
        teleopVelLimit = 4.25
        teleopAccelLimit = 3
        
    class thetaPIDConstants:
        autoVelLimit = 2
        autoAccelLimit = 2
        xPoseToleranceMeters = 0.03
        yPoseToleranceMeters = 0.03
        thetaPoseToleranceRadians = 0.004363
        class translationPIDConstants:
            kP = 3.0
            kI = 0.0
            kD = 0.0
            period = 0.05

class FieldConstants:
    fieldWidthMeters = 16.54
    fieldLengthMeters = 8.21
    speakerYMeters = 5.548
    speakerZMeters = 2.05
    speakerXMeters = 0.225
class armConstants:
    Speaker = 80
    Amp = 90
    Home = 5
    Source = 70
class grabber:
    bottomMotorCANID = 11
    topMotorCANID = 12
    intake = -0.5
    outtake = 0.5
    idle = 0
    sensorDIOID = 3