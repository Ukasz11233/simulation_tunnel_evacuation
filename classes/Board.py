import math
import pygame
from settings import *
from classes.Cell import *


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
            pygame.draw.rect(
                self.screen, color, (x * CELL_SIZE, y, CELL_SIZE, CELL_SIZE))

        def _checkIfCellIsOnPath(x, y):
            return (y > TOP_TUNNEL_HEIGHT + PATH_HEIGHT or y < TOP_TUNNEL_HEIGHT or x < PATH_WIDTH or x > BOARD_WIDTH - PATH_WIDTH)

        if (self.board[x][y].isObstacle()):
            _drawCellColored(RED)
        elif (self.board[x][y].isExit()):
            _drawCellColored(GREEN)
        elif (_checkIfCellIsOnPath(x, y)):
            scaledBlue = abs(
                255 - (self.board[x][y].getStaticValue() * 255) // self.tmpMaxStaticVal)
            _drawCellColored((0, 0, scaledBlue))

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
            self.board[x][bottomWall].setObstacle()
            self.board[x][topWall].setObstacle()

    def drawOuterVerticalWalls(self):
        for y in range(BOARD_HEIGHT):
            self.board[0][y].setObstacle()
            self.board[BOARD_WIDTH-1][y].setObstacle()

    def drawInnerVerticalWalls(self):
        for y in range(TOP_TUNNEL_HEIGHT, PATH_HEIGHT + TOP_TUNNEL_HEIGHT):
            self.board[PATH_WIDTH][y].setObstacle()
            self.board[BOARD_WIDTH - PATH_WIDTH][y].setObstacle()

    def createExit(self):
        for x in range(EXIT_WIDTH):
            for y in range(BOARD_HEIGHT-1, BOARD_HEIGHT - BOTTOM_TUNNEL_HEIGHT, -1):
                self.board[x][y].setExit()

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
        print(result)
        return result
    
    def inicializeDynamicLayer(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.board[x][y].setLayerVal(LayerType.DYNAMIC, 1)  #zeby nie zerowac prawdopodobienstw

    def calculateMove(self, positionXY, speed):
        x, y = positionXY
        new_dynamic = 0
        bestMove = float('inf')
        bestPosition = positionXY
        moves = [(x-speed, y), (x+speed, y), (x, y-speed), (x, y+speed)]

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
                if not self.board[move_x][move_y].isObstacle() and bestMove > static_value:
                    bestMove = static_value
                    bestPosition = (move_x, move_y)
                    new_dynamic = dynamic_value

        # UPGRADE dynamic_value
        best_x, best_y = bestPosition
        self.board[best_x][best_y].setLayerVal(LayerType.DYNAMIC, new_dynamic+1)
        # if self.board[best_x][best_y].getDynamicValue()>2:
        print(bestPosition, self.board[best_x][best_y].getDynamicValue())

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
