import pygame
from settings import *
from classes.Board import *


class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((HEIGHT, WIDTH))
        pygame.display.set_caption("Simulation")
        self.running = True
        self.board = Board(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.board.drawBoard()
            pygame.display.flip()

