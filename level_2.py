#basic visual parameters
title = "The Adventures of Mr. Mrew"
font = 'arial'

width = 1200
height = 600
framerate = 60

spritesheet_01 = "spritesheet_player_right.png"
spritesheet_platforms_1 = "spritesheet_platforms_2.jpg"
spritesheet_enemies_1 = "spritesheet_enemies_2.png"
spritesheet_background_1 = "spritesheet_background_2.png"



#colors using rgb definitions
white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

color_background = white
background_layer = 1
color_platforms = black
platform_layer = 2

#player properties
player_size = (30,40)
player_acceleration = 2
player_friction = 0.4
player_airres = 0.02
player_gravity = 0.5
player_jump = 20
player_position_start = (100,100)
player_layer = 3

enemy_speed = 5
enemy_layer = 3

#platform properties
position_platforms_0 = [(50,400,1800,10,None,None,None),
						(1900, 400, 400, 10,None,None,None),
						(1950,200,100,10,None,None,None),
						(2150,200,100,10,None,None,None)]

position_enemies_0 = [0,0,2,3]
type_enemies_0 = [0,0,1,1]
position_enemy_pos_0 = [1000,1500,0,0]

position_platforms_1 = [(0,400,1800,10,None,None,None),
							(800,550,100,10,None,None,None)]

position_enemies_1 = [0,1]
type_enemies_1 = [2,2]
position_enemy_pos_1 = [800,0]

platforms_all = [position_platforms_0,position_platforms_1]
enemypositions_all = [position_enemies_0,position_enemies_1]
enemytypes_all = [type_enemies_0,type_enemies_1]
enemypos_all = [position_enemy_pos_0,position_enemy_pos_1]

