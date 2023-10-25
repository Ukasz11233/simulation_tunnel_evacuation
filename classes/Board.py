import pygame
from settings import *
from classes.Cell import *

class Board:

    def __init__(self, _screen) -> None:
        self.cellSize = WIDTH // BOARD_WIDTH

        self.boardWidth = BOARD_WIDTH
        self.boardHeight = BOARD_HEIGHT
        self.screen = _screen
        self.board = [[Cell(self.screen) for _ in range(self.boardHeight)] for _ in range(self.boardWidth)]
        self.createWalls()
        print("created")
        pass

    def drawBoard(self):
        for x in range(self.boardWidth):
            for y in range(self.boardHeight):
                self.drawCell(x, y)

    def drawCell(self, x, y):
        def _drawCellColored(color):
            pygame.draw.rect(self.screen, color, (x * self.cellSize, y, self.cellSize, self.cellSize))

        if(self.board[x][y].isObstacle()):
            _drawCellColored(RED)


    def createWalls(self):
        self.drawTopWall()
        self.drawBottomWall()
        self.drawInnerWalls()

        
    def drawTopWall(self):
        y = 10
        for x in range(250):
            self.board[x][y].setObstacle()
            if(x % 25 == 0):
                y -= 1

            if(y < 0):
                print(y)
        for x in range(250, self.boardWidth):
            self.board[x][0].setObstacle()

    def drawBottomWall(self):
        y_bottom_left = self.boardHeight-7
        x_start = 0
        x_end = 42
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle()
            if( x % 7 == 0):
                y_bottom_left += 1
        
        x_start = x_end
        x_end = 42 + 288
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle()
            if(x % 28 == 0):
                y_bottom_left -= 1
            
        x_start = x_end
        x_end = 42 + 288 + 471
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle()

        x_start = x_end
        x_end = 42 + 288 + 471 + 46
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle()
            if(x % 5 == 0):
                y_bottom_left -= 1

    def drawInnerWalls(self):
        y_top = self.boardHeight - 66
        y_bottom = self.boardHeight - 16
        x_start = 0
        x_end = 141
        for x in range(x_end):
            self.board[x][y_top].setObstacle()
            self.board[x][y_bottom].setObstacle()
            if(x < 42 and x % 7 == 0):
                y_bottom += 1
            if(x >= 42 and x % 28 == 0):
                y_bottom -= 1
            if(x % 28 == 0):
                y_top -= 1

        x_start = x_end + 3
        x_end = x_start + 188

        for x in range(x_start, x_end):
            self.board[x][y_top].setObstacle()
            self.board[x][y_bottom].setObstacle()
            if( x % 28 == 0):
                y_top -= 1
                y_bottom -= 1

        for i in range(2):
            x_start = x_end + 3
            x_end = x_start + 188

            for x in range(x_start, x_end):
                self.board[x][y_top].setObstacle()
                self.board[x][y_bottom].setObstacle()
