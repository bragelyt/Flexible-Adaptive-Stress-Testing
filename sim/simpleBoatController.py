import math, json, copy


#TODO: Messy simulation. Should be cleaned up.
#
#   Function explenation
#  execute_action(self, action:float) -> p, e, d (transition probability from last action, episode happened, shortest distance throughout sim.)
#   Takes a seed (random float from [0,1]), transfomrs seed into doable action, and executes that aciton on the simulation
#
#  is_endstate(self) -> bool (is the simulation in an endstate?)
#   If boates are within crahs distance or the boat going straight has exited frame collision_happened and sim_in_endstate is updated and sim_in_endstate is returned
#
#  get_state(self) -> action_trace : list[float]
#
#  reset_sim(self) -> None:
#   Sim is reset to start state, variables and everything reset.
#
#  plot(self) -> None:
#   Plots the route of the current state.

class SimpleBoatController:

    def __init__(self) -> None:
        with open("parameters.json") as f:
            params = json.load(f)
        self.steplength = params["steplength"]
        self.crash_distance_threshold = params["crash_distance_threshold"]
        self.action_range = params["action_range"]
        self.resetSim()
    

    def resetSim(self):
        with open("parameters.json") as f:
            params = json.load(f)
        self.straightPos = params["straight_pos"]
        self.steerablePos = params["steerable_pos"]
        self.steerableangle = 0
        self.collisionHappened = False
        self.simInEndstate = False
        self.closestBoatDistance = self._getCurrentDistance()
            
    def executeAction(self, action: float):  # Action should be scaled by actionIntefrace.
        self.steerableangle += action*math.pi/100
        self._nextState()
        self.isEndstate()

    def terminalStats(self):
        if self.simInEndstate:
            e = self.collisionHappened
            d = self.closestBoatDistance
            return(e, d)
        else:
            print("Cant get terminal reward when sim is not in endstate")

    def isEndstate(self):
        if self.simInEndstate != True:
            if self.closestBoatDistance < self.crash_distance_threshold:
                self.collisionHappened = True
                self.simInEndstate = True
            elif self.straightPos[0] > 100:
                self.simInEndstate = True
        return self.simInEndstate

    def _nextState(self):
        self.steerablePos[0] += math.sin(self.steerableangle)*self.steplength
        self.steerablePos[1] += math.cos(self.steerableangle)*self.steplength
        self.straightPos[0] += self.steplength
        self._updateClosestDistance()
    
    def _getCurrentDistance(self):
        return self._boatDistance(self.steerablePos, self.straightPos)

    def _boatDistance(self, pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

    def _updateClosestDistance(self):
        distance = self._getCurrentDistance()
        if distance < self.closestBoatDistance:
            self.closestBoatDistance = distance

    def _getPositionTrace(self, actionTrace):  # Prev pos is not stored, so sim is reset, and fast forwarded through
        self.resetSim()
        steerableState = []
        straightState = []
        for action in actionTrace:
            steerableState.append(copy.copy(self.steerablePos))
            straightState.append(copy.copy(self.straightPos))
            self.executeAction(action)
        steerableState.append(copy.copy(self.steerablePos))
        straightState.append(copy.copy(self.straightPos))
        return steerableState, straightState
