import os
import torch
import random
import argparse
import numpy as np
import torch.nn as nn
from cannon import Cannon
import torch.optim as optim
from collections import deque
import matplotlib.pyplot as plt
from model import DQN

np.random.seed(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

weights_prefix = 'canon_episode_'
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
weights_dir = os.path.join(base_path, 'weights')


class Agent:

    def __init__(self, state_space, action_space, inference=0):

        self.action_space = action_space
        self.state_space = state_space
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.gamma = 0.95
        self.batch_size = 32
        self.epsilon_decay = 0.99997
        self.inference = inference
        self.memory = deque(maxlen=100000)
        self.model = DQN(state_space, action_space).to(device)
        if inference:
            checkpoint = "{}/{}{}.pth".format(weights_dir, weights_prefix, inference)
            self.model.load_state_dict(torch.load(checkpoint))
            print("Loaded weights from {}".format(checkpoint))
            self.model.eval()
        self.optimizer = optim.Adam(self.model.parameters())
        self.MSE_loss = nn.MSELoss().to(device)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon and not self.inference:
            return random.randrange(self.action_space)
        state = torch.FloatTensor(state).to(device)
        act_values = self.model(state)
        return torch.argmax(act_values).item()

    def replay(self):

        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = torch.from_numpy(states.squeeze()).float().to(device)
        next_states = torch.from_numpy(next_states.squeeze()).float().to(device)

        self.model.eval()
        next_state_values = self.model(next_states).detach().numpy()
        self.model.train()

        targets = rewards + self.gamma*(np.amax(next_state_values, axis=1))*(1-dones)
        targets_full = self.model(states)
        targets_pred = targets_full.clone()
        targets_full[np.arange(self.batch_size), actions] = torch.from_numpy(targets).float()
       
        # value_pred = self.model(states)
        loss = self.MSE_loss(targets_pred, targets_full)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(env, episode, inference=False):

    loss = []
    action_space = env.action_space
    state_space = env.observation_space
    max_steps = 1000
    agent = Agent(state_space, action_space, inference=inference)
    for e in range(episode):
        state = env.reset()
        state = np.reshape(state, [1, state_space])
        score = 0
        for i in range(max_steps):
            action = agent.act(state)
            reward, next_state, done = env.step(action)
            next_state = np.reshape(next_state, [1, state_space])
            if not inference:
                agent.remember(state, action, reward, next_state, done)
                agent.replay()
            state = next_state    
            score += reward
            if done:
                print("episode: {}/{}, score: {:.2f}, epsilon: {:.2}, steps: {}".format(e, episode, score, agent.epsilon, i))
                break
        loss.append(score)

        if (e+1) % 300 == 0:
            torch.save(agent.model.state_dict(), "{}/{}{}.pth".format(weights_dir, weights_prefix, e+1))

    return loss


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inference', type=int, default=0)
    parser.add_argument('--episodes', type=int, default=50000)
    parser.add_argument('--fps', type=int, default=-1)
    return parser.parse_args()


if __name__ == '__main__':

    args = argparser()
    fps = args.fps
    episodes = args.episodes
    inference = args.inference

    env = Cannon(fps=fps)
    loss = train_dqn(env, episodes, inference=inference)
    plt.plot([i for i in range(episodes)], loss)
    plt.xlabel('episodes')
    plt.ylabel('reward')
    plt.show()
