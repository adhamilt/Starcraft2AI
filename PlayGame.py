import numpy
from pysc2.lib import actions
from pysc2.lib import features



_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_SELECTED = features.SCREEN_FEATURES.selected.index

_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4

_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_UNIT = actions.FUNCTIONS.select_unit.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_SELECT_RECT = actions.FUNCTIONS.select_rect.id

_NOT_QUEUED = [0]
_SELECT_ALL = [0]

_SCREEN_SIZE= 64


def NoOp():
    return actions.FunctionCall(_NO_OP,[])


def SelectPoint(xy,select):
    return actions.FunctionCall(_SELECT_POINT,[[select],xy])


def AttackPoint(xy,queued):
    return actions.FunctionCall(_ATTACK_SCREEN,[[queued],xy])


def SelectArmy(select):
    return actions.FunctionCall(_SELECT_ARMY,[[select]])


def SelectRect(xy1,xy2,select):
    return actions.FunctionCall(_SELECT_RECT,[[select],xy1,xy2])


def ParseAction(obs,args):
    action_id = int(round(4 * args[0]))
    opt = int(round(args[1]))
    xy1 = [int(round((_SCREEN_SIZE - 1) * args[2])), int(round((_SCREEN_SIZE - 1) * args[3]))]
    xy2 = [int(round((_SCREEN_SIZE - 1) * args[4])), int(round((_SCREEN_SIZE - 1) * args[5]))]

    if action_id == 0:
        return NoOp()

    elif action_id == 1:
        return SelectPoint(xy1, opt)

    elif action_id == 2:
        if _ATTACK_SCREEN in obs[0].observation["available_actions"]:
            return AttackPoint(xy1, opt)
        else:
            #print("Attack Screen Not Available!")
            return NoOp()

    elif action_id == 3:
        if _SELECT_ARMY in obs[0].observation["available_actions"]:
            return SelectArmy(opt)
        else:
            #print("Attack Screen Not Available!")
            return NoOp()

    elif action_id == 4:
        return SelectRect(xy1, xy2, opt)

    else:
        #print("action id unknown!")
        return NoOp()


def PlayGame(env):
    obs = env.reset()
    env.action_spec()

    # Begin the Game!
    oldstep, newstep = 0, 0
    while newstep >= oldstep:
        rnd = numpy.random.rand(6).tolist()
        action = ParseAction(obs, rnd)

        score = obs[0].observation["score_cumulative"][0]
        obs = env.step([action])
        oldstep = newstep
        newstep = obs[0].observation["game_loop"][0]
    return score