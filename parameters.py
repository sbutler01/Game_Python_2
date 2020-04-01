import pygame as pg


#basic visual parameters
title = "The Adventures of Mr. Mrew"
font = 'arial'

width = 1000
height = 600
framerate = 60

spritesheet_01 = "spritesheet_player_right.png"

#colors using rgb definitions
white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

color_background = white
color_player = blue
color_platforms = black

class SpriteSheet:
	#loads and parses spritesheets
	def __init__(self,filename):
		self.spritesheet = pg.image.load(filename).convert()

	#grab image from the sheet
	def get_image(self,x,y,w,h):
		image = pg.Surface((w,h))
		image.blit(self.spritesheet, (0,0), (x,y,w,h))
		return image
