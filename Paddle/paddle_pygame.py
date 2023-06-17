import pygame
import sys
import numpy as np
from time import sleep

# Constants for the screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Paddle Constants
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20

# Ball Constants
BALL_DIAMETER = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Paddle():
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up some properties
        self.done = False
        self.reward = 0
        self.hit, self.miss = 0, 0

        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set up the paddle
        self.paddle = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

        # Set up the ball
        self.ball = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_DIAMETER, BALL_DIAMETER)
        self.ball_dx = 3
        self.ball_dy = -3

        # Set up the font for the score display
        self.font = pygame.font.Font(None, 36)

    def paddle_left(self):
        if self.paddle.left > 0:
            self.paddle.left -= 20

    def paddle_right(self):
        if self.paddle.right < SCREEN_WIDTH:
            self.paddle.right += 20

    def run_frame(self):

        # sleep(0.017) # To slow down the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle_left()
        if keys[pygame.K_RIGHT]:
            self.paddle_right()

        # Update ball position
        self.ball.left += self.ball_dx
        self.ball.top += self.ball_dy

        # Ball and wall collision
        if self.ball.left <= 0 or self.ball.right >= SCREEN_WIDTH:
            self.ball_dx *= -1
        if self.ball.top <= 0:
            self.ball_dy *= -1

        # Ball and paddle collision
        if self.ball.colliderect(self.paddle) and self.ball_dy > 0:
            self.ball_dy *= -1
            self.hit += 1
            self.reward += 3

        # Ball misses paddle
        if self.ball.top >= SCREEN_HEIGHT:
            self.ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.miss += 1
            self.reward -= 3
            self.done = True

        # Draw everything
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.paddle)
        pygame.draw.circle(self.screen, RED, self.ball.center, BALL_DIAMETER / 2)

        # Render the score
        hit_percentage = self.hit / (self.hit + self.miss) * 100 if self.hit + self.miss > 0 else 0
        score_text = self.font.render("Hits: {}   Missed: {}".format(self.hit, self.miss), True, WHITE)
        self.screen.blit(score_text, (20, 20))
        stats_text = self.font.render("Accuracy: {:.2f}%".format(hit_percentage), True, WHITE)
        self.screen.blit(stats_text, (SCREEN_WIDTH - stats_text.get_width() - 20, 20))

        # Flip the display
        pygame.display.flip()

    # ------------------------ AI control ------------------------

    # 0 move left
    # 1 do nothing
    # 2 move right


    def reset(self):
        
        # place the paddle at the center
        self.paddle.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10)

        # place the ball at center vertically but randomly horizontally
        self.ball.center = (np.random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT / 2)

        return [self.paddle.centerx/600, self.ball.centerx/600, self.ball.centery/600, self.ball_dx, self.ball_dy]

    # Step
    def step(self, action):
        self.reward = 0
        self.done = 0
        if action == 0:
            self.paddle_left()
            self.reward -= .1
        if action == 2:
            self.paddle_right()
            self.reward -= .1

        self.run_frame()
        state = [self.paddle.centerx/600, self.ball.centerx/600, self.ball.centery/600, self.ball_dx, self.ball_dy]
        return self.reward, state, self.done
        

if __name__ == "__main__":

    env = Paddle()
    clock = pygame.time.Clock()

    while not env.done:
        env.run_frame()
        clock.tick(60)  # Limit to 60 frames per second
    pygame.quit()

