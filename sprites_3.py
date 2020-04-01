
#import general packages
import pygame as pg

#import game packages
from level_3 import *

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

		self.image = self.frames_rightwalking[0]
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
		self.player_friction = player_friction
		self.player_acceleration = player_acceleration

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
			self.acceleration.x = -self.player_acceleration
		elif keys_pressed[pg.K_RIGHT] and not self.scrambling:
			self.rightfacing = True
			self.walking = True
			self.acceleration.x = self.player_acceleration
		else:
			self.walking = False

		if keys_pressed[pg.K_DOWN]:
			self.fall_through = True
		else:
			self.fall_through = False


		#apply friction, air resistance and acceleration
		self.acceleration.x -= (self.velocity.x * self.player_friction)
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
		#if x is not an integer, that's a clue to make it slippery
		if x%1 != 0:
			self.ice = True
		else:
			self.ice = False

		if self.ice:
			self.image = self.game.spritesheet_platforms_1.get_image(0,0,int(39*(w/h)),39)
			self.image = pg.transform.scale(self.image,(w,h))
		else:
			self.image = self.game.spritesheet_platforms_2.get_image(0,0,int(39*(w/h)),39)
			self.image = pg.transform.scale(self.image,(w,h))

		self.rect = self.image.get_rect()

		self.rect.x = int(x)
		self.rect.y = y
		self.xrange = xranges
		self.yrange = yranges
		self.time = time

		#define all the movement stuff
		if self.xrange is not None:
			self.xrange = vec(self.xrange)
			self.movement_x = self.xrange[0] - self.xrange[1]
			self.velocity_x = int(self.movement_x/(self.time*framerate))
		else:
			self.movement_x = 0
		if self.yrange is not None:
			self.yrange = vec(self.yrange)
			self.movement_y = self.yrange[0] - self.yrange[1]
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

		if self.type == 0:
			self.image = self.frames_straight_left[0]
		else:
			self.image = self.frames_up_left[0]

		self.rect = self.image.get_rect()

		self.player_close = False
		self.player_close_starting = True
		self.rightfacing = False
		self.firing = False
		self.frame_change = False

		self.frame_before = 0

		#start him a certain distance down the platform
		self.rect.x = self.plat.rect.left + self.pos
		self.rect.bottom = self.plat.rect.top

		if self.type == 0:
			self.rect.x -= 29
		else:
			self.rect.x -= 27

		self.position = vec(self.rect.midbottom)
		# self.velocity = 1

	def load_images(self):

		self.image_stationary = self.game.spritesheet_enemies_1.get_image(7,20,44,37)

		self.image_aiming_1 = self.game.spritesheet_enemies_1.get_image(62,13,42,43)
		self.image_aiming_2 = self.game.spritesheet_enemies_1.get_image(129,13,66,47)

		self.image_firing_straight_1 = self.game.spritesheet_enemies_1.get_image(11,73,44,36)
		self.image_firing_straight_2 = self.game.spritesheet_enemies_1.get_image(74,76,42,34)
		self.image_firing_straight_3 = self.game.spritesheet_enemies_1.get_image(136,70,47,40)
		self.image_firing_straight_4 = self.game.spritesheet_enemies_1.get_image(198,65,50,44)
		self.image_firing_straight_5 = self.game.spritesheet_enemies_1.get_image(260,63,50,46)

		self.image_firing_up_1 = self.game.spritesheet_enemies_1.get_image(68,129,38,40)
		self.image_firing_up_2 = self.game.spritesheet_enemies_1.get_image(120,131,38,38)
		self.image_firing_up_3 = self.game.spritesheet_enemies_1.get_image(173,122,43,47)
		self.image_firing_up_4 = self.game.spritesheet_enemies_1.get_image(228,119,50,50)
		self.image_firing_up_5 = self.game.spritesheet_enemies_1.get_image(290,119,50,51)

		self.frames_straight = [self.image_stationary, self.image_firing_straight_1,self.image_firing_straight_2,
		self.image_firing_straight_3,self.image_firing_straight_4,self.image_firing_straight_5]
		self.frames_up = [self.image_aiming_1, self.image_firing_up_1, self.image_firing_up_2, self.image_firing_up_3, 
		self.image_firing_up_4, self.image_firing_up_5]

		#difference between the left side and the center
		#used to shift the x-coordinate
		self.distance_centers_straight = [29,26,23,33,35,35]
		self.distance_centers_up = [27,23,21,29,35,36]

		for frame in self.frames_straight:
			color_bg = frame.get_at((0,0))
			frame.set_colorkey(color_bg)

		for frame in self.frames_up:
			color_bg = frame.get_at((0,0))
			frame.set_colorkey(color_bg)

		self.frames_straight_left = []
		self.frames_up_left = []

		for frame in self.frames_straight:
			self.frames_straight_left.append(pg.transform.flip(frame, True, False))

		for frame in self.frames_up:
			self.frames_up_left.append(pg.transform.flip(frame, True, False))


	def update(self):

		self.animate()

		self.rect.x = self.plat.rect.left + self.pos
		self.rect.bottom = self.plat.rect.top

		if self.rightfacing:	
			if self.type == 0:
				self.rect.x += self.distance_centers_straight[self.frame_current]
			else:
				self.rect.x += self.distance_centers_up[self.frame_current]
		else:
			if self.type == 0:
				self.rect.x -= self.distance_centers_straight[self.frame_current]
			else:
				self.rect.x -= self.distance_centers_up[self.frame_current]


	def animate(self):

		time_current_enemy = pg.time.get_ticks()

		if self.player_close_starting:
			self.frame_current = 0

		if self.player_close:
			if self.player_close_starting:
				self.time_player_close = time_current_enemy
				self.player_close_starting = False

			self.frame_before = self.frame_current
			if (time_current_enemy - self.time_player_close) <= 200:
				self.frame_current = 1
			elif 200 < (time_current_enemy - self.time_player_close) <= 400:
				self.frame_current = 2
			elif 400 < (time_current_enemy - self.time_player_close) <= 600:
				self.frame_current = 3
				if self.frame_current - self.frame_before != 0:
					self.firing = True
			elif 600 < (time_current_enemy - self.time_player_close) <= 800:
				self.frame_current = 4
			elif 800 < (time_current_enemy - self.time_player_close) <= 1000:
				self.frame_current = 5
			elif 1000 < (time_current_enemy - self.time_player_close) <= 2000:
				self.frame_current = 0
			else:
				self.time_player_close = time_current_enemy

		if self.type == 0:
			if not self.rightfacing:
				self.image = self.frames_straight[self.frame_current]
			else:
				self.image = self.frames_straight_left[self.frame_current]

		elif self.type == 1:
			if not self.rightfacing:
				self.image = self.frames_up[self.frame_current]
			else:
				self.image = self.frames_up_left[self.frame_current]

		self.rect = self.image.get_rect()
		self.mask = pg.mask.from_surface(self.image)


class Background(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = background_layer
		self.groups = game.sprites_all, game.background_onscreen
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.game.spritesheet_background_1.get_image(0,0,3346,1579)
		self.image = pg.transform.scale(self.image,(1271,600))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.speed = 0.5

class Projectile(pg.sprite.Sprite):
	def __init__(self, game, enemy):

		self._layer = enemy_layer
		self.groups = game.sprites_all, game.projectiles_onscreen

		self.game = game
		pg.sprite.Sprite.__init__(self, self.groups)

		self.enemy = enemy
		self.load_image()

		self.rect = self.image.get_rect()

		if self.enemy.rightfacing:
			self.rect.topright = vec(self.enemy.rect.topright) - vec(5,5)
		else:
			self.rect.topright = vec(self.enemy.rect.topleft) + vec(5,5)

		self.projectile_gravity = projectile_gravity
		self.projectile_airres = projectile_airres

		self.position = vec(self.rect.center)

		if self.enemy.type == 0:
			if self.enemy.rightfacing:
				self.velocity = vec(15,-10)
			else:
				self.velocity = vec(-15,-10)

		elif self.enemy.type == 1:
			if self.enemy.rightfacing:
				self.velocity = vec(15,-15)
			else:
				self.velocity = vec(-15,-15)

		self.acceleration = vec(0,0)


	def load_image(self):

		self.image = self.game.spritesheet_enemies_1.get_image(203,39,16,16)

		color_bg = self.image.get_at((0,0))
		self.image.set_colorkey(color_bg)

		self.mask = pg.mask.from_surface(self.image)

	def update(self):

		self.acceleration = vec(0,projectile_gravity)

		self.acceleration.x -= (self.velocity.x * self.projectile_airres)
		self.acceleration.y -= (self.velocity.y * self.projectile_airres)

		self.velocity += self.acceleration
		self.position += self.velocity + (0.5 * self.acceleration)
		
		self.rect.center = self.position









