# Author: Sathish Kumar E

import pygame
import sys
import os
from random import randint
from pygame.locals import *
from math import sin, cos, pi

WIN_WIDTH = 600
WIN_HEIGHT = 600
FPS = 30
pygame.font.init()
pygame.init()
STAT_FONT = pygame.font.SysFont("comicsans", 30)


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

    def __init__(self):
        self.xvel = 1
        self.rect = pygame.Rect(0, 0, self.PLANK_WIDTH, self.PLANK_HEIGHT)
        self.rect.center = (300, 550)
        self.cannon = pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'imgs', 'cannon.png')),
            (80, 110)
        )

    def move(self):
        if self.rect.right >= WIN_WIDTH or self.rect.left <= 0:
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

    def __init__(self):
        self.radius = 25
        self.center = [
            randint(self.MAX_RADIUS, WIN_WIDTH-self.MAX_RADIUS), randint(-70, -55)]
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (25, 224, 71), (25, 25), self.radius)
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

    def __init__(self, x, y, angle, plank_xvel):
        self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (247, 136, 25), (10, 10), 10)
        self.mask = pygame.mask.from_surface(self.surf)
        x, y = x+50*sin(pi*(angle/180)), y-50*cos(pi*(angle/180))
        self.rect = self.surf.get_rect(center=(x, y))
        self.dx = self.VEL*sin(pi*(angle/180))+plank_xvel
        self.dy = -self.VEL*cos(pi*(angle/180))

    def move(self):
        if self.rect.left <= 0 or self.rect.right >= WIN_WIDTH:
            self.dx = -self.dx
        self.rect.move_ip(self.dx, self.dy)

    def draw(self, win):
        self.move()
        win.blit(self.surf, self.rect)


def draw_frame(win, plank, circles, bullets, angle, score, lives):
    win.fill((0, 0, 0))
    pygame.draw.line(win, (100, 100, 100), (0, 450), (WIN_WIDTH, 450))
    for circle in circles:
        circle.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    plank.draw(win, angle)

    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    lives_label = STAT_FONT.render("Lives: " + str(lives), 1, (255, 255, 255))
    win.blit(lives_label, (15, 10))


if __name__ == '__main__':

    clock = pygame.time.Clock()
    pygame.display.set_caption("Cannon")
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    plank = Plank()
    angle = 0
    lives = 3
    score = 0
    ADDBALL = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDBALL, 2000)
    balls = [Ball()]
    bullets = list()
    shoot_counter = 5

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == ADDBALL:
                balls.append(Ball())
        for i, bullet in enumerate(bullets):
            for j, ball in enumerate(balls):
                offset_x = bullet.rect.x - ball.rect.x
                offset_y = bullet.rect.y - ball.rect.y
                overlap = ball.mask.overlap(bullet.mask, (offset_x, offset_y))
                if overlap:
                    balls.pop(j)
                    bullets.pop(i)
                    del ball
                    del bullet
                    score += 1
                    break
        for index, ball in enumerate(balls):
            if ball.rect.center[1]+ball.radius >= 450:
                balls.pop(index)
                del ball
                lives -= 1
                break
        for index, bullet in enumerate(bullets):
            if bullet.rect.bottom <= 0:
                bullets.pop(index)
                del bullet
                break
        

        if lives < 0:
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and angle < 80:
            angle += 3
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and angle > -80:
            angle -= 3
        if shoot_counter < 0 and keys[pygame.K_SPACE]:
            shoot_counter = 5
            x, y = plank.rect.center
            bullets.append(Bullet(x, y, angle, plank.xvel))
        shoot_counter -= 1

        draw_frame(WIN, plank, balls, bullets, angle, score, lives)
        pygame.display.update()
    pygame.quit()