
#import general-use packages
import pygame
import random

#import files for this game
from parameters import *

#initialize the game and sounds
pygame.init()
pygame.mixer.init()

#set up basic display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)

#set game clock
clock = pygame.time.Clock()

#create list of sprites
sprites_all = pygame.sprite.Group()

#get the game running
running = True
while running:
	#start the game clock
	clock.tick(framerate)

	#set up infrastructure for any event
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

	#update the sprite positions
	sprites_all.update()

	screen.fill(black)
	sprites_all.draw(screen)

	pygame.display.flip()

pygame.quit()





