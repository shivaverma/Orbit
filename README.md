# Orbit

Orbit is a open-source project and a collection of reinforcement learning environments. If you want to contribute to this project by creating your own environment then please drop a mail to shivajbd@gmail.com. You can know how to create an environment through [this](https://towardsdatascience.com/create-your-own-reinforcement-learning-environment-beb12f4151ef) blog: 

### Requirements

- **`python`** - `3.7`
- **`keras`** -  `2.4.3`
- **`tensorflow`** -  `2.2.0`

Orbit contains following RL environments as of today.

---
## Environment 1: Paddle

### Author: [Shiva Verma](https://www.linkedin.com/in/shiva-verma/)

The task is to hit the ball with paddle. Inbuilt `turtle` library is used to create the environment.

<img src=Paddle/wall.gif width="400">

---

**Action space (3)**

- **`0`** - move paddle to left
- **`1`** - do nothing
- **`2`** - move paddle to right

**State space (5)**

- x position of paddle
- x and y position of ball 
- x and y velocity of ball

**Reward function**

|  Reward  | Description |
| :-----------: | :-----------: |
| **+3** | when paddle hit the ball |
| **-3**   | when ball touchs the ground        |
| **-0.1**      | when paddle moves     |

**Episode termination**

- Episode ends when ball touchs the ground.

---

## Environment 2: Jump

### Author: [Vinod Kumar](https://www.linkedin.com/in/vinodkumar96/)

The task to dodge the box from moving balls. Inbuilt `turtle` library is used to create the environment.

<img src=Jump/wall.gif width="600">

**Action space (2)**

- **`0`** - jump
- **`1`** - do nothing

**State space (13)**

- y position of box
- x and y position of all moving ball

**Reward function**

|  Reward  | Description |
| :-----------: | :-----------: |
| **+5** | when box dodge a ball |
| **+0.1**   | for each time step        |

**Episode termination**

- Episode ends when box touchs a ball.

---

## Environment 3: Cannon (Coming Soon...)

### Author: [Sathish Kumar](https://www.linkedin.com/in/sathish-kumar-elangovan-1a5379168/)
