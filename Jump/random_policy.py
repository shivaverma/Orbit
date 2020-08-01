import numpy as np
from jump import Jump

env = Jump()
np.random.seed(0)

def random_policy(episode):

    action_space = 2
    state_space = 13
    max_steps = 1000

    for e in range(episode):
        state = env.reset()
        score = 0

        for i in range(max_steps):
            action = np.random.randint(action_space)
            reward, next_state, done = env.step(action)
            score += reward
            state = next_state
            if done:
                print("episode: {}/{}, score: {}".format(e, episode, score))
                break


if __name__ == '__main__':

    random_policy(10)