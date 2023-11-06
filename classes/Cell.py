import pygame
from common import *
from settings import *


class CellAdapter:
    def __init__(self, _screen) -> None:
        self.screen = _screen
        self.isUsed = False
        self.value = 0
        pass

    def setValue(self, _value):
        self.isUsed = True
        self.value = _value
        return

    def getValue(self):
        return self.value

    def isSet(self):
        return self.isUsed
    
    def move(self, positionXY):
        self.isUsed = True
        return



class ObstacleCell(CellAdapter):
    def __init__(self, _screen, _isObstacle) -> None:
        super().__init__(_screen)


class ManCell(CellAdapter):
    def __init__(self, _screen, x, y) -> None:
        super().__init__(_screen)
        self.currentX = x
        self.currentY = y

    def move(self, positionXY):
        self.currentX = positionXY[0]
        self.currentY = positionXY[1]
        return super().move(positionXY)