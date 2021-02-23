import time
import os
import sys
from network import DQN
from network import Network
import numpy as np
from keras.utils import to_categorical
import tensorflow as tf
import pygame
from pygame.locals import *
from keras import Sequential, layers
from keras.optimizers import Adam
from keras.layers import Dense
from collections import deque

pygame.init()



class tennis:
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
            300, ysource=80, Ynew=650)  # Network A
        self.NetworkB = self.net.network(
            200, ysource=650, Ynew=80)  # Network B

        pygame.init()
        self.BLACK = (0, 0, 0)

        self.myFontA = pygame.font.SysFont("Times New Roman", 25)
        self.myFontB = pygame.font.SysFont("Times New Roman", 25)
        self.myFontIter = pygame.font.SysFont('Times New Roman', 25)

        self.FPS = fps
        self.fpsClock = pygame.time.Clock()

    def setWindow(self):

        # set up the window
        self.DISPLAYSURF = pygame.display.set_mode((600, 750), 0, 32)
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
        pygame.draw.rect(self.DISPLAYSURF, self.BLACK, (50, 100, 500, 550))
        pygame.draw.rect(self.DISPLAYSURF, self.RED, (50, 365, 500, 20))
        return

    def reset(self):
        return

    def evaluate_state_from_last_coordinate(self, c):
        """
        cmax: 550
        cmin: 50

        c definately will be between 50 and 550.
        """
        if c >= 50 and c <= 550:
            return int(c/50 - 1)
        else:
            return 0

    def evaluate_action(self, diff):

        if (int(diff) <= 50):
            return True
        else:
            return False

    def randomVal(self, action):
        "action is a probability of values between 0 and 1"
        val =  (action*500) + 50
        return val

    def step(self, action, count=0, step = 'A'):
        # Step = A implies compute player A's next step.
        # Step = B implies compute player B's next step.
        
        if step == 'A':
            # playerA should play
            if count == 0:
                self.NetworkA = self.net.network(
                    self.ballx, ysource=80, Ynew=650)  # Network A
                self.bally = self.NetworkA[1][count]
                self.ballx = self.NetworkA[0][count]

                if self.GeneralReward == True:
                    self.playerax = self.randomVal(action)
                else:
                    self.playerax = self.ballx


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

        else:
            # playerB should play
            if count == 0:
                self.NetworkB = self.net.network(
                    self.ballx, ysource=650, Ynew=80)  # Network B
                self.bally = self.NetworkB[1][count]
                self.ballx = self.NetworkB[0][count]

                if self.GeneralReward == True:
                    self.playerbx = self.randomVal(action)
                else:
                    self.playerbx = self.ballx


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

    def computeLoss(self, reward, loss = 'A'):
        # loss = A, implies compute loss of player A, otherwise, compute Player B loss.
        if loss == 'A':
            if reward == 0:
                self.lossA += 1
            else:
                self.lossA += 0
        else:
            if reward == 0:
                self.lossB += 1
            else:
                self.lossB += 0
        return

    def execute(self, state, iteration, count, player = 'A'):
        if player == 'B':
            stateB = state
            # Online DQN evaluates what to do
            
            try:
                q_valueB = self.AgentB.model.predict([stateB])
            except:
                q_valueB = 0
            actionB = self.AgentB.epsilon_greedy(q_valueB, iteration)

            # Online DQN plays
            obsB, rewardB, doneB, infoB = self.step(
                action=actionB, count=count, step = 'B')
            next_stateB = actionB

            # Let's memorize what just happened
            self.AgentB.replay_memory.append(
                (stateB, actionB, rewardB, next_stateB, 1.0 - doneB))
            stateB = next_stateB

            output = (q_valueB, actionB, obsB, rewardB, doneB, infoB, next_stateB,  actionB, stateB)

        else:
            stateA = state
            # Online DQN evaluates what to do
            # arr = np.array([stateA])
            try:
                q_valueA = self.AgentB.model.predict([stateB])
            except:
                q_valueA = 0
            actionA = self.AgentA.epsilon_greedy(q_valueA, iteration)

            # Online DQN plays
            obsA, rewardA, doneA, infoA = self.step(
                action=actionA, count=count, step = 'A')
            next_stateA = actionA

            # Let's memorize what just happened
            self.AgentA.replay_memory.append(
                (stateA, actionA, rewardA, next_stateA, 1.0 - doneA))
            stateA = next_stateA

            output = (q_valueA, actionA, obsA, rewardA, doneA, infoA, next_stateA,  actionA, stateA)

        return output

    def trainOnlineDQN(self, player = 'A'):
        if player == 'A':
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
        else:
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


        return True

    def render(self):
        # diplay team players
        self.PLAYERA = pygame.image.load('Images/padB.png')
        self.PLAYERA = pygame.transform.scale(self.PLAYERA, (50, 50))
        self.PLAYERB = pygame.image.load('Images/padA.png')
        self.PLAYERB = pygame.transform.scale(self.PLAYERB, (50, 50))
        self.ball = pygame.image.load('Images/ball.png')
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
        state = 0
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
                'Score A: '+str(self.updateRewardA), 1, self.BLACK)
            self.randNumLabelB = self.myFontB.render(
                'Score B: '+str(self.updateRewardB), 1, self.BLACK)
            
            if nextplayer == 'A':

                if count == 0:
                    print('state: ', state)
                    print('iteration: ', iteration)
                    print('count: ', count)
                    print('player: ', nextplayer)
                    output = self.execute(state, iteration, count, player = nextplayer)
                    q_valueA, actionA, obsA, rewardA, doneA, infoA, next_stateA,  actionA, stateA = output
                    state = next_stateA


                elif count == 49:

                    output = self.execute(state, iteration, count, player = 'A')
                    q_valueA, actionA, obsA, rewardA, doneA, infoA, next_stateA,  actionA, stateA = output
                    state = next_stateA

                    self.updateRewardA += rewardA
                    self.computeLoss(rewardA, loss = 'A')

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
                    self.trainOnlineDQN(player = 'A')

                    nextplayer = 'B'
                    self.updateIter += 1

                    count = 0
                    # evaluate A

                else:
                    output = self.execute(state, iteration, count, player = 'A')
                    q_valueA, actionA, obsA, rewardA, doneA, infoA, next_stateA,  actionA, stateA = output
                    state = next_stateA

                if nextplayer == 'A':
                    count += 1
                else:
                    count = 0

            else:
                if count == 0:
                    output = self.execute(state, iteration, count, player = 'B')
                    q_valueB, actionB, obsB, rewardB, doneB, infoB, next_stateB,  actionB, stateB = output
                    state = next_stateB

                elif count == 49:

                    output = self.execute(state, iteration, count, player = 'B')
                    q_valueB, actionB, obsB, rewardB, doneB, infoB, next_stateB,  actionB, stateB = output
                    state = next_stateB

                    self.updateRewardB += rewardB
                    self.computeLoss(rewardB, loss = 'B')

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
                    self.trainOnlineDQN(player = 'B')

                    nextplayer = 'A'
                    self.updateIter += 1
                    # evaluate B

                else:
                    output = self.execute(state, iteration, count, player = 'B')
                    q_valueB, actionB, obsB, rewardB, doneB, infoB, next_stateB,  actionB, stateB = output
                    state = next_stateB

                if nextplayer == 'B':
                    count += 1
                else:
                    count = 0

            iteration += 1

            # CHECK BALL MOVEMENT
            self.DISPLAYSURF.blit(self.PLAYERA, (self.playerax, 50))
            self.DISPLAYSURF.blit(self.PLAYERB, (self.playerbx, 650))
            self.DISPLAYSURF.blit(self.ball, (self.ballx, self.bally))
            self.DISPLAYSURF.blit(self.randNumLabelA, (20, 15))
            self.DISPLAYSURF.blit(self.randNumLabelB, (450, 15))


            pygame.display.update()
            self.fpsClock.tick(self.FPS)

            for event in pygame.event.get():

                if event.type == QUIT:
                    # self.AgentA.model.save('models/AgentA.h5')
                    # self.AgentB.model.save('models/AgentB.h5')
                    pygame.quit()
                    sys.exit()



if __name__ == "__main__":
    tennis = tennis(fps=70)
    tennis.reset()
    tennis.render()
