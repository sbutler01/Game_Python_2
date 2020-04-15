#basic visual parameters
title = "The Adventures of Mr. Mrew"
font = 'arial'

width = 1000
height = 600
framerate = 60

spritesheet_01 = "spritesheet_player_right.png"
spritesheet_platforms_1 = "spritesheet_platforms_1.jpg"
spritesheet_enemies_1 = "spritesheet_enemies_1.png"
spritesheet_background_1 = "spritesheet_background_1.png"



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
player_acceleration = 2
player_friction = 0.4
player_airres = 0.02
player_gravity = 0.5
player_jump = 20
player_position_start = (100,100)
player_layer = 3

enemy_speed = 2
enemy_layer = 3

#platform properties
position_platforms_0 = [(50,400,800,10, None, None, None),
						(1000, 550, 500, 10, None, None, None),
						(1600, 300, 300, 10, None, (100,500), 2),
						(2000, 200, 300, 10, None, None, None)]

position_enemies_0 = [1,3]
type_enemies_0 = [0,0]
position_enemy_pos_0 = [250,150]

position_platforms_1 = [(50,300,200,10, None, None, None),
							(400,500,600,10, None, None, None)]

position_enemies_1 = [1,1]
type_enemies_1 = [0,0]
position_enemy_pos_1 = [100,400]


position_platforms_2 = [(0,350,200,10, None, None, None),
						(200,350,200,10, (200,600), None, 2),
						(900,450,200,10, (500,900), None, 2),
						(900,250,200,10, (900,1300), None, 2)]


position_enemies_2 = []
type_enemies_2 = []
position_enemy_pos_2 = []

platforms_all = [position_platforms_0,position_platforms_1,position_platforms_2]
enemypositions_all = [position_enemies_0,position_enemies_1,position_enemies_2]
enemytypes_all = [type_enemies_0,type_enemies_1,type_enemies_2]
enemypos_all = [position_enemy_pos_0,position_enemy_pos_1,position_enemy_pos_2]

