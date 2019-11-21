Orbit is a open-source project and a collection of reinforcement learning environments.

# Environment 1: Paddle

Library used - Turtle

In this environment, the task is to hit the ball with paddle. 

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
