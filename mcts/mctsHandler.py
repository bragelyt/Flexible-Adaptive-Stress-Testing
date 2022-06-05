import math, json

from typing import List, Tuple
from numpy import double

from datetime import datetime
from mcts.mcts import MCTS
from visualize.tracePlotter import TracePlotter

def rootPrintNN(rootNr, maxReward, maxTrace, avgReward, state, pred, isBest):
    text = f'rootDepth: {rootNr:2.0f} | max: {maxReward:8.4f} | avg: {avgReward:8.4f} | best: {str([round(x,2) for x in maxTrace]):126s} | pred: {state:.2f} {[round(x, 3) for x in pred]}'
    if isBest:
        text = '\033[93m' + text + '\033[0m'
    print(text)

def rootPrint(rootNr, maxReward, maxTrace, avgReward, isBest):
    text = f'rootDepth: {rootNr:2.0f} | max: {maxReward:8.4f} | avg: {avgReward:8.4f} | best: {str([round(x,2) for x in maxTrace]):126s}'
    if isBest:
        text = '\033[93m' + text + '\033[0m'
    print(text)

def resultPrint(result, iteration, trace):
    if result > 0:
        print(f'\033[93m{result} found at iteration {iteration} | {trace}\033[0m')
    else:
        print(f'\033[91m{result} found at iteration {iteration} | {trace}\033[0m')


class MCTSHandler:

    #TODO: Add funcitons for rerooting tree at most promising node. (Start wiht simple UCT and no exploration?)

    def __init__(self, interface, verbose = True, plotBest = False, rolloutPolicy = None, valuePolicy = None, loadModel= False, saveModel = False, train = True, seeds = 1) -> None:
        self.loadModel = loadModel
        self.saveModel = saveModel
        self.train = train
        self.timeStart = str(datetime.now().replace(microsecond=0)).replace(" ","_").replace(":","-")
        self.rolloutPolicyType = rolloutPolicy
        self.valuePolivyType = valuePolicy
        self.simInterface = interface
        if self.simInterface.__class__.__name__ == "ZeabuzSimInterface":
            self.interface = "zeabuz"
            self.verboseInterval = 10
        elif self.simInterface.__class__.__name__ == "SimInterface":
            self.interface = "simple"
            self.verboseInterval = 1000
        self.mcts = MCTS(rolloutPolicy, valuePolicy, self.interface if loadModel else None, seeds = seeds)
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
        if self.verbose:
            print(self.maxReward)
        if self.plotBest:
            self.plotResult()
        return(self.bestActionSeedTrace, self.maxReward)

    def buildMultipleSingleTree(self, nrOfTrees, loops):
        cumReward = 0
        stats = {}
        for h in range(nrOfTrees):
            self.mcts = MCTS(None, None, None)
            stats[h] = {}
            actionTrace, reward = self.buildSingleTree(loops)
            cumReward += reward
            stats[h] = {"maxReward": reward, "route": str(actionTrace)}
            with open("multipleSingleTrees.json", 'w') as f:
                json.dump(stats, f, indent=4)

    def buildDescendingTree(self, nrOfTrees, treeDepth, loopsPrRoot, setInternalState = False) -> List[double]:  # MCTS should keep track of root
        self.maxReward = -math.inf
        self.bestActionSeedTrace = None
        self.stats = {}
        cumLoopTime = datetime.now() -datetime.now()
        simRunTimes = {}
        # rewards = []  # REVIEW: Should be looked at, but rewards are probably correct
        for h in range(nrOfTrees):
            print(f'\033[94m--------- Iteration {h} ----------\033[0m')
            self.stats[h] = {}
            root = self.mcts.reset()
            simState = []
            self.simInterface.resetSim()
            root.stateRepresentation = self.simInterface.getStateRepresentation()
            for i in range(treeDepth):
                start = datetime.now()
                maxReward = -math.inf
                cumReward = 0
                self.simInterface.setState(simState)
                isBest = False
                for j in range(loopsPrRoot):
                    self.simInterface.setState(simState)
                    totalReward, actionSeedTrace = self.loop()
                    if totalReward > maxReward:
                        maxReward = totalReward
                        bestPath = actionSeedTrace
                    cumReward += totalReward
                    isBest = self.saveBest(totalReward, actionSeedTrace, j + loopsPrRoot*i) or isBest
                if self.rolloutPolicyType is not None:
                    if self.train:
                        self.simInterface.setState(simState)
                        self.mcts.addNodeToTrainingBatch(self.simInterface.getStateRepresentation())
                nextAction = self.mcts.setNextRoot()
                self.stats[h][i] = {"maxReward": maxReward, "avg": cumReward / loopsPrRoot, "route": bestPath}
                if nextAction is None:
                    break
                else:
                    simState.append(nextAction)
                if self.verbose:
                    if self.rolloutPolicyType is not None:
                        rootPrintNN(i, maxReward, bestPath, cumReward / loopsPrRoot, self.simInterface.getStateRepresentation()[0], self.mcts.rolloutPolicy.getPrediction(self.simInterface.getStateRepresentation()), isBest)
                    else:
                        rootPrint(i, maxReward, bestPath, cumReward / loopsPrRoot, isBest)
                # print(i, "FullRootTime" , datetime.now()-start)
            if self.rolloutPolicyType is not None:
                print(f'\033[94m--------- Training {h} ----------\033[0m')
                if self.train:
                    self.mcts.trainRolloutPolicyAtRoot()
                    self.mcts.trainValuePolicyOnTree()
            if self.saveModel:
                self.mcts.saveModel(self.interface, self.rolloutPolicyType, self.valuePolivyType, self.timeStart)
            fileName = ""
            if self.loadModel:
                fileName+="load"
            if self.rolloutPolicyType is None and self.valuePolivyType is None:
                fileName += "noNetworkStats.json"
            elif self.rolloutPolicyType is None and self.valuePolivyType is not None:
                fileName += "valuePolicyStats.json"
            elif self.rolloutPolicyType is not None and self.valuePolivyType is None:
                fileName += "rolloutPolicyStats.json"
            elif self.rolloutPolicyType is not None and self.valuePolivyType is not None:
                fileName += "fullNNStats.json"
            with open(fileName, 'w') as f:
                    json.dump(self.stats, f, indent=4)
        if self.plotBest:
            self.plotResult()
        # print([round(x,4) for x in self.bestActionSeedTrace])
        print("-----", cumLoopTime)
        print(simRunTimes)
        # return
        return(self.bestActionSeedTrace)

    def loop(self) -> Tuple[double, double]:
        #  Selection and progressive widening  #
        p = None
        while not self.mcts.isAtLeafNode() and not self.simInterface.isTerminal():
            nextNode = self.mcts.selectNextNode(self.simInterface.getStateRepresentation())  # REVIEW: Hva faen?
            actionSeed = nextNode.action
            p = self.simInterface.step(actionSeed)
            nextNode.stateRepresentation = self.simInterface.getStateRepresentation()
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
            if self.interface == "zeabuz":
                self.simInterface.saveLast(totalReward, actionSeedTrace, self.timeStart, iterationNr)
            if self.verbose:
                resultPrint(totalReward, iterationNr, [round(x,2) for x in actionSeedTrace])
            return True
        return False
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