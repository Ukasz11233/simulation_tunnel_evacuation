import pygame
from settings import *
from classes.Cell import *

class Board:

    def __init__(self, _screen) -> None:
        self.boardWidth = BOARD_WIDTH
        self.boardHeight = BOARD_HEIGHT
        self.screen = _screen
        self.board = [[Cell(self.screen) for _ in range(self.boardHeight)] for _ in range(self.boardWidth)]
        self.createWalls()
        pass

    def drawBoard(self):
        for x in range(self.boardWidth):
            for y in range(self.boardHeight):
                self.board[x][y].draw()


    def createWalls(self):
        for x in range(self.boardWidth):
            self.board[x][0].setObstacle(x, 0)
            self.board[x][self.boardHeight - 1].setObstacle(x, self.boardHeight - 1)
        for y in range(self.boardHeight):
            self.board[0][y].setObstacle(0, y)
            self.board[self.boardWidth - 1][y].setObstacle(self.boardWidth - 1, y)

