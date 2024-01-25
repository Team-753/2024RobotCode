import commands2

class DriveTrainSubsystem(commands2.Subsystem):
    stateStdDevs = 0.1, 0.1, 0.1
    visionMeasurementStdDevs = 0.9, 0.9, 0.9 * math.pi
    
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config # inhereting the robot config json from the robot container