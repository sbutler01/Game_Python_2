
#import general-use packages
import pygame as pg
import random
import math
import sys
from os import path

from parameters import *

class Game_Start:

		#initialize game
	def __init__(self):
		#game starts running when initialized
		#initialize the game and sounds
		pg.init()
		pg.mixer.init()

		#set up basic display stuff
		self.screen = pg.display.set_mode((width, height))
		pg.display.set_caption(title)
		self.font = pg.font.match_font(font)
		#set game clock
		self.clock = pg.time.Clock()
		#set game running
		self.running = True
		#load data from other files
		self.load()
		#set the level of the game
		self.level_play = 0

	def load(self):
		self.dir = path.dirname(__file__)
		self.spritesheet = SpriteSheet(path.join(self.dir, spritesheet_01))

	def draw(self):
		self.screen.fill(color_background)
		self.sprites_all.draw(self.screen)

		self.write('get to the end!', 25, red, width/2, height-30)

		pg.display.flip()

	def write(self, text, size, color, x, y):
		font = pg.font.Font(self.font, size)
		text_write = font.render(text, True, color)
		text_rect = text_write.get_rect()
		text_rect.midtop = (int(x),int(y))
		self.screen.blit(text_write,text_rect)

	def screen_start(self):

		pg.mixer.music.load(path.join(self.dir, 'music_opening.wav'))
		pg.mixer.music.play()

		self.screen.fill(black)
		self.write(title, 50, white, width/2, height/4)
		self.write("Left/Right Arrows = Move", 25, white, width/2, (height/4) + 55)
		self.write("Space/Up Arrow = Jump", 25, white, width/2, (height/4) + 80)
		self.write("Down Arrow = Drop Through Platform", 25, white, width/2, (height/4) + 105)
		self.write("press number key to select level", 25, white, width/2, (height/4) + 140)
		self.write("Levels:   1   2   3", 25, white, width/2, (height/4) + 200)

		pg.display.flip()
		self.wait()

	def wait(self):
		self.waiting = True
		while self.waiting:
			self.clock.tick(framerate)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.waiting = False
					self.running = False
					self.level_play = 0
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_1:
						self.waiting = False
						pg.mixer.music.fadeout(500)
						self.level_play = 1
					elif event.key == pg.K_2:
						self.waiting = False
						pg.mixer.music.fadeout(500)
						self.level_play = 2
					elif event.key == pg.K_3:
						self.waiting = False
						pg.mixer.music.fadeout(500)
						self.level_play = 3


class Game:

	#initialize game
	def __init__(self):
		#game starts running when initialized
		#initialize the game and sounds
		pg.init()
		pg.mixer.init()

		#set up basic display stuff
		self.screen = pg.display.set_mode((width, height))
		pg.display.set_caption(title)
		self.font = pg.font.match_font(font)
		#set game clock
		self.clock = pg.time.Clock()
		#set game running
		self.running = True
		#load data from other files
		self.load()
		#set the level of the game
		self.level_play = 0
		#determine whether you've already died to start music
		self.died_already = False


	def load(self):
		self.dir = path.dirname(__file__)
		self.spritesheet = SpriteSheet(path.join(self.dir, spritesheet_01))

	#start a new game
	def new(self, checkpoint):
		#create new set of sprites
		#can set beginning parameters like score
		self.screen = pg.display.set_mode((width, height))
		self.platforms_added = checkpoint
		self.gameoverscreen = False


		if level_music == 1 and not self.died_already:
			self.spritesheet_enemies_1 = SpriteSheet(path.join(self.dir, spritesheet_enemies_1))
			self.spritesheet_platforms_1 = SpriteSheet(path.join(self.dir, spritesheet_platforms_1))
			self.spritesheet_background_1 = SpriteSheet(path.join(self.dir, spritesheet_background_1))

			pg.mixer.music.load(path.join(self.dir, 'music_game_1.wav'))
			pg.mixer.music.set_volume(0.2)
			pg.mixer.music.play(loops = -1)


		elif level_music == 2 and not self.died_already:
			self.spritesheet_enemies_1 = SpriteSheet(path.join(self.dir, spritesheet_enemies_1))
			self.spritesheet_platforms_1 = SpriteSheet(path.join(self.dir, spritesheet_platforms_1))
			self.spritesheet_background_1 = SpriteSheet(path.join(self.dir, spritesheet_background_1))

			pg.mixer.music.load(path.join(self.dir, 'music_game_2.wav'))
			pg.mixer.music.set_volume(0.8)
			pg.mixer.music.play(loops = -1)

		elif level_music == 3 and not self.died_already:
			self.spritesheet_enemies_1 = SpriteSheet(path.join(self.dir, spritesheet_enemies_1))
			self.spritesheet_platforms_1 = SpriteSheet(path.join(self.dir, spritesheet_platforms_1))
			self.spritesheet_platforms_2 = SpriteSheet(path.join(self.dir, spritesheet_platforms_2))
			self.spritesheet_background_1 = SpriteSheet(path.join(self.dir, spritesheet_background_1))

			pg.mixer.music.load(path.join(self.dir, 'music_game_3.wav'))
			pg.mixer.music.set_volume(0.2)
			pg.mixer.music.play(loops = -1)

		self.sprites_all = pg.sprite.LayeredUpdates()
		self.platforms_onscreen = pg.sprite.Group()
		self.enemies_onscreen = pg.sprite.Group()
		self.background_onscreen = pg.sprite.Group()
		self.projectiles_onscreen = pg.sprite.Group()

		for position in platforms_all[self.platforms_added]:
			Platform(self,*position)

		count = 0
		for enemy in enemypositions_all[self.platforms_added]:
			Enemy(self,Platform(self,*platforms_all[self.platforms_added][enemy]),enemytypes_all[self.platforms_added][count], enemypos_all[self.platforms_added][count])
			count += 1

		Background(self,-300,0)

		self.Player = Player(self)
		#add counter to measure distance traveled
		self.add_platforms_right = False
		self.add_platforms_up = False
		self.distance_since_added = (width+1)/2

		self.on_moving_platform = False


		#start running the game
		self.run()

	def run(self):
		#determine whether the game is being played
		self.playing = True

		while self.playing:
			#set the clock ticking
			self.clock.tick(framerate)
			self.events()
			self.update()
			self.draw()

	def update(self):
		#update sprites
		self.sprites_all.update()
		#detect collision while fallings
		self.distance_since_added += self.Player.velocity.x

		#defines conditions to land on a platform
		if self.Player.velocity.y >= 0 and not self.Player.fall_through and not self.Player.death:

			self.Player.rect.y += 1
			contact_platform = pg.sprite.spritecollide(self.Player, self.platforms_onscreen, False)
			self.Player.rect.y -= 1

			if contact_platform and contact_platform[0].movement_x != 0:
					self.Player.position.x += contact_platform[0].velocity_x
					self.on_moving_platform = True

			if contact_platform and contact_platform[0].movement_y != 0:
					self.Player.position.y += contact_platform[0].velocity_y
					self.on_moving_platform = True

			if self.on_moving_platform:
				self.velocity_player = self.Player.velocity.x
				self.Player.velocity.x = contact_platform[0].velocity_x

			if level_music == 3:
				if contact_platform and contact_platform[0].ice:
					self.Player.player_friction = player_friction_ice
					self.Player.player_acceleration = player_acceleration_ice
				elif contact_platform or self.Player.velocity.x < 5:
					self.Player.player_friction = player_friction_snow
					self.Player.player_acceleration = player_acceleration_snow

			if contact_platform and self.Player.position.y < (contact_platform[0].rect.top + (0.3*self.Player.rect.height))\
			 and not self.Player.scrambling:
				platform_lowest = contact_platform[0]

				for collision in contact_platform:
					if collision.rect.top < platform_lowest.rect.top:
						platform_lowest = collision

				if self.Player.position.x < platform_lowest.rect.right and self.Player.position.x > platform_lowest.rect.left:

					self.Player.position.y = contact_platform[0].rect.top
					self.Player.velocity.y = 0
					self.Player.jumping = False

			#scrmable up if you're close to the top of a platform
			elif contact_platform and self.Player.position.y < (contact_platform[0].rect.top + self.Player.rect.height):

				self.Player.jumping = False
				self.Player.scrambling = True

				platform_lowest = contact_platform[0]

				for collision in contact_platform:
					if collision.rect.top < platform_lowest.rect.top:
						platform_lowest = collision

				if self.Player.position.x > platform_lowest.rect.right:
					self.Player.rightfacing = False

				if self.Player.position.x < platform_lowest.rect.left:
					self.Player.rightfacing = True

				if self.Player.frame_current == 0:
					self.Player.position.y = contact_platform[0].rect.top+(self.Player.rect.height*1/3)
					self.Player.velocity.y = 0
					self.Player.velocity.x = 0

				elif self.Player.frame_current == 1:
					self.Player.position.y = contact_platform[0].rect.top+(self.Player.rect.height*1/5)
					if self.Player.position.x > platform_lowest.rect.right:
						self.Player.position.x -= (self.Player.rect.height*1/2)
					if self.Player.position.x < platform_lowest.rect.left:
						self.Player.position.x += (self.Player.rect.height*1/2)
					self.Player.velocity.y = 0
					self.Player.velocity.x = 0

				elif self.Player.frame_current == 2:
					self.Player.position.y = contact_platform[0].rect.top
					if self.Player.position.x > platform_lowest.rect.right - (self.Player.rect.height*1/2):
						self.Player.position.x -= (self.Player.rect.height*1/2)
					if self.Player.position.x < platform_lowest.rect.left + (self.Player.rect.height*1/2):
						self.Player.position.x += (self.Player.rect.height*1/2)
					self.Player.velocity.y = 0
					self.Player.velocity.x = 0


		#Player dies when touching enemy
		if not self.Player.death and level_music != 3:
			contact_enemy = pg.sprite.spritecollide(self.Player, self.enemies_onscreen, False)
			if contact_enemy:
				contact_enemy_mask = pg.sprite.spritecollide(self.Player, self.enemies_onscreen, False, pg.sprite.collide_mask)
				if contact_enemy_mask:
						self.Player.velocity.y = -10
						self.Player.death = True

		if level_music == 3:
			for enemy in self.enemies_onscreen:
				if enemy.firing:
					Projectile(self,enemy)
					enemy.firing = False

			contact_projectile = pg.sprite.spritecollide(self.Player, self.projectiles_onscreen, False)
			if contact_projectile:
				contact_projectile_mask = pg.sprite.spritecollide(self.Player,self.projectiles_onscreen,False,pg.sprite.collide_mask)
				if contact_projectile_mask:
					self.Player.velocity.y = -10
					self.Player.death = True

			for projectile in self.projectiles_onscreen:
				if projectile.position.y > height+10:
					projectile.kill()


		#move screen with player (slightly faster if it needs to catch up)
		if self.Player.rect.right >= width*1.1/2 and self.Player.velocity.x > 0:
			self.Player.position.x -= int(1.2*self.Player.velocity.x)
			count = 0
			for position in self.platforms_onscreen:
				position.rect.x -= int(1.2*self.Player.velocity.x)
				if position.movement_x != 0:
					position.xrange[0] -= int(1.2*self.Player.velocity.x)
					position.xrange[1] -= int(1.2*self.Player.velocity.x)
				if self.Player.position.x > (position.rect.right - width/2):
					count += 1
				if count == len(self.platforms_onscreen):
					self.add_platforms_right = True
				#test how close the player is to the end of the section
			for enemy in self.enemies_onscreen:
				enemy.position -= (int(1.2*self.Player.velocity.x),0)

			for background in self.background_onscreen:
				background.rect.x -= int(1.2*background.speed*self.Player.velocity.x)

			for projectile in self.projectiles_onscreen:
				projectile.position.x -= int(1.2*self.Player.velocity.x)

		elif self.Player.rect.right >= width*1/2 and self.Player.velocity.x > 0:
			self.Player.position.x -= self.Player.velocity.x
			count = 0
			for position in self.platforms_onscreen:
				position.rect.x -= int(self.Player.velocity.x)
				if position.movement_x != 0:
					position.xrange[0] -= int(self.Player.velocity.x)
					position.xrange[1] -= int(self.Player.velocity.x)
				#test how close the player is to the end of the section
				if self.Player.position.x > (position.rect.right - width/2):
					count += 1
				if count == len(self.platforms_onscreen):
					self.add_platforms_right = True
				if position.rect.right < -width:
					position.kill()
			for enemy in self.enemies_onscreen:
				enemy.position -= (int(self.Player.velocity.x),0)
				if enemy.rect.right < -width:
					enemy.kill()
			#kill platforms if they're too far back
			for background in self.background_onscreen:
				background.rect.x -= int(background.speed*self.Player.velocity.x)
				if background.rect.right < -(1.5*width):
					background.kill()

			for projectile in self.projectiles_onscreen:
				projectile.position.x -= int(self.Player.velocity.x)
				if projectile.rect.right < -(1.5*width):
					projectile.kill()


		if self.Player.rect.right <= width*0.25 and self.Player.velocity.x < 0:
			self.Player.position.x -= int(1.2*self.Player.velocity.x)
			for position in self.platforms_onscreen:
				position.rect.x -= int(1.2*self.Player.velocity.x)
				if position.movement_x != 0:
					position.xrange[0] -= int(1.2*self.Player.velocity.x)
					position.xrange[1] -= int(1.2*self.Player.velocity.x)
			for enemy in self.enemies_onscreen:
				enemy.position -= (int(1.2*self.Player.velocity.x),0)

			for background in self.background_onscreen:
				background.rect.x -= int(1.2*background.speed*self.Player.velocity.x)

			for projectile in self.projectiles_onscreen:
				projectile.position.x -= int(1.2*self.Player.velocity.x)

		elif self.Player.rect.right <= width*0.3 and self.Player.velocity.x < 0:
			self.Player.position.x -= self.Player.velocity.x
			for position in self.platforms_onscreen:
				position.rect.x -= int(self.Player.velocity.x)
				if position.movement_x != 0:
					position.xrange[0] -= int(self.Player.velocity.x)
					position.xrange[1] -= int(self.Player.velocity.x)
			for enemy in self.enemies_onscreen:
				enemy.position -= (int(self.Player.velocity.x),0)

			for background in self.background_onscreen:
				background.rect.x -= int(background.speed*self.Player.velocity.x)

			for projectile in self.projectiles_onscreen:
				projectile.position.x -= int(self.Player.velocity.x)

		if self.on_moving_platform:
			self.Player.velocity.x = self.velocity_player
			self.on_moving_platform = False

		if int(self.Player.velocity.x) >= 0:
				background_farthest = 0
				count = 0
				for background in self.background_onscreen:
					if background.rect.right > background_farthest:
						background_farthest = background.rect.right
					count += 1
					if count == len(self.background_onscreen) and self.Player.position.x + width > background_farthest:
						Background(self, background_farthest,0)


		if self.add_platforms_right and self.platforms_added < len(platforms_all) - 1:

			self.platforms_added += 1

			platforms_stationary = [i for i in platforms_all[self.platforms_added] if i[4] is None]
			platforms_moving = [i for i in platforms_all[self.platforms_added] if i[4] is not None]

			position_platforms_stationary_add = [(x+width,y,w,h,i,j,k) for (x,y,w,h,i,j,k) in platforms_stationary]
			position_platforms_moving_add = [(x+width,y,w,h,(sx+width,ex+width),j,k) for (x,y,w,h,(sx,ex),j,k) in platforms_moving]

			for position in position_platforms_stationary_add:
				Platform(self,*position)

			for position in position_platforms_moving_add:
				Platform(self,*position)

			count = 0
			for enemy in enemypositions_all[self.platforms_added]:
				Enemy(self,Platform(self,*position_platforms_stationary_add[enemy]),enemytypes_all[self.platforms_added][count], enemypos_all[self.platforms_added][count])
				count += 1

			self.add_platforms_right = False
			self.distance_since_added = 0

		if self.Player.rect.top > 2*height:

			self.died_already = True

			if self.distance_since_added > width/2:
				self.new(self.platforms_added)
			elif self.platforms_added > 0:
				self.new(self.platforms_added - 1)
			else:
				self.new(0)

			self.playing = False

		#activate enemies if the get too close
		if int(self.Player.velocity.x) != 0:
			for enemy in self.enemies_onscreen:
				if enemy.player_close_starting:
					if math.sqrt((enemy.position - self.Player.position)*(enemy.position - self.Player.position)) < width/2:
						enemy.player_close = True
				if enemy.type == 1 and self.Player.position.x > enemy.position.x:
					enemy.rightfacing = True
				elif enemy.type == 1:
					enemy.rightfacing = False
				if level_music == 3 and self.Player.position.x > enemy.position.x:
					enemy.rightfacing = True
				elif level_music == 3:
					enemy.rightfacing = False



	def events(self):
		for event in pg.event.get():
			
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
					pg.mixer.music.stop()
				if self.gameoverscreen:
					self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.Player.jump()
				if event.key == pg.K_UP:
					self.Player.jump()

			if event.type == pg.KEYUP:
				if event.key == pg.K_SPACE:
					self.Player.jump_cut()
				if event.key == pg.K_UP:
					self.Player.jump_cut()


	def draw(self):
		self.screen.fill(color_background)
		self.sprites_all.draw(self.screen)

		self.write('get to the end!', 25, red, width/2, height-30)

		pg.display.flip()

	def write(self, text, size, color, x, y):
		font = pg.font.Font(self.font, size)
		text_write = font.render(text, True, color)
		text_rect = text_write.get_rect()
		text_rect.midtop = (int(x),int(y))
		self.screen.blit(text_write,text_rect)

	#define the gameover screen
	def screen_gameover(self):

		self.gameoverscreen = True

		if not self.running:
			return

		self.screen.fill(black)
		self.write("Game Over", 50, white, width/2, height/4)
		self.write("press number key to select level", 25, white, width/2, (height/4) + 65)
		self.write("Levels:   1   2   3", 25, white, width/2, (height/4) + 125)

		pg.display.flip()
		self.wait()

	#wait for some kind of button input
	def wait(self):
		self.waiting = True
		while self.waiting:
			self.clock.tick(framerate)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.waiting = False
					self.running = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_1:
						self.waiting = False
						pg.mixer.music.fadeout(500)
						if self.level_play != 1:
							self.died_already = False
						self.level_play = 1
					elif event.key == pg.K_2:
						self.waiting = False
						pg.mixer.music.fadeout(500)
						if self.level_play != 2:
							self.died_already = False
						self.level_play = 2
					elif event.key == pg.K_3:
						self.waiting = False
						pg.mixer.music.fadeout(500)
						if self.level_play != 3:
							self.died_already = False
						self.level_play = 3


#create a game object
g = Game_Start()
g.screen_start()

#use this to import the new level
if g.level_play == 1:
	from sprites_1 import *
	level_music = 1

elif g.level_play == 2:
	from sprites_2 import *
	level_music = 2

elif g.level_play == 3:
	from sprites_3 import *
	level_music = 3

elif g.level_play == 0:
	sys.exit(0)

g = Game()

while g.running:

	if g.level_play == 1:
		from sprites_1 import *
		level_music = 1

	elif g.level_play == 2:
		from sprites_2 import *
		level_music = 2

	elif g.level_play == 3:
		from sprites_3 import *
		level_music = 3

	g.new(0)
	g.screen_gameover()

pg.quit()
