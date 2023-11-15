import pygame, sys
from settings import *
from classes.Board import *
from classes.Man import *
import random


class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simulation")
        self.running = True
        self.board = Board(self.screen)
        # self.people = [Man(BOARD_WIDTH - 2, 120, self.screen), Man(BOARD_WIDTH - 2, 80, self.screen), Man(BOARD_WIDTH-3, 30, self.screen)]
        self.people = self.bus_position()


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
            
    def bus_position(self):
        # TODO: changing speed and adjusting it to the inner walls
        table = []
        random_values_x = random.sample(range(-10, 11), EVACUATORS)#[random.randint(-10, 10) for _ in range(EVACUATORS)]
        random_values_y = [random.randint(-5, 5) for _ in range(EVACUATORS)]
        # random_speed = [random.randint(1,2) for _ in range(EVACUATORS)]
        print(random_values_x, random_values_y)
        for i in range(EVACUATORS):
            table.append(Man(BUS_X+random_values_x[i], BUS_Y+random_values_y[i], self.screen, SPEED))
        return table