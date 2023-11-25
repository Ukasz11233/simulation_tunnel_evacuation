import math
import pygame
from settings import *
from classes.Cell import *
import random


class Board:
    def __init__(self, _screen) -> None:
        self.boardWidth = BOARD_WIDTH
        self.boardHeight = BOARD_HEIGHT
        self.screen = _screen
        self.board = [[Cell(self.screen) for _ in range(self.boardHeight)]
                      for _ in range(self.boardWidth)]
        self.createWalls()
        self.createExit()
        self.calcualteStaticLayer()
        self.inicializeDynamicLayer()
        self.tmpMaxStaticVal = self.getMaxStaticValue()
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
            scaledBlue = abs(
                255 - (self.board[x][y].getStaticValue() * 255) // self.tmpMaxStaticVal)

            scaledRed = (self.board[x][y].getFireValue() * 255) // 100
            scaledGray = (self.board[x][y].getSmokeValue() * 255) // 100

            _drawCellColored((scaledRed, 0, scaledBlue - scaledGray))

    def createWalls(self):
        self.drawOuterHorizontalWalls()
        self.drawOuterVerticalWalls()
        self.drawInnerHorizontalWalls()
        self.drawInnerVerticalWalls()

    def drawOuterHorizontalWalls(self):
        for x in range(BOARD_WIDTH):
            self.board[x][0].setObstacle()
            self.board[x][BOARD_HEIGHT-1].setObstacle()

    def drawInnerHorizontalWalls(self):
        bottomWall = BOARD_HEIGHT - BOTTOM_TUNNEL_HEIGHT - 1
        topWall = TOP_TUNNEL_HEIGHT - 1
        for x in range(PATH_WIDTH, BOARD_WIDTH - PATH_WIDTH):
            for i in range(SPEED):
                self.board[x][bottomWall-i].setObstacle()
                self.board[x][topWall+i].setObstacle()

    def drawOuterVerticalWalls(self):
        for y in range(BOARD_HEIGHT):
            self.board[0][y].setObstacle()
            self.board[BOARD_WIDTH-1][y].setObstacle()

    def drawInnerVerticalWalls(self):
        for y in range(TOP_TUNNEL_HEIGHT, PATH_HEIGHT + TOP_TUNNEL_HEIGHT):
            for i in range(SPEED):
                self.board[PATH_WIDTH+i][y].setObstacle()
                self.board[BOARD_WIDTH - PATH_WIDTH - i][y].setObstacle()

    def createExit(self):
        for x in range(EXIT_WIDTH):
            for y in range(BOARD_HEIGHT-1, BOARD_HEIGHT - EXIT_HEIGHT, -1):
                self.board[x][y].setExit()

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

                    # Rozprzestrzenianie się dymu na boki
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

    def initializeFire(self):
        for _ in range(random.randint(5, 10)):
            x, y = random.randint(1, BOARD_WIDTH - 2), random.randint(1, BOARD_HEIGHT - 2)
            intensity = random.randint(50, 100)  # Losowa intensywność ognia
            for i in range(-1, 2):
                for j in range(-1, 2):
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
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                calculatedValue = math.sqrt(pow(EXIT_X - x, 2) + pow(EXIT_Y - y, 2))
                self.board[x][y].setLayerVal(LayerType.STATIC, calculatedValue)

    def getMaxStaticValue(self):
        result = 0
        # print(self.board)
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                result = max(result, self.board[x][y].getStaticValue())
        # print(result)
        return result
    
    def inicializeDynamicLayer(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.board[x][y].setLayerVal(LayerType.DYNAMIC, 0)

    def calculateMove(self, positionXY, speed):
        x, y = positionXY
        new_dynamic = 0
        bestMove = float('inf')
        bestPosition = positionXY
        moves = []
        for distance in range(0, speed):
            moves.append((x-distance, y))
            moves.append((x+distance, y))
            moves.append((x, y - distance))
            moves.append((x, y + distance))

        for move_x, move_y in moves:
            if 0 <= move_x < BOARD_WIDTH and 0 <= move_y < BOARD_HEIGHT:
                static_value = self.board[move_x][move_y].getStaticValue()
                dynamic_value = self.board[move_x][move_y].getDynamicValue()
                # TODO:
                # current_value
                # dynamic_value
                # define N, alfa, beta
                # isObstacle(), isOtherMan()
                # wzor = N * current_value * math.exp(alfa*dynamic_value) * math.exp(beta*static_value) * (1-isObstacle()) * (1-isOtherMan())
                fire_value = self.board[move_x][move_y].getFireValue()  # Nowa linia do pobrania wartości ognia
                if not self.board[move_x][move_y].isObstacle() and bestMove > static_value + fire_value:  # Zmodyfikowany warunek z uwzględnieniem ognia
                    bestMove = static_value + fire_value
                    new_dynamic = dynamic_value
                    bestPosition = (move_x, move_y)
    
        # UPGRADE dynamic_value
        best_x, best_y = bestPosition
        self.board[best_x][best_y].setLayerVal(LayerType.DYNAMIC, new_dynamic+1)
        # if self.board[best_x][best_y].getDynamicValue()>2:
        # print(bestPosition, self.board[best_x][best_y].getDynamicValue())


        return bestPosition
    
    # TODO: 
    # p[i,j] = N * M[i,j] * exp(alfa*D[i,j]) * exp(beta*S[i,j]) * (1-n[i,j]) * d[i,j]
    # p[i,j] - prawdopodobieństwo przejścia do komórki o współrzędnych (i, j)
    # N - współczynnik normalizacji ???
    # M[i,j] - wartość podstawowa (current_value)
    # D[i,j] - wartość warstwy dynamicznej (dynamic_value)
    # S[i,j] - wartość warstwy statycznej
    # n[i,j] - wartość określająca czy komórka nie jest zajęta przez przeszkodę
    # d[i,j] - wartość określająca czy komórka nie jest zajęta przez inną osobę

