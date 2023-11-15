from settings import *
from common import *
import pygame
from classes.Layer import *

class Man(Layer):
    def __init__(self, _x, _y, _screen, _speed = SPEED) -> None:
        self.currentX = _x
        self.currentY = _y
        self.screen = _screen
        self.speed = _speed
        pass

    def move(self, positionXY):
        self.draw(BLACK)
        self.currentX = positionXY[0]
        self.currentY = positionXY[1]

    def draw(self, color=GREEN):
        pygame.draw.rect(self.screen, color, (self.currentX*CELL_SIZE, self.currentY, CELL_SIZE, CELL_SIZE))

    def getXYPosition(self):
        return (self.currentX, self.currentY)   
    
    def getSpeed(self):
        return self.speed