import math, json
from typing import Dict

class TreeNode:

    def __init__(self, action, parent):
        self.action = action
        self.parrent = parent
        self.isTerminal = False
        # self.cumD = None  # REVIEW: When can cumulative distance be passed in? Nodes are allways built after parrents. Might be possible to pass in at first backprop, but messy.
        
        # ---------- Stats --------- #
        self.timesVisited = 0  # Initiates only after visit so should be one
        self.evaluation = 0
        if self.action == None:
            self.transProb = 1
        else:
            self.evaluation = 0

        self.children : Dict[int, TreeNode] = {}
        # self.childrenVisits : Dict[tuple, int] = {}  # ChildNodeState, nrOfVisits  # TODO: Change childNodeState to treeNode
        # self.childrenEvaluations : Dict[tuple, tuple] = {}
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.explorationCoefficient = params["exploration_coefficient"]
    
    def visit_node(self):
        self.timesVisited += 1
    
    def add_child(self, newBornAction):
        if newBornAction not in self.children.keys():  # REVIEW: Sloppy fix for randomness in seed generation. If exact same seed generated before, a child is not added.
            self.children[newBornAction] = TreeNode(newBornAction, self)  # NOTE This is the backbone of the tree structure
        return self.children[newBornAction]
    
    def UCTselect(self):  # Tree policy. "Bandit based Monte-Carlo Planning", Kocsis and Szepervari (2006)
        # NOTE: This is left without a check for if children are empty. Should resolve itself through prog widening but might fuck up
        maxValue = -math.inf
        bestChild : TreeNode = None
        for child in self.children.values():
            x = child.evaluation + self.explorationCoefficient*(math.sqrt(math.log(self.timesVisited)/(1+child.timesVisited)))
            if x > maxValue:
                bestChild = child
                maxValue = x
        return bestChild

    def eveluate(self, reward): # Called dureing backprop
        self.evaluation = self.evaluation + (reward - self.evaluation)/self.timesVisited

    # def visit_child(self, childNodeState):
    #     self.childrenVisits[tuple(childNodeState)] += 1
    
    # def evaluate_child(self, childNodeState, evaluation):
    #     childTuple = tuple(childNodeState)
    #     self.childrenEvaluations[childTuple] = self.childrenEvaluations[childTuple] + (evaluation - self.childrenEvaluations[childTuple])/self.childrenVisits[childTuple]

    # def backpropegate(self, reward, targetNode):
    #     if self == targetNode:
    #         pass
    #     else:  # REVIEW Unsusre if this is correct. Must find out how policy works
    #         # ! Think this is a mistake, as the step reward is not taken into account as totalReward = reward + self.simulate()
    #         self.totalEvaluation += reward
    #         self.timesVisited += 1
    #         if self.parrent is not None:
    #             self.parrent.backpropegate(reward + self.reward, targetNode)  # FIXME: Do we want to return this? Don't see why, but I'm partialy blind.
