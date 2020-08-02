# Orbit

Orbit is a open-source project and a collection of reinforcement learning environments. If you want to contribute to this project by creating your own environment then please drop a mail to shivajbd@gmail.com. You can know how to create an environment through [this](https://towardsdatascience.com/create-your-own-reinforcement-learning-environment-beb12f4151ef) blog: 

### Requirements

- **`python`** - `3.7`
- **`keras`** -  `2.4.3`
- **`tensorflow`** -  `2.2.0`

Chekout `random_policy.py` to see how to use a environment. Orbit contains following RL environments as of today.

---

# Environment 1: Paddle

### Author: [Shiva Verma](https://www.linkedin.com/in/shiva-verma/)

The task is to take the ball on paddle. Inbuilt `turtle` library is used to create the environment.

<img src=Paddle/wall.gif width="400">

**Action space (3)**

- **`0`** - move paddle to left
- **`1`** - do nothing
- **`2`** - move paddle to right

**State space (5)**

- x position of paddle
- x and y position of ball 
- x and y velocity of ball

**Reward function**

- **`+3.0`** - when paddle hit the ball
- **`-3.0`** - when ball touchs the ground
- **`-0.1`** - when paddle moves

**Episode termination**

- Episode ends when ball touchs the ground.

# Environment 2: Jump

### Author: [Vinod Kumar](https://www.linkedin.com/in/vinodkumar96/)

The task to dodge the kangaroo from moving balls. Inbuilt `turtle` library is used to create the environment.

<img src=Jump/wall.gif width="600">

**Action space (2)**

- **`0`** - jump
- **`1`** - do nothing

**State space (13)**

- y position of kangaroo
- x and y position of all moving ball

**Reward function**

- **`+5.0`** - when kangaroo dodge a ball
- **`-1.0`** - for each jump
- **`+0.1`** - for each time step 

**Episode termination**

- Episode ends when kangaroo touchs a ball.

# Environment 3: Cannon 

### Author: [Sathish Kumar](https://www.linkedin.com/in/sathish-kumar-elangovan-1a5379168/)

The task to hit the dropping balls. `pygame` library is used to create the environment.

<img src=Cannon/wall.gif width="400">

**Action space (4)**

- **`0`** - rotate left
- **`1`** - rotate right
- **`2`** - shoot bullet
- **`3`** - do nothing

**State space (8)**

- x position of cannon
- x and y position of all balls
- sin of angle of cannon

**Reward function**

- **`+5.0`** - hitting the bullet
- **`-0.5`** - for shooting bullet
- **`-0.1`** - for rotating canon 
- **`-5.0`** - episode termination 

**Episode termination**

- Episode ends when a ball touchs the line.
