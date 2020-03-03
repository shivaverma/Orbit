# Orbit

Orbit is a open-source project and a collection of reinforcement learning environments. If you want to contribute to this project by creating your own environment then please drop a mail to shivajbd@gmail.com. You can know how to create an environment through [this](https://towardsdatascience.com/create-your-own-reinforcement-learning-environment-beb12f4151ef) blog: 

Orbit contains following RL environments as of today.

---
## Environment 1: Paddle

### Author: [Shiva Verma](https://www.linkedin.com/in/shiva-verma/)

The task is to hit the ball with paddle. Inbuilt `turtle` library is used to create the environment.

<img src=environments/paddle/wall.gif width="400">

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
---

## Environment 2: Jump

### Author: [Vinod Kumar](https://www.linkedin.com/in/vinodkumar96/)

The task to dodge the box from moving balls. Inbuilt `turtle` library is used to create the environment.

<img src=environments/jump/wall.gif width="600">

### Action space (2)

`0` - Jump.

`1` - Do nothing.

### State space (13)

- y position of box.
- X and Y position of all moving ball.

### Reward function

- `+5` when box dodge a ball.
- `+.1` for each time step.

### Episode termination

- Episode ends when box touchs a ball.
---

## Environment 3: Cars (Coming Soon...)

### Author: [Himanshu Verma](https://www.linkedin.com/in/himanshu-verma-bba8b610b/)

