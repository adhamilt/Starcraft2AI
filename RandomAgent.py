from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
import numpy as np



class RandomAgent(base_agent.BaseAgent):

    def __init__(self):
        self.selected = False


    def step(self, obs):
        return np.random.rand(6).tolist()
