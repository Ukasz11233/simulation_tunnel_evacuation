from enum import Enum
from settings import WIDTH, BOARD_WIDTH

class LayerType(Enum):
    STATIC = 0
    POSITION = 1
    DYNAMIC = 2
    OBSTACLE = 3

class ObstacleType(Enum):
    NONE = 0
    WALL = 1
    EXIT = 2


CELL_SIZE = WIDTH // BOARD_WIDTH