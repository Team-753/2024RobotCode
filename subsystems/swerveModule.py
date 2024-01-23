import rev
from wpimath import kinematics, geometry
import math
import wpilib

'''Things to do:
Get gear ratios
MAKE SURE WE USE THE THRIFTYBOT ENCODERS OR REPLACE ENCODER TICKS VALUES!!!
figure out tick ratios
get wheel diameters
make sure all numbers are in meters

driving gear teeth: 66ish
turning gear teeth: 12.8
wheel diameter: 0.0762
encoder ticks: 2048'''

class SwerveModule:
    
    countsPerRotation = 2048
    wheelDiameter = 0.0762
    
    def __init__(self, config: dict, moduleName: str ) -> None:
        self.driveMotor = rev.CANSparkMax(config["drivemotorID"], rev._rev.CANSparkLowLevel.MotorType.kBrushless) # defines the motor that drives the wheel, will need to be changed if we get krakens
        self.turnMotor = rev.CANSparkMax(config["turnmotorID"], rev._rev.CANSparkLowLevel.MotorType.kBrushless) # defines the motor that turns the wheel
        wpilib.AnalogInput(config["encoderID"]).setSampleRate(125)
        self.absoluteEncoder = wpilib.AnalogEncoder(config['encoderID'])
        self.encoderOffeset = config["encoderOffest"]
        self.turningGearRatio = 1
        self.drivingGearRatio = 1



    def getAbsolutePositionRadians (self):
        return (self.absoluteEncoder() * math.tau)
    
    def getWheelAngleRadians (self):
        adjustedRelValueDegrees = ((self.absoluteEncoder.getAbsolutePosition() % (self.countsPerRotation * self.turningGearRatio))* math.tau) / (self.countsPerRotation * self.turningGearRatio) # might not return the number of spins of the motor, might be the point in the wheel rotation that we're at
        return adjustedRelValueDegrees 
   
    def getTurnWheelState (self):
        return geometry.Rotation2d(self.getWheelAngleRadians())

    def getSwerveModulePosition(self):
        distanceMeters = self.absoluteEncoder.getAbsolutePosition() * self.wheelDiameter * math.pi / (self.countsPerRotation * self.drivingGearRatio)
        angle = self.getTurnWheelState()
        return kinematics.SwerveModulePosition(distanceMeters, angle)

    def getSwerveModuleState (self):
        velocityMetersPerSecond = (self.absoluteEncoder() * 10 * self.wheelDiameter * math.pi) / (self.countsPerRotation * self.drivingGearRatio)
        angle = self.getTurnWheelState()
        return kinematics.SwerveModuleState(velocityMetersPerSecond, angle)

    def setStateTurnOnly(self, desiredStateAngle):
        

    def setState (self, state: kinematics.SwerveModuleState): 
        state = kinematics.SwerveModuleState.optimize (state)
        state.angle.rotateBy(geometry.Rotation2d(math.pi))
        velocity = state.speed 