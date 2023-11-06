import math
import pygame
from settings import *
from classes.Cell import *
from classes.Layer import *

class Board:
    def __init__(self, _screen) -> None:
        self.screen = _screen
        self.layers = [Layer(self.screen, i) for i in range(len(LayerType))]
        self.createWalls()
        self.createExit()
        self.calcualteStaticLayer()
        self.addPeople()
        pass

    def updateBoardLayers(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.movePeople(x, y)
                for layer in self.layers:
                    layer.drawLayer(x, y)                        

    def createWalls(self):
        self.drawOuterHorizontalWalls()
        self.drawOuterVerticalWalls()
        self.drawInnerHorizontalWalls()
        self.drawInnerVerticalWalls()

    def drawOuterHorizontalWalls(self):
        for x in range(BOARD_WIDTH):
            self.layers[LayerType.OBSTACLE.value].setCellValue(x, 0, ObstacleType.WALL)
            self.layers[LayerType.OBSTACLE.value].setCellValue(x, BOARD_HEIGHT - 1, ObstacleType.WALL)

    def drawInnerHorizontalWalls(self):
        bottomWall = BOARD_HEIGHT - BOTTOM_TUNNEL_HEIGHT - 1
        topWall = TOP_TUNNEL_HEIGHT - 1
        for x in range(PATH_WIDTH, BOARD_WIDTH - PATH_WIDTH):
            self.layers[LayerType.OBSTACLE.value].setCellValue(x, bottomWall, ObstacleType.WALL)
            self.layers[LayerType.OBSTACLE.value].setCellValue(x, topWall, ObstacleType.WALL)

    def drawOuterVerticalWalls(self):
        for y in range(BOARD_HEIGHT):
            self.layers[LayerType.OBSTACLE.value].setCellValue(0, y, ObstacleType.WALL)
            self.layers[LayerType.OBSTACLE.value].setCellValue(BOARD_WIDTH-1, y, ObstacleType.WALL)

    def drawInnerVerticalWalls(self):
        for y in range(TOP_TUNNEL_HEIGHT, PATH_HEIGHT + TOP_TUNNEL_HEIGHT):
            self.layers[LayerType.OBSTACLE.value].setCellValue(PATH_WIDTH, y, ObstacleType.WALL)
            self.layers[LayerType.OBSTACLE.value].setCellValue(BOARD_WIDTH - PATH_WIDTH, y, ObstacleType.WALL)

    def createExit(self):
        for x in range(EXIT_WIDTH):
            for y in range(BOARD_HEIGHT-1, BOARD_HEIGHT - BOTTOM_TUNNEL_HEIGHT, -1):
                self.layers[LayerType.OBSTACLE.value].setCellValue(x, y, ObstacleType.EXIT)

    def calcualteStaticLayer(self):
        calculatedValue = 0
        maxVal = -1
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                calculatedValue = math.sqrt(pow(EXIT_X - x, 2) + pow(EXIT_Y - y, 2))
                self.layers[LayerType.STATIC.value].setCellValue(x, y, calculatedValue)
                maxVal = max(maxVal, calculatedValue)
        print(maxVal) # here I'm printing temporary maxStaticValue which is used as "magic number" in Layer.drawLeyer method 


    def addPeople(self):
        self.layers[LayerType.POSITION.value].setCellValue(100, 50, True)

    def movePeople(self, x, y):
        if(self.layers[LayerType.POSITION.value].getCellValue(x, y) == 0):
            return
        self.layers[LayerType.POSITION.value].move(x, y, self.calculateMove((x, y), 1))

    def calculateMove(self, positionXY, speed):
        x, y = positionXY
        bestMove = float('inf')
        bestPosition = positionXY
        moves = [(x-speed, y), (x+speed, y), (x, y-speed), (x, y+speed)]

        for move_x, move_y in moves:
            if 0 <= move_x < BOARD_WIDTH and 0 <= move_y < BOARD_HEIGHT:
                static_value = self.layers[LayerType.STATIC.value].getCellValue(move_x, move_y)
                print(bestMove, static_value)
                if (not self.layers[LayerType.OBSTACLE.value].getCellValue(move_x, move_y) == ObstacleType.WALL.value) and bestMove > static_value:
                    bestMove = static_value
                    bestPosition = (move_x, move_y)

        return bestPosition
    