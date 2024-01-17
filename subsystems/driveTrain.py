import commands2

class DriveTrainSubsystem(commands2.Subsystem):
    
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config # inhereting the robot config json from the robot container