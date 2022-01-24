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
        self.leafNode = False
        self.bestState = None
        self.bestReward = -math.inf
        with open("parameters.json") as f:
            params = json.load(f)   # Pass out to controller
        self.k = params["expansion_coefficient"]
        self.a = params["expansion_exponentioal"]
        self.MCT : Dict[tuple, TreeNode] = {}

# ~~~ Selection and progressive widening ~~ #

    def selectNextNode(self) -> int:  # Returns next action towards a leaf node. Should happen in paralell with simulator.
        if len(self.currentNode.children) < self.k*self.currentNode.timesVisited**self.a:  # Prog wideniung
            seedAction = random.random()
            newBornAction = seedAction
            self.currentNode.add_child(newBornAction)
        selectedNode = self.currentNode.UCTselect()
        if selectedNode is None:
            seedAction = random.random()
            newBornAction = seedAction
            selectedNode = self.currentNode.add_child(newBornAction)
        selectedNode.visit_node()
        if selectedNode.timesVisited == 1:  # If first time visiting, it should be a leaf node.
            self.leafNode = True
        self.currentNode = selectedNode
        return selectedNode.action
    
    def isAtLeafNode(self):
        return self.leafNode

    def setAtRoot(self):
        self.leafNode = False

    def setCurrentNodeTerminal(self):  # REVIEW: Might not need this here. Could be handled in handler
        self.currentNode.isTerminal = True
    
    def setTransitionProbability(self, p):
        self.currentNode.transProb = p

    def rollout(self):
        # Returns the next sugested action.
        # NOTE: If this should be inteligent we need to track the actions dureing rollout. Not needed for random rollout.
        # Check for terminal should happen in terminal 
        return random.random()

    def backpropagate(self, reward):
        while self.currentNode != self.rootNode:
            reward = reward + self.currentNode.transProb  # REVIEW: Might be this simple, but I am tired.
            self.currentNode.eveluate(reward)
            self.currentNode.visit_node()
            self.currentNode = self.currentNode.parrent
        self.currentNode.visit_node()  # REVIEW: Doublecheck that some backrpop is not lost.
        return(reward)