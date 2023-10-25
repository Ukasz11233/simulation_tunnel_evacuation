import pygame
from common import *
from settings import *
from classes.Layer import *

class Cell:
    def __init__(self, _screen, _isObstacle=False) -> None:
        self.isObstacleFlag = _isObstacle
        self.staticValue = 0
        self.screen = _screen
        self.Layers = [Layer() for _ in range(len(LayerType))]
        pass

    def setObstacle(self):
        self.isObstacleFlag = True

    def isObstacle(self) -> bool:
        return self.isObstacleFlag

