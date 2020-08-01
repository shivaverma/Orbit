# Author: Sathish Kumar E

import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_a, K_d
from assets.objects import Ball, Bullet, Plank, rotate
from math import sin, cos, pi , inf
# Game environment class

class Cannon:
	WIN_WIDTH = 600
	WIN_HEIGHT = 600
	FPS = 30

	def __init__(self,graphics=True):
		pygame.font.init()
		pygame.init()
		self.graphics = graphics
		self.STAT_FONT = pygame.font.SysFont("comicsans", 30)
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Cannon")
		self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
		self.last_ball = 0
		self.playing = False
		self.plank = Plank(self.WIN_WIDTH, self.WIN_HEIGHT)
		self.angle = 0
		self.lives = LIVES
		self.score = 0
		self.balls = list()
		for i in range(3):
			b = Ball(self.WIN_WIDTH, self.last_ball)
			self.balls.append(b)
			self.last_ball = b.center[1]

		self.bullets = list()
		self.shoot_counter = 10

	# drawing all the objects to screen(WIN)

	def draw_frame(self):
		self.WIN.fill((0, 0, 0))
		pygame.draw.line(self.WIN, (100, 100, 100), (0,
													 self.WIN_HEIGHT-150), (self.WIN_WIDTH, self.WIN_HEIGHT-150))
		for ball in self.balls:
			ball.draw(self.WIN)
		for bullet in self.bullets:
			bullet.draw(self.WIN)
		self.plank.draw(self.WIN, self.angle)

		score_label = self.STAT_FONT.render(
			"Score: " + str(self.score), 1, (255, 255, 255))

		self.WIN.blit(score_label, ((self.WIN_WIDTH - score_label.get_width())/2, 10))

	# game logic runs in this fuction for each frame
	def game_loop(self):
		hit = False
		life_down = False

		for event in pygame.event.get():
			if event.type == QUIT:           # terminates the game when game window is closed
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:    # terminates the game when esc is pressed
					pygame.quit()
					sys.exit()

		# Detect collision between ball and bullet
		for i, bullet in enumerate(self.bullets):
			for j, ball in enumerate(self.balls):
				offset_x, offset_y = bullet.rect.x - \
					ball.rect.x, bullet.rect.y - ball.rect.y  # calculate offset
				# returns points of overlap
				overlap = ball.mask.overlap(bullet.mask, (offset_x, offset_y))
				if overlap:
					self.balls.pop(j)
					self.bullets.pop(i)
					del ball
					del bullet
					self.score += 1
					hit = True
					break

		# check if lost a life
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

		# creating new balls to fall
		while len(self.balls) < 3:
			b = Ball(self.WIN_WIDTH, self.last_ball)
			self.balls.append(b)
			self.last_ball = b.center[1]

		self.shoot_counter -= 1

		return hit, life_down

	def play(self):
		self.playing = True
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
				self.shoot_counter = 10
				x, y = self.plank.rect.center
				self.bullets.append(Bullet(x, y, self.angle, self.WIN_WIDTH))

			# game termination condition
			if self.lives < 0:
				pygame.quit()
				sys.exit()
			if self.graphics:
				self.draw_frame()           # generates new frame
				pygame.display.update()     # renders the new frame
		pygame.quit()

	# reset the
	def reset(self):
		self.plank.__init__(self.WIN_WIDTH, self.WIN_HEIGHT)
		self.angle = 0
		self.lives = 1
		self.score = 0
		self.balls = list()
		self.last_ball = 0
		for i in range(3):
			b = Ball(self.WIN_WIDTH, self.last_ball)
			self.balls.append(b)
			self.last_ball = b.center[1]

		self.bullets = list()
		self.shoot_counter = 10

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

	def step(self, action):

		self.reward = 0
		self.done = 0

		# left
		if action == 0:
			self.reward -= .1
			if self.angle > -70:
				self.angle -= 3

		# right
		elif action == 1:
			self.reward -= .1
			if self.angle < 70:
				self.angle += 3

		# shoot
		elif action == 2:
			self.reward -= .5
			if self.shoot_counter < 0:
				self.shoot_counter = 10
				x, y = self.plank.rect.center
				self.bullets.append(Bullet(x, y, self.angle, self.WIN_WIDTH))

		# do nothing
		elif action == 3:
			pass

		hit, life_down = self.game_loop()

		if hit:
			self.reward += 5
		if life_down:
			self.reward -= 5
		if self.lives <= 0:
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

		if self.graphics:
			self.clock.tick(self.FPS)
			self.draw_frame()           # generates new frame
			pygame.display.update()     # renders the new frame

		return self.reward, state, self.done


LIVES = 1

if __name__ == '__main__':
	env = Cannon(graphics=True)
	env.play()