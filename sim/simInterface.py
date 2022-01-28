import json, math

from typing import List, Tuple

from sim.simpleBoatController import SimpleBoatController

class SimInterface:

    def __init__(self) -> None:  # Initiates simulation at state zero
        self.simWorld = SimpleBoatController()
        with open("parameters.json") as f:
            params = json.load(f)
        actionRange = params["action_range"]
        self.collisionReward = params["collision_reward"]
        self.totalRange = actionRange[1] - actionRange[0]
        self.minAction = actionRange[0]
        self.actionSeedTrace : List(float) = []
        self.simInEndstate : bool = False
        self.lastActionSeed = None

    def step(self, actionSeed):  # Return step reward (e.g. transition probability)
        action = self._getActionFromSeed(actionSeed)
        p = self._getTransitionProbability(actionSeed)
        self.simWorld.executeAction(action)
        self.actionSeedTrace.append(actionSeed)
        self.simInEndstate = self.simWorld.isEndstate()
        self.lastActionSeed = actionSeed
        return math.log(p)

    def terminalReward(self):
        e, d = self.simWorld.terminalStats()
        if e:
            return self.collisionReward
        else:
            return -d

    def isTerminal(self) -> bool:
        return self.simInEndstate

    def isFailureEpisode(self) -> bool:
        return self.simWorld.collisionHappened

    def getActionSeedTrace(self) -> List:
        return(self.actionSeedTrace)
    
    def setState(self, state : Tuple) -> None:
        self.resetSim()
        state = list(state)
        for actionSeed in state:
            self.step(actionSeed)

    def resetSim(self) -> None:
        self.actionSeedTrace = []
        self.lastActionSeed = None
        self.simWorld.resetSim()
        self.simInEndstate = False

    def plot(self) -> None:
        self.simWorld.plot(self._generateActionTrace(self.actionSeedTrace))
        
    def getPositionTrace(self, actionSeedTrace):
        actionTrace = self._generateActionTrace(actionSeedTrace)
        steerablePT, straightPT = self.simWorld._getPositionTrace(actionTrace)
        return [steerablePT, straightPT]

    def _getTransitionProbability(self, action):
        if self.lastActionSeed is None:
            return 1
        else:
            return 1-abs(action - self.lastActionSeed)  # TODO: Check if this is correct
    
    def _getActionFromSeed(self, actionSeed):
        return actionSeed * self.totalRange + self.minAction
        
    def _generateActionTrace(self, actionSeedTrace):
        actionTrace = []
        for actionSeed in actionSeedTrace:
            actionTrace.append(self._getActionFromSeed(actionSeed))
        return actionTrace
