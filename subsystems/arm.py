# Imports for arm.
import wpilib
import commands2
import RobotConfig
from RobotConfig import armConstants
from RobotConfig import DriveConstants
import rev
from rev import _rev
import wpimath
from wpimath import kinematics
"""Needed?^"""
class ArmSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        """ This is ran once, it returns NOTHING """
        super().__init__()
        # Sets motors for arm commands
        self.leftArm = rev.CANSparkMax(RobotConfig.Arm.leftMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        self.rightArm = rev.CANSparkMax(RobotConfig.Arm.rightMotorCanID, _rev.CANSparkLowLevel.MotorType.kBrushless)
        # Sets XBOX controller
        self.auxControl = wpilib.XboxController(DriveConstants.XBOX.USB_ID)
    def periodic(self) -> None:
        # TODO: Get XBOX control response to set arm. Add this to the "self.rightArm"
        def function(button):
            # TODO: Add code here
            # Do something based on button
            pass
        self.auxControl.A(function("A"))
        self.auxControl.B(function("B"))
        self.auxControl.X(function("X"))
        self.auxControl.Y(function("Y"))
        # Inverts and controls left arm motor based on what right arm is doing.
        self.rightArm
        self.leftArm.follow(self.rightArm, True)
        """ Put code you want to be looped in here. Nothing is returned here either."""
        return super().periodic()
    