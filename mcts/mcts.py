import random, math, json

from datetime import datetime
from typing import Dict
from mcts import treeNode

from mcts.treeNode import TreeNode
from sim.simInterface import SimInterface

# TODO: Pull sim out of mcts.

# This funciton should simply handle tree creatin, tuneing and traversal.

# Loop should be splitt into
    #  selectLeafNode: Traverse the tree form the root, checking each traversed node for expansion. Returns seed action sequence to leaf.
    #  rollout: Inputs 
    #  backpropagate:

# Functions are to be called from handler, and the simulator should also be forwarded from there.
# Handler should call selectionToLeafNode, Rollout, Backprop. Future possibilities are reroot and reset.

class MCTS:  
    
    def __init__(self) -> None:
        self.rootNode = TreeNode(None, None)  # NOTE: Might cause problems with None action, but it is correct. T=0
        self.currentNode = self.rootNode
        self.simIntefrace = SimInterface()
        self.endStates = []
        self.crashStates = []
        self.bestState = None
        self.bestReward = -math.inf
        with open("parameters.json") as f:
            params = json.load(f)   # Pass out to controller
        self.k = params["expansion_coefficient"]
        self.a = params["expansion_exponentioal"]
        self.MCT : Dict[tuple, TreeNode] = {}


    def selectLeafNode(self) -> int:  # Returns next action towards a leaf node. Should happen in paralell with simulator.
        actionSequence = []
        if len(self.currentNode.childrenVisits) < self.k*self.currentNode.timesVisited**self.a:  # Prog wideniung
            seedAction = random.random()
            newBornAction = seedAction
            self.currentNode.add_child(newBornAction)
        selectedNode = self.currentNode.UCTselect()
        selectedNode.visit_node()
        actionSequence.append(selectedNode.action)
        if selectedNode.timesVisited == 1:  # If first time visiting, it should be a leaf node.
            return actionSequence
            # TODO: Update node with terminal if it is. 
        self.currentNode = selectedNode
        
    def setCurrentNodeTerminal(self):
        self.currentNode.isTerminal = True
    
    def rollout(self):
        # Returns the next sugested action.
        # NOTE: If this should be inteligent we need to track the actions dureing rollout. Not needed for random rollout.
        # Check for terminal should happen in terminal 
        return self.random()

    def backpropagate(self):
        # TODO: Use parrent and current node to backpropagate. 
        # NOTE: Might want to have the step reward saved for backprop upgrade. 
        # NOTE: As totalReward = reward + self.simulate() then step reward should be taken into account at all steps. Backprop in node is broken.
        # totalReward = reward + self.simulate()

        # NOTE: D is the distance from current node to endstate. A parrent should have its own distance, as well as distance of children.
        # NOTE: Bacprop distance from leaf to root would cumulate distance by adding action distance going backwards

        # REVIEW: Calculate toltal distance and reward during rollout. Going up the tree dureing backprop, add distances to a cumulative Q and tune for that.
        # REVIEW: Where to store d?
            # d could be stored in node, but might be hard to find a fitting spot to input d
            # list of d's could be constructed dureing selection phase. Probably stupid though, but easy.

        # To achieve this cumD should be passed into node and not added to total R dureing seleciton, only during rollouts.
        while self.currentNode.parent is not None:
            #TODO: Meat of the funcion goes here.
            reward = 0
            self.currentNode.evaluate(reward)
            self.currentNode = self.currenNode.parrent
    
    def loop(self, numberOfLoops):
        for i in range(numberOfLoops):
            self.currentNode = None
            if (i%1000 == 0):
                print(i)
            self.simIntefrace.reset_sim()
            G = self.simulate()
            if G > self.bestReward:
                self.bestState = self.simIntefrace.get_state()
                self.bestReward = G
                print(f'Score {round(G, 2)} found at iteration {i}')
        return self.bestState, self.bestReward

    def getMainRoot(self):
        self.rootNode : treeNode = None
        self.currentNode = self.rootNode
    
    def setRoot(self, node: treeNode):
        self.rootNode = node

    def oneLoop(self):
        self.currentNode = None
        self.simIntefrace.reset_sim()
        totalReward = self.simulate()
        if totalReward > self.bestReward:
            self.bestState = self.simIntefrace.get_state()
            self.bestReward = totalReward

    def simulate(self):  # Three polict, expansion, rollout and backprop of a leaf node

        state = self.simIntefrace.get_state()  # Get state to determine what node to bee at. Sloppy

        if tuple(state) not in list(self.MCT.keys()):  # Check at tree node level. Smaller dicts. Easier cleanup.
            simNode = TreeNode(state)  # If new node, it is a leaf node and we can rollout. Selection part
            self.MCT[tuple(state)] = simNode
            return self.rollout()  # return actionSequence.
        node = self.MCT[tuple(state)]

        node.visit_node()

        if len(node.childrenVisits) < self.k*node.timesVisited**self.a:  # Prog wideniung
            seedAction = random.random()
            newBornState = state + [seedAction]
            node.add_child(newBornState)

        nextNode = node.UCTselect()  # ! returns state, not just action. Might want to change

        chosenSeed = nextNode[-1]

        # TODO: This should be moved out. Here on down is sim handling.
        reward = self.simIntefrace.step(chosenSeed)
        terminal = self.simIntefrace.is_terminal()  # ! Figure out if we test for terminal before or after. Is crash destined?
        e = self.simIntefrace.is_failure_episode()
        if terminal:  # If tree is big enough to have an endstate in it we cant rollout.
            self.endStates.append(state)
            if e:
                self.crashStates.append(tuple(state))
            return reward
        # self.currentNode = nextNode
        totalReward = reward + self.simulate()
        node.visit_child(nextNode)
        node.evaluate_child(nextNode, totalReward)
        return totalReward
    
    def rollout(self) -> float:  # Should be redefined to getRolloutSeed.
        actionSeed = random.random()
        reward = self.simIntefrace.step(actionSeed)
        terminal = self.simIntefrace.is_terminal()
        e = self.simIntefrace.is_failure_episode()
        if terminal:
            state = self.simIntefrace.get_state()
            self.endStates.append(state)
            if e:
                self.crashStates.append(tuple(state))
            return reward
        return reward + self.rollout()