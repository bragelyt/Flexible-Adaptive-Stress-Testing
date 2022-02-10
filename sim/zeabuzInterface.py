
from re import X
import random
from af_colav_sim import Simulation
import numpy as np
import matplotlib.pyplot as plt
from af_colav_sim.data_utils import pack_array
from af_colav_sim.plotting.scenario_plotter import ScenarioPlotter
import math


class ZeabuzSimInterface:

    def __init__(self, scenario) -> None:
        self.sim = Simulation(f'scenarios/{scenario}.yaml')
        self.controlllers = None
        self.resetSim()
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
    
    def step(self, actionSeed):
        self.actionSeedTrace.append(actionSeed)
        nu_d = [1., 0., self._getActionFromSeed(actionSeed)]
        p = self._getTransitionProbability(actionSeed)
        for vessel, controller in self.controllers.items():
            controller.update_nu_d(nu_d)
        for i in range(10):
            self.mA.controller.tracker.set_noise(self.getDelayedState(100))
            self.terminal = not self.sim.step()
            self._updateDistance()
            if self.terminal:
                break
        self.lastActionSeed = actionSeed
        # self.mA.controller.tracker.set_noise([0,0,0,0])
        return math.log(p)

    def getActionSeedTrace(self):
        return self.actionSeedTrace
    
    def getDelayedState(self, delay):
        i = len(self.sim.sim_state.xx) - delay
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
        currPos = xx[-1][13:16]
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
                return -self.d*10

    def saveLast(self, fileName = "LastSim"):
        print("Saving as", fileName)
        self.sim.save(fileName)
    
    def plotSavedPath(self, fileName = "LastSim", rate = 20.0, borders = False, noise = True):  # TODO: Pull sim stats out to params.
        simPlotter = ScenarioPlotter(fileName, rate = rate, plot_obs_est = noise, sp_vp = borders, metrics = False)
        simPlotter.run()

    def _getActionFromSeed(self, actionSeed):
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
            print("Crashed")
        if mAx > 99:
            # print("Reached dock")
            self.terminal = True

    def _getTransitionProbability(self, action):
        if self.lastActionSeed is None:
            return 1
        else:
            return 1-abs(action - self.lastActionSeed)  # TODO: Check if this is correct

    def _euclideanD(self, x1, y1, x2, y2):
        return(math.sqrt((x1-x2)**2 + (y1-y2)**2))
    
    def _angleToVector(self, angle):
        return[math.cos(angle[0])*angle[1], math.sin(angle[0])*angle[1]]