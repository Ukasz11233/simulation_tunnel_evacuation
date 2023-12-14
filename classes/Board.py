import math
import pygame
from settings import *
from classes.Cell import *
import random
import numpy as np


class Board:
    def __init__(self, _screen) -> None:
        self.boardWidth = BOARD_WIDTH
        self.boardHeight = BOARD_HEIGHT
        self.screen = _screen
        self.board = [[Cell(self.screen) for _ in range(self.boardHeight)]
                      for _ in range(self.boardWidth)]
        self.createWalls()
        self.createExit()
        self.createBus()
        self.calcualteStaticLayer()
        self.inicializeDynamicLayer()
        print("STATIC VAL", self.board[0][0].getStaticValue(), self.board[0][BOARD_HEIGHT-1].getStaticValue(), self.board[BOARD_WIDTH-1][EXIT_Y-1].getStaticValue())
        pass

    def updateBoardLayers(self):
        for x in range(self.boardWidth):
            for y in range(self.boardHeight):
                self.board[x][y].updateLayers()
                self.drawCell(x, y)

    def drawCell(self, x, y):
        def _drawCellColored(color):
            color = tuple(max(0, min(value, 255)) for value in color)
            pygame.draw.rect(self.screen, color, (x * CELL_SIZE, y, CELL_SIZE, CELL_SIZE))

        def _checkIfCellIsOnPath(x, y):
            return (y > TOP_TUNNEL_HEIGHT + PATH_HEIGHT or y < TOP_TUNNEL_HEIGHT or x < PATH_WIDTH or x > BOARD_WIDTH - PATH_WIDTH)

        if self.board[x][y].isObstacle():
            _drawCellColored(RED)
        elif self.board[x][y].isExit():
            _drawCellColored(GREEN)
        elif _checkIfCellIsOnPath(x, y):
            scaledBlue = abs(255 - (self.board[x][y].getStaticValue() * 255))
            scaledRed = (self.board[x][y].getFireValue() * 255) // 100
            scaledGray = (self.board[x][y].getSmokeValue() * 255) // 100
            _drawCellColored((scaledRed, 0, scaledBlue - scaledGray))
        if self.board[x][y].getDynamicValue() > 0:
            scaledBlue = abs(255 - (self.board[x][y].getStaticValue() * 255) // self.tmpMaxStaticVal)
            dynamiValueColor = scaledBlue - (self.board[x][y].getDynamicValue() * 255) // 100
            _drawCellColored((0, 0, dynamiValueColor))

    def createWalls(self):
        def _drawOuterHorizontalWalls(self):
            for x in range(BOARD_WIDTH):
                self.board[x][0].setObstacle()
                self.board[x][BOARD_HEIGHT-1].setObstacle()

        def _drawInnerHorizontalWalls(self):
            bottomWall = BOARD_HEIGHT - BOTTOM_TUNNEL_HEIGHT - 1
            topWall = TOP_TUNNEL_HEIGHT - 1
            for x in range(PATH_WIDTH, BOARD_WIDTH - PATH_WIDTH):
                for i in range(SPEED+1):
                    self.board[x][bottomWall-i].setObstacle()
                    self.board[x][topWall+i].setObstacle()

        def _drawOuterVerticalWalls(self):
            for y in range(BOARD_HEIGHT):
                self.board[0][y].setObstacle()
                self.board[BOARD_WIDTH-1][y].setObstacle()

        def _drawInnerVerticalWalls(self):
            for y in range(TOP_TUNNEL_HEIGHT, PATH_HEIGHT + TOP_TUNNEL_HEIGHT):
                for i in range(SPEED+1):
                    self.board[PATH_WIDTH+i][y].setObstacle()
                    self.board[BOARD_WIDTH - PATH_WIDTH - i][y].setObstacle()

        _drawOuterHorizontalWalls(self)
        _drawOuterVerticalWalls(self)
        _drawInnerHorizontalWalls(self)
        _drawInnerVerticalWalls(self)

    def createExit(self):
        print("EXIT: 0 ",BOARD_HEIGHT - EXIT_HEIGHT, -1)
        for x in range(EXIT_WIDTH):
            for y in range(BOARD_HEIGHT-1, BOARD_HEIGHT - EXIT_HEIGHT, -1):
                self.board[x][y].setExit()
    
    def createBus(self):
        print("BUS: ", BUS_TOP_LEFT_X, BUS_TOP_LEFT_Y)
        for x in range(BUS_TOP_LEFT_X, BUS_TOP_LEFT_X + BUS_LENGTH):
            for y in range(BUS_TOP_LEFT_Y, BUS_TOP_LEFT_Y + BUS_WIDTH):
                self.board[x][y].setObstacle()

    def calculateFireAndSmoke(self):
        for x in range(1, BOARD_WIDTH - 1):
            for y in range(1, BOARD_HEIGHT - 1):
                fire_value = self.board[x][y].getFireValue()
                smoke_value = self.board[x][y].getSmokeValue()
                # Symulacja rozprzestrzeniania się ognia
                if fire_value > 0:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if not (i == 0 and j == 0):
                                neighbor_x = x + i
                                neighbor_y = y + j
                                if 0 <= neighbor_x < BOARD_WIDTH and 0 <= neighbor_y < BOARD_HEIGHT:
                                    # Prawdopodobieństwo, że ogień się rozprzestrzeni
                                    spread_probability = 0.8
                                    if random.random() < spread_probability:
                                        self.board[neighbor_x][neighbor_y].setFireValue(fire_value * 0.8)
                # Symulacja rozprzestrzeniania się dymu
                if smoke_value > 0:
                    # Rozprzestrzenianie się dymu w górę
                    self.board[x][y - 1].setSmokeValue(smoke_value * 0.7)
                    for i in range(-1, 2):
                        neighbor_x = x + i
                        neighbor_y = y
                        if 0 <= neighbor_x < BOARD_WIDTH and 0 <= neighbor_y < BOARD_HEIGHT:
                            self.board[neighbor_x][neighbor_y].setSmokeValue(smoke_value * 0.5)
                # Źródło ognia i dymu
                if fire_value == 0 and smoke_value == 0:
                    source_probability = 0.01
                    if random.random() < source_probability:
                        intensity = random.randint(50, 100)  # Losowa intensywność ognia
                        density = random.randint(20, 50)  # Losowa gęstość dymu
                        self.board[x][y].setFireValue(intensity)
                        self.board[x][y].setSmokeValue(density)

    def initializeFire(self, fire_sources):
        for source in fire_sources:
            x, y, size, intensity = source
            # intensity = random.randint(50, 100)  # Random intensity for each fire source
            for i in range(-size // 2, size // 2 + 1):
                for j in range(-size // 2, size // 2 + 1):
                    neighbor_x = x + i
                    neighbor_y = y + j
                    if 0 <= neighbor_x < BOARD_WIDTH and 0 <= neighbor_y < BOARD_HEIGHT:
                        self.board[neighbor_x][neighbor_y].setFireValue(intensity)

    def initializeSmoke(self):
        for x in range(1, BOARD_WIDTH - 1):
            for y in range(1, BOARD_HEIGHT - 1):
                density = random.randint(20, 50)  # Losowa gęstość dymu
                self.board[x][y].setSmokeValue(density)

    def calcualteStaticLayer(self):
        calculatedValue = 0
        self.tmpMaxStaticVal = math.sqrt(pow(BOARD_WIDTH-1, 2) + pow(EXIT_Y-1, 2))
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                calculatedValue = math.sqrt(pow(EXIT_X - x, 2) + pow(EXIT_Y - y, 2))  / self.tmpMaxStaticVal
                self.board[x][y].setLayerVal(LayerType.STATIC, calculatedValue)

    def inicializeDynamicLayer(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.board[x][y].setLayerVal(LayerType.DYNAMIC, 0)

    def calculateMove(self, positionXY, speed, fire_sources): # z omijaniem ognia
    # def calculateMove(self, positionXY, speed): # bez omijania ognia
        x, y = positionXY
        newDynamic = 0
        bestMove = float('-inf')
        bestPosition = positionXY
        moves = [(x,y)]
        for distance in range(1, speed+1):
            moves.append((x, y + distance))
            moves.append((x, y - distance))
            moves.append((x+distance, y))
            moves.append((x-distance, y))

        # print("MOVES: ",  moves)
        
        for move_x, move_y in moves:
            if 0 <= move_x < BOARD_WIDTH and 0 <= move_y < BOARD_HEIGHT:
                static_value = 1 -  self.board[move_x][move_y].getStaticValue()
                dynamic_value = self.board[move_x][move_y].getDynamicValue()
                obstacle_value = int(self.board[move_x][move_y].isObstacle())
                taken_value = int(self.board[move_x][move_y].isTakenByMan())
                
                ### FIRE CALCULATION START ###
                # Calculate distance to the nearest fire source
                min_distance_to_fire = min(
                    math.sqrt(pow(fx - move_x, 2) + pow(fy - move_y, 2))
                    for fx, fy, size, intensity in fire_sources
                )

                distance_threshold = 10

                if min_distance_to_fire >= distance_threshold:
                    min_distance_to_fire = distance_threshold
                elif min_distance_to_fire <= 0:
                    min_distance_to_fire = 0.000000000001
                else:
                    pass


                # Modify moveProbability based on the distance to the fire
                moveProbability = random.uniform(0.98, 1) * math.exp(ALFA * dynamic_value) * math.exp(BETA * static_value) * (1 - obstacle_value) * (1 - taken_value) * np.abs(min_distance_to_fire / distance_threshold)
                ### FIRE CALCULATION END ###

                # TODO:
                # current_value
                # wzor = N * current_value * math.exp(alfa*dynamic_value) * math.exp(beta*static_value) * (1-isObstacle()) * (1-isOtherMan())
                # fire_value = self.board[move_x][move_y].getFireValue()  # Nowa linia do pobrania wartości ognia
                # moveProbability = random.uniform(0.98, 1) * math.exp(ALFA * dynamic_value) * math.exp(BETA * static_value) * (1 - obstacle_value) * (1 - taken_value)
                # print("Probability: ", moveProbability, bestMove, move_x, move_y, dynamic_value, static_value)
                if moveProbability > bestMove and moveProbability > 0:
                    # print("NEW ", math.exp(ALFA*dynamic_value), math.exp(BETA*static_value))
                    bestMove = moveProbability
                    newDynamic = dynamic_value
                    bestPosition = (move_x, move_y)
        best_x, best_y = bestPosition
        # print("Best move: ", bestMove, best_x-x, best_y-y)    
        # print(bestMove)
        # if(newDynamic > 0):
        #     print(static_value, newDynamic)
        self.board[best_x][best_y].setLayerVal(LayerType.DYNAMIC, newDynamic+DYNAMIC_INCREMENT)
        self.board[x][y].setLayerVal(LayerType.DYNAMIC, newDynamic-DYNAMIC_INCREMENT)

        self.board[best_x][best_y].setTakenByMan(True)
        self.board[x][y].setTakenByMan(False)
        return bestPosition
    
    def removeMan(self, position : [int, int]):
        x, y = position
        self.board[x][y].setTakenByMan(False)