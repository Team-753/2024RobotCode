
from pathplannerlib import PathPlannerTrajectory
import commands
from subsystems.swerveModule import PoseEstimatorSubsystem
from subsystems.driveTrain import DriveTrainSubSystem
from wpilib import DriverStation
from wpimath import geometry
import commands2
from commands2 import cmd
from typing import List
import math
class SwerveAutoBuilder:
    fieldWidthMeters = 0 # I will change this when I look back through the rule book to check what it is

    def __init__(self, poseEstimator: PoseEstimatorSubsystem, 
                 driveTrain: DriveTrainSubSystem,
                 eventMap: dict, 
                 useAllianceColor: bool, # In case you dont't know what a bool is it's true or false basicly
                 translationConstants: dict, 
                 rotationConstants: List,  
                 tolerance: geometry.Pose2d) -> None:
        self.eventMap = eventMap
        self.useAllianceColor = useAllianceColor
        self.poseEstimator = poseEstimator
        self.driveTrain = driveTrain
        self.translationConstants = translationConstants
        self.rotationConstants = rotationConstants
        self.tolerance = tolerance
    
    def followPathGroup(self, pathGroup: List[PathPlannerTrajectory]):
        commands = []

        for trajectory in pathGroup:
            commands.append(self.followPath(trajectory))

        return cmd.sequence(commands)
    
    def followPathGroupWithEvents(self, pathGroup: List[PathPlannerTrajectory]):
        commands = []

        for trajectory in pathGroup:
            commands.append(self.followPathWithEvents(trajectory))

        return cmd.sequence(commands)
    
    def resetPose(self, trajectory: PathPlannerTrajectory):

        return cmd.runOnce(lambda: self.__rPCmd(trajectory), [self.poseEstimator])
    
    def __rPCmd(self, trajectory: PathPlannerTrajectory):
        initialState = trajectory.getInitialState()

        if (self.useAllianceColor):
            initialState = PathPlannerTrajectory.transformStateForAlliance(initialState, DriverStation.getAlliance())

        self.poseEstimator.setCurrentPose(geometry.Pose2d(initialState.pose.translation(), initialState.holonomicRotation))
        
    def wrappedEventCommand(self, eventCommand: commands2.Command) -> commands2.Temporary: # Ignore the temporary for now I will fix it later
        requirements: List[commands2.Subsystem] = eventCommand.getRequirements()

        return commands2.FunctionalCommand(
            eventCommand.initialize(),
            eventCommand.execute(),
            eventCommand.end(False),
            eventCommand.isFinished(),
            []
        )
    
    def getStopEventCommands(self, stopEvent: PathPlannerTrajectory.StopEvent) -> commands2.Temporary:
        commands = []
        
        startIndex = 1 if stopEvent.executionBehavior == PathPlannerTrajectory.StopEvent.ExecutionBehavior.PARALLEL_DEADLINE else 0
        while startIndex < len(stopEvent.names):
            name = stopEvent.names[startIndex]
            if (self.eventMap[name] != None):
                commands.append(self.wrappedEventCommand(self.eventMap[name]))

        if stopEvent.executionBehavior == PathPlannerTrajectory.StopEvent.ExecutionBehavior.SEQUENTIAL:
            return cmd.sequence(commands)
        elif stopEvent.executionBehavior == PathPlannerTrajectory.StopEvent.ExecutionBehavior.PARALLEL:
            return cmd.parallel(commands)
        elif stopEvent.executionBehavior == PathPlannerTrajectory.StopEvent.ExecutionBehavior.PARALLEL_DEADLINE:
            deadline = self.wrappedEventCommand(self.eventMap[stopEvent.names[0]]) if stopEvent.names[0] in self.eventMap else cmd.none()
            return cmd.deadline(deadline, commands)
        else:
            raise Exception("Not Valid: {}".format(stopEvent.executionBehavior))
        
    def stopEventGroup(self, stopEvent: PathPlannerTrajectory.StopEvent):

        if len(stopEvent.names) == 0:
            return cmd.wait(stopEvent.waitTime)
        
        eventCommands = self.getStopEventCommands(stopEvent)

        if stopEvent.waitBehavior == PathPlannerTrajectory.StopEvent.WaitBehavior.BEFORE:
            return cmd.sequence(cmd.waitSeconds(stopEvent.waitTime), eventCommands)
        elif stopEvent.waitBehavior == PathPlannerTrajectory.StopEvent.WaitBehavior.AFTER:
            return cmd.sequence(eventCommands, cmd.waitSeconds(stopEvent.waitTime))
        elif stopEvent.waitBehavior == PathPlannerTrajectory.StopEvent.WaitBehavior.DEADLINE:
            return cmd.deadline(cmd.waitSeconds(stopEvent.waitTime), eventCommands)
        elif stopEvent.waitBehavior == PathPlannerTrajectory.StopEvent.WaitBehavior.MINIMUM:
            return cmd.parallel(cmd.waitSeconds(stopEvent.waitTime), eventCommands)
        else:
            return eventCommands
    
    def fullAuto(self, trajectory: PathPlannerTrajectory) -> commands2.Temporary: # Ingore temporary I will fix it later

        return self.fullAuto([trajectory])
