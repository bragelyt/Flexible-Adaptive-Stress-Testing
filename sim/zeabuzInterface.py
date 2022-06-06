import math, json, copy
from datetime import datetime

import numpy as np
from sim.adversarialRouter import AdversarialRouter

from af_colav_sim import Simulation
from af_colav_sim.plotting.scenario_plotter import ScenarioPlotter


class ZeabuzSimInterface:

    def __init__(self, scenario, mode = "Steer", route = False, steerablePaths = None) -> None:  #TODO: add steerablePaths to scenario.yaml file
        self.sim = Simulation(f'scenarios/{scenario}.yaml')
        self.controllers = None
        self.mode = mode
        self.route = route
        self.steerablePaths = steerablePaths
        if steerablePaths is not None:
            with open("scenarios/"+steerablePaths+".json", 'r') as f:
                self.steerablePaths = json.load(f)
        self.resetSim()
        print("Boink")
        self.initialState = self.getInternalState()
        # self.order = len(self.controllers)  # TODO: Could be nice to add more boats. Need to refractor action to a touple 
    
    def resetSim(self):
        self.d = math.inf
        self.terminal = False
        self.episodeHeppened = False
        self.lastActionSeed = None
        self.actionSeedTrace = []
        self.collisionReward = 200
        self.crashThreshold = 1
        self.sim.start()
        self.controllers = self.sim.get_steerable_controllers()
        self.mA = self.sim.get_milliAmphere()
        self.routers = []
        if self.route:
            for key, controller in self.controllers.items():
                if key in self.steerablePaths.keys():
                    if controller.name == "SteerableVesselController":
                        router = AdversarialRouter(controller, self.steerablePaths[key])
                        self.routers.append(router)
    
    def getInternalState(self):
        internalState = {
            "xx": copy.deepcopy(self.sim.sim_state.xx),
            "dxdt": self.sim.sim_state.dxdt,
            "t": copy.deepcopy(self.sim.sim_state.t),
            "step_callback": self.sim.sim_state.step_callback,
            
            "d": self.d,
            "terminal": self.terminal,
            "episodeHeppened": self.episodeHeppened,
            "lastActionSeed": self.lastActionSeed,
            "actionSeedTrace": self.actionSeedTrace
        }
        return internalState
    
    def setState(self, state) -> None:
        self.resetSim()
        for actionSeed in state:
            self.step(actionSeed)
    
    def setSmartState(self, state) -> None:
        self.setInternalState(self.initialState)
        for actionSeed in state:
            self.step(actionSeed)

    def setInternalState(self, internalState):
        self.sim.sim_state.xx = internalState["xx"]
        self.sim.sim_state.dxdt = internalState["dxdt"]
        self.sim.sim_state.t = internalState["t"]
        self.sim.sim_state.step_callback = internalState["step_callback"]

        self.d = internalState["d"]
        self.terminal = internalState["terminal"]
        self.episodeHeppened = internalState["episodeHeppened"]
        self.lastActionSeed = internalState["lastActionSeed"]
        self.actionSeedTrace = internalState["actionSeedTrace"]

    def getStateRepresentation(self):
        xx = self.sim.sim_state.xx
        zeabuzPos = xx[-1][0:3]
        adversaryPos = xx[-1][13:16]
        stateRepresentation = list(zeabuzPos) + list(adversaryPos)
        return stateRepresentation

    def step(self, actionSeed):
        if self.route:
            for router in self.routers:
                router.step()
        self.actionSeedTrace.append(actionSeed)
        if self.mode == "Steer":  # Steer and route not compatible yet. Could be fixed so that steer is path noise added on top of steer.
            return self.steerStep(actionSeed) * 10
        elif self.mode == "Delay":
            return self.delayStep(actionSeed) * 10
        elif self.mode == "Noise":
            return self.noiseStep(actionSeed) * 10
    
    def steerStep(self, actionSeed):
        nu_d = [1., 0., self._getActionFromSeed(actionSeed)]
        p = self._getTransitionProbability(actionSeed)*0.75
        for vessel, controller in self.controllers.items():
            controller.update_nu_d(nu_d)
        for i in range(30):
            self.terminal = not self.sim.step()
            self._updateDistance()
            if self.terminal:
                break
        self.lastActionSeed = actionSeed
        return math.log(p)
    
    def delayStep(self, actionSeed):
        p = self._getTransitionProbability(actionSeed)
        for i in range(30):
            dxdt = self.getDelayedState(actionSeed * 400)
            self.mA.controller.tracker.set_noise(dxdt)
            self.terminal = not self.sim.step()
            self._updateDistance()
            if self.terminal:
                break
        return - actionSeed*0.5 + math.log(p)# REVIEW: (log(1-x) might work)
    
    def noiseStep(self, actionSeed):
        noiseRanges = [[-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5]] # pos: N, E, acceleration: N, E. 10 pos = 1 acce
        totNoise = 0
        stringSeed = str(actionSeed)
        if "e" in stringSeed:
            stringSeed = stringSeed[:stringSeed.find("e")]
        while len(stringSeed) <= 18:
            stringSeed += "0"
        noise = []
        for i in range(4):
            seed = float(stringSeed[2+4*i:6+4*i])/10**4  # Seed is in range 0.0000 -> 0.9999
            scaledNoise = self.scaleSeedToRange(seed, noiseRanges[i])
            totNoise+= abs(scaledNoise)
            noise.append(scaledNoise)
        self.mA.controller.tracker.set_noise(noise)
        for i in range(30):
            self.terminal = not self.sim.step()
            self._updateDistance()
            if self.terminal:
                break
        return -totNoise/4

    def getActionSeedTrace(self):
        return self.actionSeedTrace
    
    def scaleSeedToRange(self, seed, range):
        totRange = range[1] - range[0]
        scaledSeed = seed*totRange+range[0]
        return scaledSeed
    
    def getDelayedState(self, delay):
        i = len(self.sim.sim_state.xx) - int(delay+1)
        #   Pos
        # 13: N
        # 14: E
        #   Angle
        # 15: deg
        # 16: velocity
        xx = self.sim.sim_state.xx
        delayPos = xx[max(0, i)][13:15]
        delayAngle = xx[max(0, i)][15:17]
        delayHeading = self._angleToVector(delayAngle)
        currPos = xx[-1][13:15]
        currAngle = xx[-1][15:17]
        currHeading = self._angleToVector(currAngle)
        dxdt = [delayPos[0]-currPos[0], delayPos[1]-currPos[1], delayHeading[0]-currHeading[0], delayHeading[1]-currHeading[1]]
        return dxdt

    def isTerminal(self):
        return self.terminal
    
    def terminalReward(self):
        if self.terminal:
            if self.episodeHeppened:
                return self.collisionReward
            else:
                return -self.d*50  # Needs tuning

    def saveLast(self, reward, actionSeed, suffix, iterationNr):
        self.fileName = f"zeabuz{self.mode}{suffix}"
        print("Saving as", self.fileName)
        data = {"Reward": reward, "ActionSeedTrace": actionSeed, "Iteration": iterationNr}
        with open("simLogs/" + self.fileName + ".json", 'w') as f:
            json.dump(data, f, indent=4)
        self.sim.save(self.fileName)
    
    def plotSavedPath(self, fileName = None, rate = 20.0, borders = True, noise = True):  # TODO: Pull sim stats out to params.
        if fileName is None:
            fileName = self.fileName
        simPlotter = ScenarioPlotter(fileName, rate = rate, plot_obs_est = noise, sp_vp = borders, metrics = False)
        simPlotter.run()

    def _getSteerActionFromSeed(self, actionSeed):
        return actionSeed - 0.5

    def _updateDistance(self):
        xx = self.sim.sim_state.xx[-1]
        xs = []
        ys = []
        for name, vessel in self.sim.vessels.items():
            _eta_ind = vessel._eta_ind
            x = xx[_eta_ind[0]]
            y = xx[_eta_ind[1]]
            if name == "milliAmpere":
                mAx = x
                mAy = y
            else:
                xs.append(x)
                ys.append(y)
        for i in range(len(xs)):
            d = self._euclideanD(mAx, mAy, xs[i], ys[i])
            if self.d > d:
                self.d = d
        if self.d < self.crashThreshold:
            self.terminal = True
            self.episodeHeppened = True
            # print("Crashed")
        if mAx > 99:
            # print("Reached dock")
            self.terminal = True

    def _getActionFromSeed(self, seedAction):
        return seedAction-0.5

    def _getTransitionProbability(self, action):
        if self.lastActionSeed is None:
            return 1
        else:
            return 1-abs(action - self.lastActionSeed)  # TODO: Check if this is correct

    def _euclideanD(self, x1, y1, x2, y2):
        return(math.sqrt((x1-x2)**2 + (y1-y2)**2))
    
    def _angleToVector(self, angle):
        return[math.cos(angle[0])*angle[1], math.sin(angle[0])*angle[1]]