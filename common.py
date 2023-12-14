from enum import Enum
from settings import WIDTH, BOARD_WIDTH


class LayerType(Enum):
    POSITION = 0
    STATIC = 1
    DYNAMIC = 2
    OBSTACLE = 3
    FIRE = 4
    SMOKE = 5

CELL_SIZE = WIDTH // BOARD_WIDTH