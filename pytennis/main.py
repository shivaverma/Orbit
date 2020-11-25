import time
import numpy as np
import pygame
import sys
import os
from keras import Sequential, layers
from keras.optimizers import Adam
from keras.layers import Dense
from collections import deque


from Scripts.DQNetwork import DQN
from Scripts.BallRegression import Network
from Scripts.PyTennis import pytennis


from pygame.locals import *
pygame.init()


# initialize the 2 agents.
AgentA = DQN()
AgentB = DQN()


if __name__ == "__main__":
    tennis = pytennis(fps=70)
    tennis.reset()
    tennis.render()
