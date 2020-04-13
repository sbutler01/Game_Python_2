#basic visual parameters
title = "The Adventures of Mr. Mrew"
font = 'arial'

width = 1200
height = 600
framerate = 60

spritesheet_01 = "spritesheet_player_right.png"
spritesheet_platforms_1 = "spritesheet_platforms_3.jpg"
spritesheet_platforms_2 = "spritesheet_platforms_3_2.jpg"
spritesheet_enemies_1 = "spritesheet_enemies_3.png"
spritesheet_background_1 = "spritesheet_background_3.png"



#colors using rgb definitions
white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellowgreen = (154,205,50)
olivedrab = (107,142,35)

color_background = white
background_layer = 1
color_platforms = black
platform_layer = 2

#player properties
player_size = (30,40)

player_acceleration_snow = 2
player_acceleration_ice = 0.75

player_acceleration = 2

player_friction_snow = 0.4
player_friction_ice = 0.075

player_friction = 0.4

player_airres = 0.02
player_gravity = 0.5
player_jump = 20
player_position_start = (100,100)
player_layer = 3

enemy_speed = 2
enemy_layer = 3

projectile_gravity = 0.5
projectile_airres = 0.01

#platform properties
position_platforms_0 = [(50.1,500,600,10,None,None,None),
						(900,300,600,10,None,None,None),
						(1300.1,550,200,10,None,None,None)]

position_enemies_0 = [1,1]
type_enemies_0 = [1,0]
position_enemy_pos_0 = [450,525]

position_platforms_1 = [(0,100,100,10,None,None,None),
						(200,400,600,10,None,None,None),
						(900,150,150,10,None,None,None),
						(1300,300,150,10,None,None,None),
						(1000.1,550,100,10,(800,1300),None,3)]

position_enemies_1 = [2,2,3,3]
type_enemies_1 = [1,0,0,1]
position_enemy_pos_1 = [25,75,25,75]


platforms_all = [position_platforms_0,position_platforms_1]
enemypositions_all = [position_enemies_0,position_enemies_1]
enemytypes_all = [type_enemies_0,type_enemies_1]
enemypos_all = [position_enemy_pos_0,position_enemy_pos_1]
