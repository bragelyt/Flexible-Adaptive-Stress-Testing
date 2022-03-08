from typing import List, Tuple

from numpy import double
from mcts.mcts import MCTS
from visualize.tracePlotter import TracePlotter
import math

class MCTSHandler:

    #TODO: Add funcitons for rerooting tree at most promising node. (Start wiht simple UCT and no exploration?)

    def __init__(self, interface, verbose = True, plotBest = False) -> None:
        self.mcts = MCTS()
        self.sim = interface
        if self.sim.__class__.__name__ == "ZeabuzSimInterface":
            self.interface = "zeabuz"
            self.verboseInterval = 10
        elif self.sim.__class__.__name__ == "SimInterface":
            self.interface = "simple"
            self.verboseInterval = 1000
        self.plotBest = plotBest
        self.verbose = verbose
        if plotBest:
            self.plotter = TracePlotter()
    
    def buildSingleTree(self, loops) -> List[double]:
        self.maxReward = -math.inf
        self.bestActionSeedTrace = None
        for i in range(loops):
            totalReward, actionSeedTrace = self.loop()
            self.saveBest(totalReward, actionSeedTrace, i)
            self.sim.resetSim()
        print(self.maxReward)
        if self.plotBest:
            self.plotResult()
        return(self.bestActionSeedTrace)

    def buildDescendingTree(self, loopsPrRoot) -> List[double]:  # MCTS should keep track of root
        self.maxReward = -math.inf
        self.bestActionSeedTrace = None
        simState = []
        for i in range(15):
            for j in range(loopsPrRoot):
                self.sim.setState(simState)
                totalReward, actionSeedTrace = self.loop()
                self.saveBest(totalReward, actionSeedTrace, j + loopsPrRoot*i)
            simState.append(self.mcts.setNextRoot())
            # print(simState)
        print(self.maxReward)
        if self.plotBest:
            self.plotResult()
        return(self.bestActionSeedTrace)

    def loop(self) -> Tuple[double, double]:
        #  Selection and progressive widening  #
        while not self.mcts.isAtLeafNode() and not self.sim.isTerminal():
            actionSeed = self.mcts.selectNextNode()
            p = self.sim.step(actionSeed)
        self.mcts.setStepReward(p)
        # --------- Rollout -------- #
        rolloutTransProb = 0
        while not self.sim.isTerminal():
            actionSeed = self.mcts.rollout()
            rolloutTransProb += self.sim.step(actionSeed)
        # ------ Backpropagate ----- #
        terminalReward = self.sim.terminalReward()
        totalReward = self.mcts.backpropagate(terminalReward + rolloutTransProb)
        self.mcts.setAtRoot()
        actionSeedTrace = self.sim.getActionSeedTrace()
        return(totalReward, actionSeedTrace)

    def saveBest(self, totalReward, actionSeedTrace, iterationNr):
        if self.maxReward < totalReward:
            self.maxReward = totalReward
            self.bestActionSeedTrace = actionSeedTrace
            if self.verbose: 
                print(totalReward, "found at itteration", iterationNr)
            if self.interface == "zeabuz":
                self.sim.saveLast()
        if self.verbose:
            if iterationNr%self.verboseInterval == 0:
                print(iterationNr)
    
    def plotResult(self):
        if self.interface == "zeabuz":
            self.sim.plotSavedPath()
        elif self.interface == "simple":
            self.plotter.animate(self.bestActionSeedTrace)
            print(self.maxReward)
        return self.bestActionSeedTrace