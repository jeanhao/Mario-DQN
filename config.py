# -------------------------------------------
#     Global constants and objects
# -------------------------------------------
FRAMERATE = 120

WIDTH = 1000
HEIGHT = 540
SCREEN_SIZE = (WIDTH, HEIGHT)

IMG_WIDTH = 200
IMG_HEIGHT = 108

ENEMY_TICKS = [25, 30, 50, 75, 100, 150]
ENEMY_X_POS = [WIDTH / 5, WIDTH / 6, WIDTH / 7, 4 * WIDTH / 5, 5 * WIDTH / 6, 6 * WIDTH / 7]
ENEMY_Y_POS = [HEIGHT / 2, 6 * HEIGHT / 7]

TEXT_COLOR = (10, 10, 10)

TRAIN = True

# -------------------------------------------
#         Mario-related constants
# -------------------------------------------
if FRAMERATE == 60:
	MARIO_X_ACC = 0.5
	MARIO_FRICTION = 0.92
	MARIO_JUMP_VEL = -10.75
	MARIO_GRAVITY = 0.4
else:
	MARIO_X_ACC = 0.25
	MARIO_FRICTION = 0.93
	MARIO_JUMP_VEL = -8
	MARIO_GRAVITY = 0.2



# -------------------------------------------
#       Shell-related constants
# -------------------------------------------
if FRAMERATE == 60:
	SHELL_GRAVITY = 0.5
	SHELL_X_VEL = 3
	SHELL_Y_VEL = 2
else:
	SHELL_GRAVITY = 0.5
	SHELL_X_VEL = 1.5
	SHELL_Y_VEL = 2
