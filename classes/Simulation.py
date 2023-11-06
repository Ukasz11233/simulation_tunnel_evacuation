import pygame, sys
from settings import *
from classes.Board import *
from classes.Man import *


class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simulation")
        self.running = True
        self.board = Board(self.screen)
        self.people = [Man(BOARD_WIDTH - 2, 120, self.screen), Man(BOARD_WIDTH - 2, 80, self.screen), Man(BOARD_WIDTH-3, 30, self.screen)]


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.board.updateBoardLayers()
            for man in self.people:
                man.move(self.board.calculateMove(man.getXYPosition(), man.getSpeed()))
                man.draw()
            pygame.display.flip()
    
    def input(self, events):
        for event in events:
            if(input(event.key.get_pressed(pygame.K_ESCAPE)) == True) or (event.type == pygame.QUIT):
                self.running = False
            