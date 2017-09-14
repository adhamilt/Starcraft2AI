from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
import numpy as np

import tensorflow as tf



_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_SELECTED = features.SCREEN_FEATURES.selected.index
_UNIT_HEALTH = features.SCREEN_FEATURES.unit_hit_points.index

_SCREEN_SIZE = 4096

class SoftmaxAgent(base_agent.BaseAgent):

    def __init__(self):
        self.x = tf.placeholder(tf.float32, [None, 4*4096])
        self.W = tf.Variable(tf.zeros([4*4096, 6]))
        self.b = tf.Variable(tf.zeros([6]))
        self.y = tf.nn.softmax(tf.matmul(self.x, self.W) + self.b)
        self.score = tf.placeholder(tf.float32,[1])

        self.sess= tf.InteractiveSession()
        tf.global_variables_initializer().run()


    def step(self, obs):


        screen=obs.observation["screen"]
        player_relative=screen[_PLAYER_RELATIVE].flatten()
        unit_type=screen[_UNIT_TYPE].flatten()
        selected=screen[_SELECTED].flatten()
        unit_health=screen[_UNIT_HEALTH].flatten()
        input_x = np.concatenate((player_relative,unit_type,selected,unit_health)).reshape(1,4*4096)


        output=self.sess.run(self.y, feed_dict={self.x: input_x}).tolist()
        return output[0]


