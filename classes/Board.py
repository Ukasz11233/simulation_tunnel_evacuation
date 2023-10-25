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
        print("created")
        pass

    def drawBoard(self):
        for x in range(self.boardWidth):
            for y in range(self.boardHeight):
                self.board[x][y].draw()


    def createWalls(self):
        self.drawTopWall()
        self.drawBottomWall()
        self.drawInnerWalls()


        #     self.board[x][self.boardHeight - 1].setObstacle(x, self.boardHeight - 1)

        # for y in range(self.boardHeight):
        #     self.board[0][y].setObstacle(0, y)
            
        #     self.board[self.boardWidth - 1][y].setObstacle(self.boardWidth - 1, y)

    def drawTopWall(self):
        y = 10
        for x in range(500):
            self.board[x][y].setObstacle(x ,y)
            if(x % 50 == 0):
                y -= 1

            if(y < 0):
                print(y)
        for x in range(500, self.boardWidth):
            self.board[x][0].setObstacle(x, 0)

    def drawBottomWall(self):
        y_bottom_left = self.boardHeight-7
        x_start = 0
        x_end = 84
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle(x, y_bottom_left)
            if( x % 14 == 0):
                y_bottom_left += 1
        x_start = x_end
        x_end = 84 + 576
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle(x, y_bottom_left)
            if(x % 57 == 0):
                y_bottom_left -= 1
            
        x_start = x_end
        x_end = 84 + 576 + 942
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle(x, y_bottom_left)

        x_start = x_end
        x_end = 84 + 576 + 942 + 93
        for x in range(x_start, x_end):
            self.board[x][y_bottom_left].setObstacle(x, y_bottom_left)
            if(x % 9 == 0):
                y_bottom_left -= 1

    def drawInnerWalls(self):
        y_top = self.boardHeight - 66
        y_bottom = self.boardHeight - 16
        x_start = 0
        x_end = 283
        for x in range(x_end):
            self.board[x][y_top].setObstacle(x, y_top)
            self.board[x][y_bottom].setObstacle(x, y_bottom)
            if(x < 84 and x % 14 == 0):
                y_bottom += 1
            if(x >= 84 and x % 57 == 0):
                y_bottom -= 1
            if(x % 57 == 0):
                y_top -= 1

        x_start = x_end + 6
        x_end = x_start + 375

        for x in range(x_start, x_end):
            self.board[x][y_top].setObstacle(x, y_top)
            self.board[x][y_bottom].setObstacle(x, y_bottom)
            if( x % 57 == 0):
                y_top -= 1
                y_bottom -= 1

        for i in range(2):
            x_start = x_end + 6
            x_end = x_start + 375

            for x in range(x_start, x_end):
                self.board[x][y_top].setObstacle(x, y_top)
                self.board[x][y_bottom].setObstacle(x, y_bottom)
