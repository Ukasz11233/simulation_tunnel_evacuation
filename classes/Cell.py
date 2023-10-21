import pygame
from common import *
from settings import *
from classes.Layer import *

class Cell:
    def __init__(self, _screen, _isObstacle=False) -> None:
        self.isObstacleFlag = _isObstacle
        self.staticValue = 0
        self.currentX = -1
        self.currentY = -1
        self.cellSize = WIDTH // BOARD_WIDTH
        self.screen = _screen
        self.Layers = [Layer() for _ in range(len(LayerType))]
        pass

    def setObstacle(self, newX, newY):
        self.moveCell(newX, newY)
        self.isObstacleFlag = True

    def isObstacle(self) -> bool:
        return self.isObstacleFlag

    def moveCell(self, newX, newY):
        if (not self.isObstacleFlag):
            self.currentX = newX
            self.currentY = newY

    def draw(self):
        def _drawCellColored(color):
            pygame.draw.rect(self.screen, color, (self.currentX *
                            self.cellSize, self.currentY, self.cellSize, self.cellSize))
        
        if self.isObstacleFlag:
            _drawCellColored(RED)
        else:
            _drawCellColored(GREEN)
