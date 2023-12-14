# WINDOW SIZE
WIDTH = 1200
HEIGHT = 700

SCALE = 4
SPEED = 6


# BOARD SIZE
BOARD_WIDTH = 150 * SCALE 
BOARD_HEIGHT = 39 * SCALE
BOTTOM_TUNNEL_HEIGHT = 4 * SCALE
TOP_TUNNEL_HEIGHT = 12 * SCALE
PATH_WIDTH = 2 * SCALE
PATH_HEIGHT = 23 * SCALE

MARGIN = 30 * SCALE


#EXIT -- bottom left of board
EXIT_WIDTH = 2 * SCALE
EXIT_HEIGHT = 6 * SCALE
EXIT_X = 0
EXIT_Y = BOARD_HEIGHT


#BUS POSITION
BUS_TOP_LEFT_X = BOARD_WIDTH // 4
BUS_TOP_LEFT_Y = TOP_TUNNEL_HEIGHT // 2
BUS_LENGTH = 13 * SCALE
BUS_WIDTH = int(3* SCALE)

BUS_EXIT_BUFFOR = 4
EVACUATORS = 7 * BUS_EXIT_BUFFOR


#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


#LOGIC VALUES
ALFA = 0.1 #DYNAMIC
BETA = 3 #STATIC
DYNAMIC_INCREMENT = 0.01 * SPEED

SMOKE_SPEED_REDUCTION = 0.5 