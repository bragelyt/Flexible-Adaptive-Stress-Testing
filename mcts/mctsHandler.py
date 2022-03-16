from fileinput import filename
import math

from typing import List, Tuple
from numpy import double

from mcts.mcts import MCTS
from visualize.tracePlotter import TracePlotter

def resultPrint(result, iteration, trace):
    if result > 0:
        print(f'\033[93m{result} found at itteration {iteration} | {trace}\033[0m')
    else:
        print(f'\033[91m{result} found at itteration {iteration} | {trace}\033[0m')


class MCTSHandler:

    #TODO: Add funcitons for rerooting tree at most promising node. (Start wiht simple UCT and no exploration?)

    def __init__(self, interface, verbose = True, plotBest = False, rolloutPolicy = None, valuePolicy = None, loadModel= False, saveModel = False, train = True) -> None:
        self.loadModel = loadModel
        self.saveModel = saveModel
        self.train = train
        self.rolloutPolicyType = rolloutPolicy
        self.valuePolivyType = valuePolicy
        self.simInterface = interface
        if self.simInterface.__class__.__name__ == "ZeabuzSimInterface":
            self.interface = "zeabuz"
            self.verboseInterval = 10
        elif self.simInterface.__class__.__name__ == "SimInterface":
            self.interface = "simple"
            self.verboseInterval = 1000
        self.mcts = MCTS(rolloutPolicy, valuePolicy, self.interface if loadModel else None)
        self.plotBest = plotBest
        self.verbose = verbose
        if plotBest:
            self.plotter = TracePlotter()
    
    def buildSingleTree(self, loops) -> List[double]:
        self.maxReward = -math.inf
        self.bestActionSeedTrace = None
        for i in range(loops):
            self.simInterface.resetSim()
            totalReward, actionSeedTrace = self.loop()
            self.saveBest(totalReward, actionSeedTrace, i)
        print(self.maxReward)
        if self.plotBest:
            self.plotResult()
        return(self.bestActionSeedTrace)

    def buildDescendingTree(self, loopsPrRoot) -> List[double]:  # MCTS should keep track of root
        self.maxReward = -math.inf
        self.bestActionSeedTrace = None
        for h in range(20):
            print("--------- Itteration", h,"----------")
            self.mcts.reset()
            simState = []
            self.simInterface.setState(simState)
            for i in range(18):
                print(i * 5, [round(x, 2) for x in self.mcts.rolloutPolicy.getPrediction(self.simInterface.getStateRepresentation())])
                for j in range(loopsPrRoot):
                    self.simInterface.setState(simState)
                    totalReward, actionSeedTrace = self.loop()
                    self.saveBest(totalReward, actionSeedTrace, j + loopsPrRoot*i)
                if self.rolloutPolicyType is not None:
                    if self.train:
                        self.mcts.addNodeToTrainingBatch(self.simInterface.getStateRepresentation())
                nextAction = self.mcts.setNextRoot()
                if nextAction is None:
                    break
                else:
                    simState.append(nextAction)
                # print(simState)
            if self.rolloutPolicyType is not None:
                print("--------- Training", h ,"------------")
                if self.train:
                    self.mcts.trainRolloutPolicyAtRoot()
        if self.saveModel:
            self.mcts.saveModel(self.interface + self.rolloutPolicyType)
        if self.plotBest:
            self.plotResult()
        print([round(x,4) for x in self.bestActionSeedTrace])
        return(self.bestActionSeedTrace)

    def loop(self) -> Tuple[double, double]:
        #  Selection and progressive widening  #
        p = None
        while not self.mcts.isAtLeafNode() and not self.simInterface.isTerminal():
            actionSeed = self.mcts.selectNextNode()
            p = self.simInterface.step(actionSeed)
        self.mcts.setStepReward(p)
        # --------- Rollout -------- #
        rolloutTransProb = 0
        while not self.simInterface.isTerminal():
            if self.rolloutPolicyType is None:
                actionSeed = self.mcts.rollout()
            else:
                actionSeed = self.mcts.getRolloutPolicy(self.simInterface.getStateRepresentation())
            rolloutTransProb += self.simInterface.step(actionSeed)
        # ------ Backpropagate ----- #
        terminalReward = self.simInterface.terminalReward()
        totalReward = self.mcts.backpropagate(terminalReward + rolloutTransProb)
        self.mcts.setAtRoot()
        actionSeedTrace = self.simInterface.getActionSeedTrace()
        return(totalReward, actionSeedTrace)

    def saveBest(self, totalReward, actionSeedTrace, iterationNr):
        if self.maxReward < totalReward:
            self.maxReward = totalReward
            self.bestActionSeedTrace = actionSeedTrace
            if self.verbose: 
                resultPrint(totalReward, iterationNr, [round(x,2) for x in actionSeedTrace])
            if self.interface == "zeabuz":
                self.simInterface.saveLast()
        # if self.verbose:  # REVIEW: I overkant?
        #     if iterationNr%self.verboseInterval == 0:
        #         print(iterationNr)
    
    def plotResult(self):
        if self.interface == "zeabuz":
            self.simInterface.plotSavedPath()
        elif self.interface == "simple":
            self.plotter.animate(self.bestActionSeedTrace)
            print(self.maxReward)
        return self.bestActionSeedTrace