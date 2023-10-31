import pygame
from settings import *
from classes.Cell import *


class Board:

    def __init__(self, _screen) -> None:
        self.cellSize = WIDTH // BOARD_WIDTH

        self.boardWidth = BOARD_WIDTH
        self.boardHeight = BOARD_HEIGHT
        self.screen = _screen
        self.board = [[Cell(self.screen) for _ in range(self.boardHeight)]
                      for _ in range(self.boardWidth)]
        self.createWalls()
        self.createExit()
        self.calcualteStaticLayer()
        self.tmpMaxStaticVal = self.getMaxStaticValue()
        pass

    def drawBoard(self):
        for x in range(self.boardWidth):
            for y in range(self.boardHeight):
                self.drawCell(x, y)

    def drawCell(self, x, y):
        def _drawCellColored(color):
            pygame.draw.rect(
                self.screen, color, (x * self.cellSize, y, self.cellSize, self.cellSize))

        if (self.board[x][y].isObstacle()):
            _drawCellColored(RED)
        elif (self.board[x][y].isExit()):
            _drawCellColored(GREEN)
        else:
            scaledBlue = abs(255 -(self.board[x][y].getStaticValue() * 255)// self.tmpMaxStaticVal)
            _drawCellColored((0, 0, scaledBlue))

    def createWalls(self):
        self.drawHorizontalWalls()
        self.drawVerticalWalls()

    def drawHorizontalWalls(self):
        for x in range(BOARD_WIDTH):
            self.board[x][0].setObstacle()
            self.board[x][BOARD_HEIGHT-1].setObstacle()

        self.drawInnerHorizontalWalls()

    def drawInnerHorizontalWalls(self):
        bottomWall = BOARD_HEIGHT - BOTTOM_TUNNEL_HEIGHT - 1
        topWall = TOP_TUNNEL_HEIGHT - 1
        for x in range(PATH_WIDTH, BOARD_WIDTH - PATH_WIDTH):
            self.board[x][bottomWall].setObstacle()
            self.board[x][topWall].setObstacle()

    def drawVerticalWalls(self):
        for y in range(BOARD_HEIGHT):
            self.board[0][y].setObstacle()
            self.board[BOARD_WIDTH-1][y].setObstacle()

        self.drawInnerVerticalWalls()

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
                calculatedValue = abs(EXIT_X - x) + abs(EXIT_Y - y)
                self.board[x][y].setLayerVal(LayerType.STATIC, calculatedValue)

    def getMaxStaticValue(self):
        result = 0
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                result = max(result, self.board[x][y].getStaticValue())
        return result