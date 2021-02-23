from keras import Sequential, layers
from keras.optimizers import Adam
from keras.layers import Dense
from collections import deque
import numpy as np


class Network:
    def __init__(self, xmin, xmax, ymin, ymax):
        """
        xmin: 150,
        xmax: 450, 
        ymin: 100, 
        ymax: 600
        """

        self.StaticDiscipline = {
            'xmin': xmin,
            'xmax': xmax,
            'ymin': ymin,
            'ymax': ymax
        }

    def network(self, xsource, ysource=100, Ynew=600, divisor=50):  # ysource will always be 100
        """
        For Network A
        ysource: will always be 100
        xsource: will always be between xmin and xmax (static discipline)

        For Network B
        ysource: will always be 600
        xsource: will always be between xmin and xmax (static discipline)
        """

        while True:
            ListOfXsourceYSource = []
            Xnew = np.random.choice([i for i in range(
                self.StaticDiscipline['xmin'], self.StaticDiscipline['xmax'])], 1)
            #Ynew = np.random.choice([i for i in range(self.StaticDiscipline['ymin'], self.StaticDiscipline['ymax'])], 1)

            source = (xsource, ysource)
            target = (Xnew[0], Ynew)

            #Slope and intercept
            slope = (ysource - Ynew)/(xsource - Xnew[0])
            intercept = ysource - (slope*xsource)
            if (slope != np.inf) and (intercept != np.inf):
                break
            else:
                continue

        #print(source, target)
        # randomly select 50 new values along the slope between xsource and xnew (monotonically decreasing/increasing)
        XNewList = [xsource]

        if xsource < Xnew:
            differences = Xnew[0] - xsource
            increment = differences / divisor
            newXval = xsource
            for i in range(divisor):

                newXval += increment
                XNewList.append(int(newXval))
        else:
            differences = xsource - Xnew[0]
            decrement = differences / divisor
            newXval = xsource
            for i in range(divisor):

                newXval -= decrement
                XNewList.append(int(newXval))

        # determine the values of y, from the new values of x, using y= mx + c
        yNewList = []
        for i in XNewList:
            findy = (slope * i) + intercept  # y = mx + c
            yNewList.append(int(findy))

        ListOfXsourceYSource = [(x, y) for x, y in zip(XNewList, yNewList)]

        return XNewList, yNewList

    def DefaultToPosition(self, x1, x2=300, divisor=50):
        DefaultPositionA = 300
        DefaultPositionB = 300
        XNewList = []
        if x1 < x2:
            differences = x2 - x1
            increment = differences / divisor
            newXval = x1
            for i in range(divisor):
                newXval += increment
                XNewList.append(int(np.floor(newXval)))

        else:
            differences = x1 - x2
            decrement = differences / divisor
            newXval = x1
            for i in range(divisor):
                newXval -= decrement
                XNewList.append(int(np.floor(newXval)))
        return XNewList




class DQN:
    def __init__(self):
        self.learning_rate = 0.001
        self.momentum = 0.95
        self.eps_min = 0.1
        self.eps_max = 1.0
        self.eps_decay_steps = 2000000
        self.replay_memory_size = 500
        self.replay_memory = deque([], maxlen=self.replay_memory_size)
        n_steps = 4000000  # total number of training steps
        self.training_start = 10000  # start training after 10,000 game iterations
        self.training_interval = 4  # run a training step every 4 game iterations
        self.save_steps = 1000  # save the model every 1,000 training steps
        self.copy_steps = 10000  # copy online DQN to target DQN every 10,000 training steps
        self.discount_rate = 0.99
        # Skip the start of every game (it's just waiting time).
        self.skip_start = 90
        self.batch_size = 100
        self.iteration = 0  # game iterations
        self.done = True  # env needs to be reset

        self.model = self.DQNmodel()

        return

    def DQNmodel(self):
        model = Sequential()
        model.add(Dense(64, input_shape=(1,), activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(10, activation='softmax'))
        model.compile(loss='categorical_crossentropy',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def sample_memories(self, batch_size):
        indices = np.random.permutation(len(self.replay_memory))[:batch_size]
        # state, action, reward, next_state, continue
        cols = [[], [], [], [], []]
        for idx in indices:
            memory = self.replay_memory[idx]
            for col, value in zip(cols, memory):
                col.append(value)
        cols = [np.array(col) for col in cols]
        return (cols[0], cols[1], cols[2].reshape(-1, 1), cols[3], cols[4].reshape(-1, 1))

    def epsilon_greedy(self, q_values, step):
        self.epsilon = max(self.eps_min, self.eps_max -
                           (self.eps_max-self.eps_min) * step/self.eps_decay_steps)
        if np.random.rand() < self.epsilon:
            return np.random.randint(10)  # random action
        else:
            return np.argmax(q_values)  # optimal action
