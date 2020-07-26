# Author: Sathish Kumar E

import pygame
import sys
import os
from random import randint
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE,K_LEFT,K_RIGHT,K_SPACE,K_a,K_d
from math import sin, cos, pi , inf

LIVES = 5


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
                    surface (pygame.Surface): The surface that is to be rotated.
                    angle (float): Rotate by this angle.
                    pivot (tuple, list, pygame.math.Vector2): The pivot point.
                    offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(
        surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


class Plank:
    PLANK_WIDTH = 150
    PLANK_HEIGHT = 30

    def __init__(self,WIN_WIDTH,WIN_HEIGHT):
        self.WIN_WIDTH = WIN_WIDTH
        self.WIN_HEIGHT = WIN_HEIGHT
        self.xvel = 1
        self.rect = pygame.Rect(0, 0, self.PLANK_WIDTH, self.PLANK_HEIGHT)
        self.rect.center = (WIN_WIDTH/2, WIN_HEIGHT-50)
        self.cannon = pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'imgs', 'cannon.png')),
            (80, 110)
        )

    def move(self):
        if self.rect.right >= self.WIN_WIDTH or self.rect.left <= 0:
            if abs(self.xvel)<5:
                self.xvel = -1.3*self.xvel
            else:
                self.xvel = -self.xvel
        self.rect.left += self.xvel

    def draw(self, win, angle):
        self.move()
        pygame.draw.rect(win, (100, 100, 100), self.rect)
        x, y = self.rect.center
        rotated_img, new_rect = rotate(
            self.cannon, angle, (x, y), pygame.math.Vector2(0, -30))
        win.blit(rotated_img, new_rect.topleft)


class Ball:
    MAX_RADIUS = 25
    MIN_RADIUS = 5

    def __init__(self,WIN_WIDTH,max_y):
        self.WIN_WIDTH = WIN_WIDTH
        self.radius = 25
        self.center = [
            randint(self.MAX_RADIUS, WIN_WIDTH-self.MAX_RADIUS), randint(max_y-100, max_y-50)]
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255,0,0), (25, 25), self.radius)
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=self.center)
        self.yvel = 5

    def move(self):
        self.rect.move_ip(0, self.yvel)

    def draw(self, win):
        self.move()
        win.blit(self.surf, self.rect)


class Bullet:
    VEL = 10

    def __init__(self, x, y, angle,WIN_WIDTH):
        self.WIN_WIDTH = WIN_WIDTH
        self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (247, 136, 25), (10, 10), 10)
        self.mask = pygame.mask.from_surface(self.surf)
        x, y = x+50*sin(pi*(angle/180)), y-50*cos(pi*(angle/180))
        self.rect = self.surf.get_rect(center=(x, y))
        self.dx = self.VEL*sin(pi*(angle/180))
        self.dy = -self.VEL*cos(pi*(angle/180))

    def move(self):
        if self.rect.left <= 0 or self.rect.right >= self.WIN_WIDTH:
            self.dx = -self.dx
        self.rect.move_ip(self.dx, self.dy)

    def draw(self, win):
        self.move()
        win.blit(self.surf, self.rect)




class Cannon:
    WIN_WIDTH = 600
    WIN_HEIGHT = 600
    FPS = 30
    # ADDBALL = pygame.USEREVENT + 1
    def __init__(self):
        pygame.font.init()
        pygame.init()
        self.STAT_FONT = pygame.font.SysFont("comicsans", 30)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Cannon")
        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.last_ball = 0


        self.plank = Plank(self.WIN_WIDTH,self.WIN_HEIGHT)
        self.angle = 0
        self.lives = LIVES
        self.score = 0
        self.balls = list()
        for i in range(3):
            b = Ball(self.WIN_WIDTH,self.last_ball)
            self.balls.append(b)
            self.last_ball = b.center[1]

        self.bullets = list()
        self.shoot_counter = 5
        # self.ball_counter = 60



    def draw_frame(self):
        self.WIN.fill((0, 0, 0))
        pygame.draw.line(self.WIN, (100, 100, 100), (0, self.WIN_HEIGHT-150), (self.WIN_WIDTH, self.WIN_HEIGHT-150))
        for ball in self.balls:
            ball.draw(self.WIN)
        for bullet in self.bullets:
            bullet.draw(self.WIN)
        self.plank.draw(self.WIN, self.angle)

        score_label = self.STAT_FONT.render("Score: " + str(self.score), 1, (255, 255, 255))
        self.WIN.blit(score_label, (self.WIN_WIDTH - score_label.get_width() - 15, 10))
        lives_label = self.STAT_FONT.render("Lives: " + str(self.lives), 1, (255, 255, 255))
        self.WIN.blit(lives_label, (15, 10))

    def game_loop(self):
        hit = False
        life_down = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # elif event.type == self.ADDBALL:
                # self.balls.append(Ball(self.WIN_WIDTH))
        # self.ball_counter-=1
        
        # Detect collision
        for i, bullet in enumerate(self.bullets):
            for j, ball in enumerate(self.balls):
                offset_x = bullet.rect.x - ball.rect.x
                offset_y = bullet.rect.y - ball.rect.y
                overlap = ball.mask.overlap(bullet.mask, (offset_x, offset_y))
                if overlap:
                    self.balls.pop(j)
                    self.bullets.pop(i)
                    del ball
                    del bullet
                    self.score += 1
                    hit = True
                    break
        # lost a life
        for index, ball in enumerate(self.balls):
            if ball.rect.center[1]+ball.radius >= self.WIN_HEIGHT-150:
                self.balls.pop(index)
                del ball
                self.lives -= 1
                life_down = True
                break
        # delete bullets out of the screen
        for index, bullet in enumerate(self.bullets):
            if bullet.rect.bottom <= 0:
                self.bullets.pop(index)
                del bullet
                break
        while len(self.balls)<3:
            b = Ball(self.WIN_WIDTH,self.last_ball)
            self.balls.append(b)
            self.last_ball = b.center[1]

        self.shoot_counter -= 1
        return hit,life_down

    def play(self):
        while True:
            self.clock.tick(self.FPS)
            
            hit, life_down = self.game_loop()
            
            # input from user
            keys = pygame.key.get_pressed()
            if (keys[K_d] or keys[pygame.K_RIGHT]) and self.angle < 70:
                self.angle += 3
            elif (keys[K_a] or keys[pygame.K_LEFT]) and self.angle > -70:
                self.angle -= 3
            if self.shoot_counter < 0 and keys[pygame.K_SPACE]:
                self.shoot_counter = 5
                x, y = self.plank.rect.center
                self.bullets.append(Bullet(x, y, self.angle,self.WIN_WIDTH))
            
            # game termination condition 
            if self.lives < 0:
                pygame.quit()
                sys.exit()

            self.draw_frame()
            pygame.display.update()
        pygame.quit()

    def reset(self):
        self.plank.__init__(self.WIN_WIDTH,self.WIN_HEIGHT)
        self.angle = 0
        self.lives = LIVES
        self.score = 0
        self.balls = list()
        self.last_ball = 0
        for i in range(3):
            b = Ball(self.WIN_WIDTH,self.last_ball)
            self.balls.append(b)
            self.last_ball = b.center[1]

        self.bullets = list()
        self.shoot_counter = 5
        # self.ball_counter = 60
        
        ball_cor = list()
        for ball in self.balls:
            ball_cor.append(ball.rect.center[0]/self.WIN_WIDTH)
            ball_cor.append(ball.rect.center[1]/self.WIN_HEIGHT)
        state = [
        self.plank.rect.center[0]/self.WIN_WIDTH,
        sin(self.angle),
        *ball_cor
        ]
        
        
        return state

    def step(self,action):      

        self.reward = 0
        self.done = 0

        # left
        if action == 0:
            self.reward -=.1
            if self.angle > -70:
                self.angle-=3
            
        # right
        elif action == 1:
            self.reward -=.1
            if self.angle < 70:
                self.angle+=3
            
        # shoot
        elif action == 2:
            self.reward -=.5
            if self.shoot_counter < 0:
                self.shoot_counter = 5
                x, y = self.plank.rect.center
                self.bullets.append(Bullet(x, y, self.angle,self.WIN_WIDTH))
        
        if self.lives < 0 :
            self.reset()

        hit, life_down = self.game_loop()

        if hit:
            self.reward += 5
        if life_down:
            self.reward -= 5
        if self.lives<0:
            self.done = True

        ball_cor = list()
        for ball in self.balls:
            ball_cor.append(ball.rect.center[0]/self.WIN_WIDTH)
            ball_cor.append(ball.rect.center[1]/self.WIN_HEIGHT)
        state = [
        self.plank.rect.center[0]/self.WIN_WIDTH,
        sin(self.angle),
        *ball_cor
        ]
        
        

######## remove this later #########################################################
        self.draw_frame()
        pygame.display.update()
        # self.clock.tick(self.FPS)


        return self.reward , state , self.done

                    


if __name__ == '__main__':
    env = Cannon()
    env.play()