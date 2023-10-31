import pygame
from common import *
from settings import *
from classes.Layer import *

class Cell:
    def __init__(self, _screen, _isObstacle=False) -> None:
        self.isObstacleFlag = _isObstacle
        self.isExitFlag = False
        self.staticValue = 0
        self.screen = _screen
        self.Layers = [Layer() for _ in range(len(LayerType))]
        pass

    def setObstacle(self):
        self.isObstacleFlag = True

    def setExit(self):
        self.isExitFlag = True

    def isExit(self) -> bool:
        return self.isExitFlag

    def isObstacle(self) -> bool:
        return self.isObstacleFlag

    def setLayerVal(self, layerType, value):
        self.Layers[layerType.value].setValue(value)

    def getStaticValue(self):
        return self.Layers[LayerType.STATIC.value].getValue()