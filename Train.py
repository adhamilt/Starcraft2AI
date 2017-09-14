import sys

import gflags as flags
from pysc2.env import sc2_env
from PlayGame import PlayGame
from SoftmaxAgent import SoftmaxAgent
import numpy as np

import tensorflow as tf

import matplotlib.pyplot as plt

FLAGS = flags.FLAGS


agent = SoftmaxAgent()


#Setup the Game!
FLAGS(sys.argv)
step_mul = 8
env = sc2_env.SC2Env("DefeatRoaches",step_mul=step_mul,visualize=False)

score=tf.stack(np.float64(PlayGame(env,agent)))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(-score)

#Train
for _ in range(1000):
    print(agent.sess.run(train_step))


#Test

print(PlayGame(env,agent))