from sim.simInterface import SimInterface
from mcts.mcts import MCTS

class MCTSHandler:

    #TODO: Add funcitons for rerooting tree at most promising node. (Start wiht simple UCT and no exploration?)

    def __init__(self) -> None:
        
        self.mcts = MCTS()
        self.sim = SimInterface()
        for i in range(6000):
            if i%500 == 0:
                print(i)
            self.loop()
    
    def loop(self):
        terminal = False
        #  Selection and progressive widening  #
        while not self.mcts.isAtLeafNode():
            actionSeed = self.mcts.selectNextNode()
            p = self.sim.step(actionSeed)
            if self.sim.is_terminal():
                self.mcts.setCurrentNodeTerminal()
        self.mcts.setTransitionProbability(p)

        # --------- Rollout -------- #
        rolloutTransProb = 0
        while not terminal:
            actionSeed = self.mcts.rollout()
            rolloutTransProb += self.sim.step(actionSeed)
            terminal = self.sim.is_terminal()

        # ------ Backpropagate ----- #
        terminalReward = self.sim.terminal_reward()
        totalReward = self.mcts.backpropagate(terminalReward + rolloutTransProb)
        self.mcts.setAtRoot()
        actionTrace = self.sim.get_state()
        self.sim.reset_sim()
        return (totalReward, actionTrace)