from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features




#Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_SELECTED = features.SCREEN_FEATURES.selected.index

# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SCV = 45

_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4


def noOp():
    return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])

def selectPoint(point,select=0):
    return actions.FunctionCall(actions.FUNCTIONS.select_point.id, [[select], point])

def checkSelected(obs):
    a,b=(obs.observation["screen"][_SELECTED]).nonzero()
    return len(a)>0

class SimpleAgent(base_agent.BaseAgent):

    def __init__(self):
        self.selected = False


    def step(self, obs):
        super(SimpleAgent, self).step(obs)
        self.selected=checkSelected(obs)

        if self.selected:
            return noOp()
        else:
            unit_type = obs.observation["screen"][_PLAYER_RELATIVE]
            unit_y, unit_x = (unit_type == _PLAYER_FRIENDLY).nonzero()
            target = [unit_x[0], unit_y[0]]
            self.selected = True
            action = selectPoint(target)
            return action
