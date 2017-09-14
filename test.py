import sys

import gflags as flags
from pysc2.env import sc2_env
from PlayGame import PlayGame
import tensorflow as tf

import matplotlib.pyplot as plt



FLAGS = flags.FLAGS


#Setup the Game!
FLAGS(sys.argv)
step_mul = 8
env = sc2_env.SC2Env("DefeatRoaches",step_mul=step_mul,visualize=False)

score=[]
for i in range(100):
    score.append(PlayGame(env))

n, bin, patches = plt.hist(score)
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.title("Score for Random Agent")
plt.show()