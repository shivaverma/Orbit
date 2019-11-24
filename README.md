# Orbit

Orbit is a open-source project and a collection of reinforcement learning environments. If you want to contribute to this project by creating your own environment then please drop a mail to shivajbd@gmail.com

Orbit contains following RL environments as of today.

# Environment 1: Paddle

### Author: Shiva Verma

The task to hit the ball with paddle. Inbuilt `turtle` library is used to create the environment.

<img src=paddle/wall.gif width="400">

### Action space (3)

`0` - Move paddle to left.

`1` - Do nothing.

`2` - Move paddle to right.

### State space (5)

- X position of paddle.
- X and Y position of ball.
- X and Y velocity of ball.

### Reward function

- `+3` when paddle hit the ball.
- `-3` when ball touchs the ground.
- `-0.1` when paddle moves.

### Episode termination

- Episode ends when ball touchs the ground.
