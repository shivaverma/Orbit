import time
import os
import sys
from Scripts.DQNetwork import DQN
from Scripts.BallRegression import Network
import numpy as np
from keras.utils import to_categorical
import tensorflow as tf
import pygame
from pygame.locals import *
pygame.init()


class pytennis:
    def __init__(self, fps=50):
        self.GeneralReward = False
        self.net = Network(150, 450, 150, 650)
        self.updateRewardA = 0
        self.updateRewardB = 0
        self.updateIter = 0
        self.lossA = 0
        self.lossB = 0
        self.restart = False

        self.AgentA = DQN()
        self.AgentB = DQN()

        # Testing
        self.net = Network(150, 450, 150, 650)
        self.NetworkA = self.net.network(
            300, ysource=130, Ynew=700)  # Network A
        self.NetworkB = self.net.network(
            200, ysource=700, Ynew=130)  # Network B

        pygame.init()
        self.BLACK = (0, 0, 0)

        self.myFontA = pygame.font.SysFont("Times New Roman", 25)
        self.myFontB = pygame.font.SysFont("Times New Roman", 25)
        self.myFontIter = pygame.font.SysFont('Times New Roman', 25)

        self.FPS = fps
        self.fpsClock = pygame.time.Clock()

    def setWindow(self):

        # set up the window
        self.DISPLAYSURF = pygame.display.set_mode((600, 800), 0, 32)
        pygame.display.set_caption(
            'REINFORCEMENT LEARNING (DQN) - TABLE TENNIS')
        # set up the colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        return

    def display(self):
        self.setWindow()
        self.DISPLAYSURF.fill(self.WHITE)
        pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (50, 150, 500, 550))
        pygame.draw.rect(self.DISPLAYSURF, self.RED, (50, 415, 500, 20))
        pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (0, 20, 600, 20))
        pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (0, 770, 600, 20))
        return

    def reset(self):
        return

    def evaluate_state_from_last_coordinate(self, c):
        """
        cmax: 450
        cmin: 150

        c definately will be between 150 and 450.
        state0 - (50 - 99)
        state1 - (100 - 149)
        state2 - (150 - 199)
        state3 - (200 - 249)
        state4 - (250 - 299)
        state5 - (300 - 349)
        state6 - (350 - 399)
        state7 - (400 - 449)
        state8 - (450- 499)
        state9 - (500 - 550)
        """
        if c >= 50 and c <= 99:
            return 0
        elif c >= 100 and c <= 149:
            return 1
        elif c >= 150 and c <= 199:
            return 2
        elif c >= 200 and c <= 249:
            return 3
        elif c >= 250 and c <= 299:
            return 4
        elif c >= 300 and c <= 349:
            return 5
        elif c >= 350 and c <= 399:
            return 6
        elif c >= 400 and c <= 449:
            return 7
        elif c >= 450 and c <= 499:
            return 8
        elif c >= 500 and c <= 550:
            return 9

    def evaluate_action(self, diff):

        if (int(diff) <= 50):
            return True
        else:
            return False

    def randomVal(self, action):
        """
        cmax: 550
        cmin: 50

        c definately will be between 150 and 450.
        state0 - (50 - 99)
        state1 - (100 - 149)
        state2 - (150 - 199)
        state3 - (200 - 249)
        state4 - (250 - 299)
        state5 - (300 - 349)
        state6 - (350 - 399)
        state7 - (400 - 449)
        state8 - (450- 499)
        state9 - (500 - 550)
        """
        if action == 0:
            val = np.random.choice([i for i in range(50, 100)])
        elif action == 1:
            val = np.random.choice([i for i in range(100, 150)])
        elif action == 2:
            val = np.random.choice([i for i in range(150, 200)])
        elif action == 3:
            val = np.random.choice([i for i in range(200, 250)])
        elif action == 4:
            val = np.random.choice([i for i in range(250, 300)])
        elif action == 5:
            val = np.random.choice([i for i in range(300, 350)])
        elif action == 6:
            val = np.random.choice([i for i in range(350, 400)])
        elif action == 7:
            val = np.random.choice([i for i in range(400, 450)])
        elif action == 8:
            val = np.random.choice([i for i in range(450, 500)])
        else:
            val = np.random.choice([i for i in range(500, 550)])
        return val

    def stepA(self, action, count=0):
        # playerA should play
        if count == 0:
            self.NetworkA = self.net.network(
                self.ballx, ysource=130, Ynew=700)  # Network A
            self.bally = self.NetworkA[1][count]
            self.ballx = self.NetworkA[0][count]

            if self.GeneralReward == True:
                self.playerax = self.randomVal(action)
            else:
                self.playerax = self.ballx


#             soundObj = pygame.mixer.Sound('sound/sound.wav')
#             soundObj.play()
#             time.sleep(0.4)
#             soundObj.stop()

        else:
            self.ballx = self.NetworkA[0][count]
            self.bally = self.NetworkA[1][count]

        obsOne = self.evaluate_state_from_last_coordinate(
            int(self.ballx))  # last state of the ball
        obsTwo = self.evaluate_state_from_last_coordinate(
            int(self.playerbx))  # evaluate player bx
        diff = np.abs(self.ballx - self.playerbx)
        obs = obsTwo
        reward = self.evaluate_action(diff)
        done = True
        info = str(diff)

        return obs, reward, done, info

    def stepB(self, action, count=0):
        # playerB should play
        if count == 0:
            self.NetworkB = self.net.network(
                self.ballx, ysource=700, Ynew=130)  # Network B
            self.bally = self.NetworkB[1][count]
            self.ballx = self.NetworkB[0][count]

            if self.GeneralReward == True:
                self.playerbx = self.randomVal(action)
            else:
                self.playerbx = self.ballx


#             soundObj = pygame.mixer.Sound('sound/sound.wav')
#             soundObj.play()
#             time.sleep(0.4)
#             soundObj.stop()

        else:
            self.ballx = self.NetworkB[0][count]
            self.bally = self.NetworkB[1][count]

        obsOne = self.evaluate_state_from_last_coordinate(
            int(self.ballx))  # last state of the ball
        obsTwo = self.evaluate_state_from_last_coordinate(
            int(self.playerax))  # evaluate player bx
        diff = np.abs(self.ballx - self.playerax)
        obs = obsTwo
        reward = self.evaluate_action(diff)
        done = True
        info = str(diff)

        return obs, reward, done, info

    def computeLossA(self, reward):
        if reward == 0:
            self.lossA += 1
        else:
            self.lossA += 0
        return

    def computeLossB(self, reward):
        if reward == 0:
            self.lossB += 1
        else:
            self.lossB += 0
        return

    def render(self):
        # diplay team players
        self.PLAYERA = pygame.image.load('Images/padB.png')
        self.PLAYERA = pygame.transform.scale(self.PLAYERA, (50, 50))
        self.PLAYERB = pygame.image.load('Images/padA.png')
        self.PLAYERB = pygame.transform.scale(self.PLAYERB, (50, 50))
        self.ball = pygame.image.load('Images/ball.jpg')
        self.ball = pygame.transform.scale(self.ball, (15, 15))

        self.playerax = 150
        self.playerbx = 250

        self.ballx = 250
        self.bally = 300

        count = 0
        nextplayer = 'A'
        # player A starts by playing with state 0
        obsA, rewardA, doneA, infoA = 0, False, False, ''
        obsB, rewardB, doneB, infoB = 0, False, False, ''
        stateA = 0
        stateB = 0
        next_stateA = 0
        next_stateB = 0

        actionA = 0
        actionB = 0

        iterations = 20000
        iteration = 0
        restart = False

        while iteration < iterations:

            self.display()
            self.randNumLabelA = self.myFontA.render(
                'A (Win): '+str(self.updateRewardA), 1, self.BLACK)
            self.randNumLabelB = self.myFontB.render(
                'B (Win): '+str(self.updateRewardB), 1, self.BLACK)
            # self.randNumLabelIter = self.myFontIter.render(
            #     'Iterations: '+str(self.updateIter), 1, self.BLACK)

            if nextplayer == 'A':

                if count == 0:
                    # Online DQN evaluates what to do
                    arr = np.array([stateA])
                    q_valueA = self.AgentA.model.predict(arr)
                    actionA = self.AgentA.epsilon_greedy(q_valueA, iteration)

                    # Online DQN plays
                    obsA, rewardA, doneA, infoA = self.stepA(
                        action=actionA, count=count)
                    next_stateA = actionA

                    # Let's memorize what just happened
                    self.AgentA.replay_memory.append(
                        (stateA, actionA, rewardA, next_stateA, 1.0 - doneA))
                    stateA = next_stateA

                elif count == 49:

                    # Online DQN evaluates what to do
                    arr = np.array([stateA])
                    q_valueA = self.AgentA.model.predict(arr)
                    actionA = self.AgentA.epsilon_greedy(q_valueA, iteration)
                    obsA, rewardA, doneA, infoA = self.stepA(
                        action=actionA, count=count)
                    next_stateA = actionA

                    self.updateRewardA += rewardA
                    self.computeLossA(rewardA)

                    # Let's memorize what just happened
                    self.AgentA.replay_memory.append(
                        (stateA, actionA, rewardA, next_stateA, 1.0 - doneA))

                    # restart the game if player A fails to get the ball, and let B start the game
                    if rewardA == 0:
                        self.restart = True
                        time.sleep(0.5)
                        nextplayer = 'B'
                        self.GeneralReward = False
                    else:
                        self.restart = False
                        self.GeneralReward = True

                    # Sample memories and use the target DQN to produce the target Q-Value
                    X_state_val, X_action_val, rewards, X_next_state_val, continues = (
                        self.AgentA.sample_memories(self.AgentA.batch_size))
                    arr = [X_next_state_val]
                    next_q_values = self.AgentA.model.predict(arr)
                    max_next_q_values = np.max(
                        next_q_values, axis=1, keepdims=True)
                    y_val = rewards + continues * self.AgentA.discount_rate * max_next_q_values

                    # Train the online DQN
                    self.AgentA.model.fit(X_state_val, tf.keras.utils.to_categorical(
                        X_next_state_val, num_classes=10), verbose=0)

                    nextplayer = 'B'
                    self.updateIter += 1

                    count = 0
                    # evaluate A

                else:
                    # Online DQN evaluates what to do
                    arr = np.array([stateA])
                    q_valueA = self.AgentA.model.predict(arr)
                    actionA = self.AgentA.epsilon_greedy(q_valueA, iteration)

                    # Online DQN plays
                    obsA, rewardA, doneA, infoA = self.stepA(
                        action=actionA, count=count)
                    next_stateA = actionA

                    # Let's memorize what just happened
                    self.AgentA.replay_memory.append(
                        (stateA, actionA, rewardA, next_stateA, 1.0 - doneA))
                    stateA = next_stateA

                if nextplayer == 'A':
                    count += 1
                else:
                    count = 0

            else:
                if count == 0:
                    # Online DQN evaluates what to do
                    arr = np.array([stateB])
                    q_valueB = self.AgentB.model.predict(arr)
                    actionB = self.AgentB.epsilon_greedy(q_valueB, iteration)

                    # Online DQN plays
                    obsB, rewardB, doneB, infoB = self.stepB(
                        action=actionB, count=count)
                    next_stateB = actionB

                    # Let's memorize what just happened
                    self.AgentB.replay_memory.append(
                        (stateB, actionB, rewardB, next_stateB, 1.0 - doneB))
                    stateB = next_stateB

                elif count == 49:

                    # Online DQN evaluates what to do
                    arr = np.array([stateB])
                    q_valueB = self.AgentB.model.predict(arr)
                    actionB = self.AgentB.epsilon_greedy(q_valueB, iteration)

                    # Online DQN plays
                    obs, reward, done, info = self.stepB(
                        action=actionB, count=count)
                    next_stateB = actionB

                    # Let's memorize what just happened
                    self.AgentB.replay_memory.append(
                        (stateB, actionB, rewardB, next_stateB, 1.0 - doneB))

                    stateB = next_stateB
                    self.updateRewardB += rewardB
                    self.computeLossB(rewardB)

                    # restart the game if player A fails to get the ball, and let B start the game
                    if rewardB == 0:
                        self.restart = True
                        time.sleep(0.5)
                        self.GeneralReward = False
                        nextplayer = 'A'
                    else:
                        self.restart = False
                        self.GeneralReward = True

                    # Sample memories and use the target DQN to produce the target Q-Value
                    X_state_val, X_action_val, rewards, X_next_state_val, continues = (
                        self.AgentB.sample_memories(self.AgentB.batch_size))
                    arr = [X_next_state_val]
                    next_q_values = self.AgentB.model.predict(arr)
                    max_next_q_values = np.max(
                        next_q_values, axis=1, keepdims=True)
                    y_val = rewards + continues * self.AgentB.discount_rate * max_next_q_values

                    # Train the online DQN
                    self.AgentB.model.fit(X_state_val, tf.keras.utils.to_categorical(
                        X_next_state_val, num_classes=10), verbose=0)

                    nextplayer = 'A'
                    self.updateIter += 1
                    # evaluate B

                else:
                    # Online DQN evaluates what to do
                    q_valueB = self.AgentB.model.predict([stateB])
                    actionB = self.AgentB.epsilon_greedy(q_valueB, iteration)

                    # Online DQN plays
                    obsB, rewardB, doneB, infoB = self.stepB(
                        action=actionB, count=count)
                    next_stateB = actionB

                    # Let's memorize what just happened
                    self.AgentB.replay_memory.append(
                        (stateB, actionB, rewardB, next_stateB, 1.0 - doneB))
                    tateB = next_stateB

                if nextplayer == 'B':
                    count += 1
                else:
                    count = 0

            iteration += 1

            # CHECK BALL MOVEMENT
            self.DISPLAYSURF.blit(self.PLAYERA, (self.playerax, 100))
            self.DISPLAYSURF.blit(self.PLAYERB, (self.playerbx, 700))
            self.DISPLAYSURF.blit(self.ball, (self.ballx, self.bally))
            self.DISPLAYSURF.blit(self.randNumLabelA, (20, 40))
            self.DISPLAYSURF.blit(self.randNumLabelB, (450, 40))
            # self.DISPLAYSURF.blit(self.randNumLabelIter, (50, 40))

            # update last coordinate
            # self.lastxcoordinate = self.ballx

            pygame.display.update()
            self.fpsClock.tick(self.FPS)

            for event in pygame.event.get():

                if event.type == QUIT:
                    self.AgentA.model.save('models/AgentA.h5')
                    self.AgentB.model.save('models/AgentB.h5')
                    pygame.quit()
                    sys.exit()
