

class Experiment(object):
    """ An experiment matches up a task with an agent and handles their interactions.
    """

    def __init__(self, task, agent):
        self.task = task
        self.agent = agent
        self.stepid = 0

    def doInteractions(self, number=1):
        """ The default implementation directly maps the methods of the agent and the task.
            Returns the number of interactions done.
        """
        for _ in range(number):
            self._oneInteraction()
        return self.stepid

    def _oneInteraction(self):
        """ Give the observation to the agent, takes its resulting action and returns
            it to the task. Then gives the reward to the agent again and returns it.
        """
        self.stepid += 1
        # observations from tasks are vectors
        self.agent.integrateObservation(self.task.getObservation())
        self.task.performAction(self.agent.getAction())
        reward = self.task.getReward()
        newstate = self.task.getObservation()
        self.agent.getReward(reward)
        return reward


if __name__=="__main__":

    from environments.loop import Loop, LoopTask
    from environments.chain import Chain, ChainTask
    from module import ActionModule
    from agent import BayesAgent

    # env = Loop()
    # task = LoopTask(env)
    env = Chain()
    task = ChainTask(env)
    module = ActionModule(env.outdim, env.indim)
    agent = BayesAgent(module)
    exp = Experiment(task, agent)

    for _ in xrange(1000):
        print exp.doInteractions(1)
        print "ACTION:",agent.lastaction, "STATE:",agent.laststate, "REWARD:",agent.lastreward

