from sim.simInterface import SimInterface

class MCTSHandler:

    # Handler should talk with MCTS and simInterfac, passing actions and rewards between the two parts.
    # At a later date different handlers could be built using the same MCTS logic. NOTE: This might meen rollout should be passed out.

    def __init__(self) -> None:
        pass

    def reward(self, actionSeed):
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