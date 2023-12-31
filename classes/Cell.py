import pygame
from common import *
from settings import *
from classes.Layer import *


class Cell:
    def __init__(self, _screen, _isObstacle=False) -> None:
        self.isObstacleFlag = _isObstacle
        self.isTaken = False
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

    def getDynamicValue(self):
        return self.Layers[LayerType.DYNAMIC.value].getValue()
    
    def getFireValue(self):
        pass

    def setFireValue(self, value):
        self.Layers[LayerType.FIRE.value].setValue(value)

    def setSmokeValue(self, value):
        self.Layers[LayerType.SMOKE.value].setValue(value)

    def getFireValue(self):
        return self.Layers[LayerType.FIRE.value].getValue()
    
    def initializeFire(self, value):
        self.Layers[LayerType.FIRE.value].setValue(value)

    def initializeSmoke(self, value):
        self.Layers[LayerType.SMOKE.value].setValue(value)

    def getSmokeValue(self):
        return self.Layers[LayerType.SMOKE.value].getValue()

    def updateLayers(self):
        for layer in self.Layers:
            if layer.value == LayerType.OBSTACLE.value:
                continue

    def isTakenByMan(self) -> bool:
        return self.isTaken
    
    def setTakenByMan(self, flag):
        self.isTaken = flag