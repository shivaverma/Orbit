from keras import Sequential, layers
from keras.optimizers import Adam
from keras.layers import Dense
from collections import deque
import numpy as np


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
