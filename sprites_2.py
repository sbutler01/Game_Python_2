
#import general packages
import pygame as pg

#import game packages
from level_2 import *
import math

vec = pg.math.Vector2

class SpriteSheet:
	#loads and parses spritesheets
	def __init__(self,filename):
		self.spritesheet = pg.image.load(filename).convert()

	#grab image from the sheet
	def get_image(self,x,y,w,h):
		image = pg.Surface((w,h))
		image.blit(self.spritesheet, (0,0), (x,y,w,h))
		return image

#player sprite
class Player(pg.sprite.Sprite):
	def __init__(self, game):

		self._layer = player_layer
		self.groups = game.sprites_all

		self.game = game
		pg.sprite.Sprite.__init__(self, self.groups)
		#sprites appear every 1000 spaces and are 500 long
		#this is reversed from the other direction
		#try to trim more depending on hitbox
		self.load_images()

		self.image = self.frames_rightwalking[1]
		self.rect = self.image.get_rect()
		self.rect.center = player_position_start

		#movement parameters
		self.walking = False
		self.jumping = False
		self.rightfacing = True
		self.scrambling = False
		#the left-facing variable is chagned by the arrow keys
		self.frame_current = 0
		self.last_update = 0

		#the scrmable animation hasn't started yet
		self.scramble_starting = True

		self.position = vec(player_position_start)
		self.velocity = vec(0,0)
		self.acceleration = vec(0,0)

		#set whether the player lands on platforms
		self.fall_through = False
		self.death = False

	def load_images(self):


		#make the sizes a standard number so the size of the map can be changed
		self.image_01 = self.game.spritesheet.get_image(200,0,800,500)
		self.image_01 = pg.transform.scale(self.image_01,(80,50))

		self.image_02 = self.game.spritesheet.get_image(1120,0,800,500)
		self.image_02 = pg.transform.scale(self.image_02,(80,50))

		self.image_03 = self.game.spritesheet.get_image(2000,0,800,475)
		self.image_03 = pg.transform.scale(self.image_03,(80,47))

		self.image_04 = self.game.spritesheet.get_image(2850,0,800,500)
		self.image_04 = pg.transform.scale(self.image_04,(80,50))

		self.image_05 = self.game.spritesheet.get_image(3750,0,800,500)
		self.image_05 = pg.transform.scale(self.image_05,(80,50))

		self.image_06 = self.game.spritesheet.get_image(4600,0,850,500)
		self.image_06 = pg.transform.scale(self.image_06,(85,50))

		self.image_07 = self.game.spritesheet.get_image(210,500,800,500)
		self.image_07 = pg.transform.scale(self.image_07,(80,50))

		self.image_08 = self.game.spritesheet.get_image(1130,500,800,500)
		self.image_08 = pg.transform.scale(self.image_08,(80,50))

		self.image_09 = self.game.spritesheet.get_image(1975,500,825,500)
		self.image_09 = pg.transform.scale(self.image_09,(82,50))

		self.image_10 = self.game.spritesheet.get_image(2800,500,875,500)
		self.image_10 = pg.transform.scale(self.image_10,(87,50))

		self.image_11 = self.game.spritesheet.get_image(3690,500,850,500)
		self.image_11 = pg.transform.scale(self.image_11,(85,50))

		self.image_12 = self.game.spritesheet.get_image(4600,500,850,500)
		self.image_12 = pg.transform.scale(self.image_12,(85,50))

		self.frames_rightstanding = [self.image_02]

		self.frames_rightwalking = [self.image_01,self.image_02,self.image_03,
									self.image_04,self.image_05,self.image_06,
									self.image_07,self.image_08,self.image_09,
									self.image_10,self.image_11,self.image_12]

		for frame in self.frames_rightstanding:
			color_bg = frame.get_at((5,5))
			frame.set_colorkey(color_bg)

		self.frames_leftstanding = []

		for frame in self.frames_rightstanding:
			self.frames_leftstanding.append(pg.transform.flip(frame, True, False))

		for frame in self.frames_rightwalking:
			color_bg = frame.get_at((5,5))
			frame.set_colorkey(color_bg)
		
		self.frames_leftwalking = []

		for frame in self.frames_rightwalking:
			self.frames_leftwalking.append(pg.transform.flip(frame, True, False))

		self.jump_right_01 = self.game.spritesheet.get_image(2630,6275,925,590)
		self.jump_right_01 = pg.transform.scale(self.jump_right_01,(92,59))

		self.jump_right_02 = self.game.spritesheet.get_image(3600,6325,950,425)
		self.jump_right_02 = pg.transform.scale(self.jump_right_02,(95,42))

		self.jump_right_03 = self.game.spritesheet.get_image(4600,6290,855,455)
		self.jump_right_03 = pg.transform.scale(self.jump_right_03,(85,45))

		self.frames_jump_right = [self.jump_right_01, self.jump_right_02, self.jump_right_03]

		for frame in self.frames_jump_right:
			color_bg = frame.get_at((5,5))
			frame.set_colorkey(color_bg)

		self.frames_jump_left = []

		for frame in self.frames_jump_right:
			self.frames_jump_left.append(pg.transform.flip(frame, True, False))

		self.scrambling_01 = self.game.spritesheet.get_image(1900,6225,727,650)
		self.scrambling_01 = pg.transform.scale(self.scrambling_01,(73,65))

		self.scrambling_02 = self.game.spritesheet.get_image(900,6350,910,450)
		self.scrambling_02 = pg.transform.scale(self.scrambling_02,(91,45))

		self.scrambling_03 = self.game.spritesheet.get_image(200,6400,650,450)
		self.scrambling_03 = pg.transform.scale(self.scrambling_03,(65,45))

		self.frames_scrambling_right = [self.scrambling_01,self.scrambling_02,self.scrambling_03]

		for frame in self.frames_scrambling_right:
			color_bg = frame.get_at((5,5))
			frame.set_colorkey(color_bg)

		self.frames_scrambling_left = []

		for frame in self.frames_scrambling_right:
			self.frames_scrambling_left.append(pg.transform.flip(frame, True, False))

		self.frames_falling_right = [self.jump_right_03]

		self.frames_falling_left = []

		for frame in self.frames_falling_right:
			self.frames_falling_left.append(pg.transform.flip(frame, True, False))


	#define a player's jump
	def jump(self):

		self.rect.y += 1
		collision_platform = pg.sprite.spritecollide(self, self.game.platforms_onscreen, False)
		self.rect.y -= 1

		if collision_platform and not self.jumping:
			self.velocity.y = -player_jump
			self.jumping = True

	def jump_cut(self):
		if self.jumping:
			if self.velocity.y < -5:
				self.velocity.y = -5



	def update(self):

		self.animate()
		self.acceleration = vec(0,player_gravity)
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_LEFT] and not self.scrambling:
			self.rightfacing = False
			self.walking = True
			self.acceleration.x = -player_acceleration
		elif keys_pressed[pg.K_RIGHT] and not self.scrambling:
			self.rightfacing = True
			self.walking = True
			self.acceleration.x = player_acceleration
		else:
			self.walking = False

		if keys_pressed[pg.K_DOWN]:
			self.fall_through = True
		else:
			self.fall_through = False


		#apply friction, air resistance and acceleration
		self.acceleration.x -= (self.velocity.x * player_friction)
		self.acceleration.y -= (self.velocity.y * player_airres)

		if abs(self.velocity.x) < 0.1:
			self.velocity.x = 0

		self.velocity += self.acceleration
		self.position += self.velocity + (0.5 * self.acceleration)



		
		self.rect.midbottom = self.position

	def animate(self):
		time_current = pg.time.get_ticks()

		if int(self.velocity.y) > 0 and self.rightfacing:
			self.image = self.frames_falling_right[0]

		elif int(self.velocity.y) > 0:
			self.image = self.frames_falling_left[0]

		if self.scrambling and self.rightfacing:

			if self.scramble_starting:
				self.time_scrambling = time_current
				self.scramble_starting = False

			if 0 <= (time_current - self.time_scrambling) <= 100:
				self.frame_current = 0
			elif 100 < (time_current - self.time_scrambling) <= 200:
				self.frame_current = 1
			elif 200 < (time_current - self.time_scrambling) <= 300:
				self.frame_current = 2
			else:
				self.scramble_starting = True
				self.scrambling = False

			self.image = self.frames_scrambling_right[self.frame_current]

		elif self.scrambling and not self.rightfacing:

			if self.scramble_starting:
				self.time_scrambling = time_current
				self.scramble_starting = False

			if 0 <= (time_current - self.time_scrambling) <= 100:
				self.frame_current = 0
			elif 100 < (time_current - self.time_scrambling) <= 200:
				self.frame_current = 1
			elif 200 < (time_current - self.time_scrambling) <= 300:
				self.frame_current = 2
			else:
				self.scramble_starting = True
				self.scrambling = False

			self.image = self.frames_scrambling_left[self.frame_current]

		elif self.jumping and self.rightfacing:
			if int(self.velocity.y) < -10:
				self.image = self.frames_jump_right[0]

			elif int(self.velocity.y) > -10 and int(self.velocity.y) < 0:
				self.image = self.frames_jump_right[1]

			else:
				self.image = self.frames_jump_right[2]

			self.rect = self.image.get_rect()

		elif self.jumping:
			if int(self.velocity.y) < -10:
				self.image = self.frames_jump_left[0]

			elif int(self.velocity.y) > -10 and int(self.velocity.y) < 0:
				self.image = self.frames_jump_left[1]

			else:
				self.image = self.frames_jump_left[2]

			self.rect = self.image.get_rect()

		elif self.walking and not self.jumping:
			if (time_current - self.last_update) > 100:
				self.last_update = time_current
				self.frame_current = (self.frame_current + 1) % len(self.frames_rightwalking)

				if self.velocity.x > 0:
					self.image = self.frames_rightwalking[self.frame_current]
				else:
					self.image = self.frames_leftwalking[self.frame_current]

				self.rect = self.image.get_rect()

		if not self.walking and not self.jumping and self.rightfacing and not self.scrambling and int(self.velocity.y) <= 0 :
			self.image = self.frames_rightwalking[self.frame_current]
			self.rect = self.image.get_rect()

		if not self.walking and not self.jumping and not self.rightfacing and not self.scrambling and int(self.velocity.y) <= 0 :
			self.image = self.frames_leftwalking[self.frame_current]
			self.rect = self.image.get_rect()

		self.mask = pg.mask.from_surface(self.image)




class Platform(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, xranges, yranges, time):
		self._layer = platform_layer
		self.groups = game.sprites_all, game.platforms_onscreen
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.game.spritesheet_platforms_1.get_image(0,0,int(67*(w/h)),67)
		self.image = pg.transform.scale(self.image,(w,h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.xrange = xranges
		self.yrange = yranges
		self.time = time

		#define all the movement stuff
		if self.xrange is not None:
			self.xrange = vec(self.xrange)
			self.movement_x = self.xrange[0] - x
			self.velocity_x = int(self.movement_x/(self.time*framerate))
		else:
			self.movement_x = 0
		if self.yrange is not None:
			self.yrange = vec(self.yrange)
			self.movement_y = self.yrange[0] - y
			self.velocity_y = int(self.movement_y/(self.time*framerate))
		else:
			self.movement_y = 0

	def update(self):
		#move the platforms
		if self.movement_x != 0:
			self.rect.x += self.velocity_x
			if self.rect.x < self.xrange[0]:
				self.velocity_x = -int(self.movement_x/(self.time*framerate))
			elif self.rect.x > self.xrange[1]:
				self.velocity_x = int(self.movement_x/(self.time*framerate))

		if self.movement_y != 0:
			self.rect.y += self.velocity_y
			if self.rect.y < self.yrange[0]:
				self.velocity_y = -int(self.movement_y/(self.time*framerate))
			elif self.rect.y > self.yrange[1]:
				self.velocity_y = int(self.movement_y/(self.time*framerate))


class Enemy(pg.sprite.Sprite):

	#initialize the enemy
	def __init__(self, game, plat, type_enemy, pos):
		self._layer = enemy_layer
		self.groups = game.sprites_all, game.enemies_onscreen
		pg.sprite.Sprite.__init__(self,self.groups)
		self.game = game
		self.plat = plat
		self.type = type_enemy
		self.pos = pos

		self.frame_current = 0

		self.load_images()

		self.image = self.frames_blue[0]
		self.rect = self.image.get_rect()

		self.rightfacing = True
		self.player_close = False
		self.player_close_starting = True
		self.rightfacing = False

		#start him a certain distance down the platform
		self.rect.x = self.plat.rect.left + self.pos
		self.rect.bottom = self.plat.rect.top
		self.position = vec(self.rect.midbottom)
		# self.velocity = 1
		self.velocity = 0
		self.velocity_2 = 0

	def load_images(self):

		self.image_stationary = self.game.spritesheet_enemies_1.get_image(0,617,158,200)
		self.image_stationary = pg.transform.scale(self.image_stationary,(64,80))

		self.image_stationary_orange = self.game.spritesheet_enemies_1.get_image(0,415,158,200)
		self.image_stationary_orange = pg.transform.scale(self.image_stationary_orange,(64,80))

		self.image_stationary_blue = self.game.spritesheet_enemies_1.get_image(0,217,158,200)
		self.image_stationary_blue = pg.transform.scale(self.image_stationary_blue,(64,80))

		self.image_stationary_red = self.game.spritesheet_enemies_1.get_image(0,10,158,200)
		self.image_stationary_red = pg.transform.scale(self.image_stationary_red,(64,80))

		self.image_transforming_1 = self.game.spritesheet_enemies_1.get_image(155,605,198,190)
		self.image_transforming_1 = pg.transform.scale(self.image_transforming_1,(80,76))

		self.image_transforming_1_orange = self.game.spritesheet_enemies_1.get_image(155,405,198,190)
		self.image_transforming_1_orange = pg.transform.scale(self.image_transforming_1_orange,(80,76))

		self.image_transforming_1_blue = self.game.spritesheet_enemies_1.get_image(155,205,198,190)
		self.image_transforming_1_blue = pg.transform.scale(self.image_transforming_1_blue,(80,76))

		self.image_transforming_1_red = self.game.spritesheet_enemies_1.get_image(155,-2,198,190)
		self.image_transforming_1_red = pg.transform.scale(self.image_transforming_1_red,(80,76))

		self.image_transforming_2 = self.game.spritesheet_enemies_1.get_image(350,605,175,200)
		self.image_transforming_2 = pg.transform.scale(self.image_transforming_2,(71,80))

		self.image_transforming_2_orange = self.game.spritesheet_enemies_1.get_image(350,406,175,200)
		self.image_transforming_2_orange = pg.transform.scale(self.image_transforming_2_orange,(71,80))

		self.image_transforming_2_blue = self.game.spritesheet_enemies_1.get_image(350,207,175,200)
		self.image_transforming_2_blue = pg.transform.scale(self.image_transforming_2_blue,(71,80))

		self.image_transforming_2_red = self.game.spritesheet_enemies_1.get_image(350,-1,175,200)
		self.image_transforming_2_red = pg.transform.scale(self.image_transforming_2_red,(71,80))

		self.image_alert = self.game.spritesheet_enemies_1.get_image(527,605,175,200)
		self.image_alert = pg.transform.scale(self.image_alert,(71,80))

		self.image_alert_orange = self.game.spritesheet_enemies_1.get_image(527,406,175,200)
		self.image_alert_orange = pg.transform.scale(self.image_alert_orange,(71,80))

		self.image_alert_blue = self.game.spritesheet_enemies_1.get_image(527,207,175,200)
		self.image_alert_blue = pg.transform.scale(self.image_alert_blue,(71,80))

		self.image_alert_red = self.game.spritesheet_enemies_1.get_image(527,-1,175,200)
		self.image_alert_red = pg.transform.scale(self.image_alert_red,(71,80))

		self.frames_blue = [self.image_stationary, self.image_stationary_blue, self.image_transforming_1_blue, self.image_transforming_2_blue, self.image_alert_blue]

		self.frames_orange = [self.image_stationary, self.image_stationary_orange, self.image_transforming_1_orange, self.image_transforming_2_orange, self.image_alert_orange]

		self.frames_red = [self.image_stationary, self.image_stationary_red, self.image_transforming_1_red, self.image_transforming_2_red, self.image_alert_red]

		for frame in self.frames_blue:
			color_bg = frame.get_at((0,0))
			frame.set_colorkey(color_bg)

		for frame in self.frames_orange:
			color_bg = frame.get_at((0,0))
			frame.set_colorkey(color_bg)

		for frame in self.frames_red:
			color_bg = frame.get_at((0,0))
			frame.set_colorkey(color_bg)

		self.frames_orange_left = []
		self.frames_blue_left = []
		self.frames_red_left = []

		for frame in self.frames_orange:
			self.frames_orange_left.append(pg.transform.flip(frame, True, False))

		for frame in self.frames_blue:
			self.frames_blue_left.append(pg.transform.flip(frame, True, False))

		for frame in self.frames_red:
			self.frames_red_left.append(pg.transform.flip(frame, True, False))


	def update(self):

		self.animate()

		self.rect.midbottom = self.position

		if self.frame_current == 4:
			if self.type == 0:

				self.position += (self.velocity,0)
				self.rect.midbottom = self.position

				if self.rect.left < self.plat.rect.left + self.pos - (width/2):
					self.velocity = enemy_speed
					self.rightfacing = True
				elif self.rect.right > self.plat.rect.left + self.pos + (width/2):
					self.velocity = -enemy_speed
					self.rightfacing = False

			elif self.type == 1:

				self.position += (0,self.velocity)
				self.rect.midbottom = self.position

				if self.rect.top <= 0:
					self.velocity = enemy_speed
				elif self.rect.bottom > height:
					self.velocity = -enemy_speed

			elif self.type == 2:

				self.position += (self.velocity,self.velocity_2)
				self.rect.midbottom = self.position

				if self.rect.top <= 0:
					self.velocity_2 = enemy_speed
				elif self.rect.bottom > height:
					self.velocity_2 = -enemy_speed

				if self.rect.left < self.plat.rect.left + self.pos - (width/2):
					self.velocity = enemy_speed
					self.rightfacing = True
				elif self.rect.right > self.plat.rect.left + self.pos + (width/2):
					self.velocity = -enemy_speed
					self.rightfacing = False


	def animate(self):

		time_current_enemy = pg.time.get_ticks()

		if self.player_close_starting:
			self.frame_current = 0

		if self.player_close:
			if self.player_close_starting:
				self.time_player_close = time_current_enemy
				self.player_close_starting = False

			if (time_current_enemy - self.time_player_close) <= 400:
				self.frame_current = 0
			elif 400 < (time_current_enemy - self.time_player_close) <= 800:
				self.frame_current = 1
			elif 800 < (time_current_enemy - self.time_player_close) <= 1000:
				self.frame_current = 2
			elif 1000 < (time_current_enemy - self.time_player_close) <= 1200:
				self.frame_current = 3
			else:
				self.frame_current = 4
				self.player_close = False
				self.velocity = -enemy_speed
				self.velocity_2 = -enemy_speed


		if self.type == 0:
			if not self.rightfacing:
				self.image = self.frames_blue_left[self.frame_current]
			else:
				self.image = self.frames_blue[self.frame_current]

		elif self.type == 1:
			if not self.rightfacing:
				self.image = self.frames_orange_left[self.frame_current]
			else:
				self.image = self.frames_orange[self.frame_current]

		elif self.type == 2:
			if not self.rightfacing:
				self.image = self.frames_red_left[self.frame_current]
			else:
				self.image = self.frames_red[self.frame_current]


		self.rect = self.image.get_rect()
		self.mask = pg.mask.from_surface(self.image)

class Background(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = background_layer
		self.groups = game.sprites_all, game.background_onscreen
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.game.spritesheet_background_1.get_image(5,0,3160,463)
		self.image = pg.transform.scale(self.image,(4095,600))
		#let's brighten the image slightly
		self.brighten = 50
		self.image.fill((125,125,125), special_flags = pg.BLEND_RGB_ADD)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.speed = 0.3
