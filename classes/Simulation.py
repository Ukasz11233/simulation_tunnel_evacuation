import pygame, sys
from settings import *
from classes.Board import *
from classes.Man import *
from  classes.Validation import *
import random
import time


class Simulation:
    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simulation")
        self.running = True
        self.board = Board(self.screen)
        self.peopleInTunnel = []
        self.peopleInBus = self.bus_position()
        self.font = pygame.font.Font(None, 25)

    def run(self, fire_sources):
        validator = Validation()
        start_time = time.time()
        self.board.initializeFire(fire_sources)
        while validator.final() and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            updated_people = []
            if len(self.peopleInBus) > 0:
                peopleWhoLeft = self.peopleInBus[:5]
                self.peopleInBus = self.peopleInBus[5:]
                self.peopleInTunnel += peopleWhoLeft
            self.board.updateBoardLayers()
            index = 0
            for man in self.peopleInTunnel:
                man.move(self.board.calculateMove(man.getXYPosition(), man.getSpeed(), fire_sources))
                if not validator.update(man.getXYPosition()):
                    updated_people.append(man)
                else:
                    self.board.removeMan(man.getXYPosition())
                man.draw()
                index += 1
            self.peopleInTunnel = updated_people
            self.displayStatistics(validator.getNumOfEscaped(), start_time)
            pygame.display.flip()
        end_time = time.time()
        print(SPEED/3 * (end_time - start_time))
        print("CZAS RZECZYWISTY: ", end_time - start_time)
    
    def input(self, events):
        for event in events:
            if(input(event.key.get_pressed(pygame.K_ESCAPE)) == True) or (event.type == pygame.QUIT):
                self.running = False
            
    def bus_position(self):
        table = []
        for i in range(EVACUATORS // BUS_EXIT_BUFFOR):
            for j in range(BUS_EXIT_BUFFOR):
                doors = BUS_WIDTH // 2
                if j % 2 == 1:
                    doors *= 3
                table.append(Man(BUS_TOP_LEFT_X + doors + j, BUS_TOP_LEFT_Y,self.screen, SPEED))
        return table
    
    def displayStatistics(self, numberOfEscaped, start_time):
        label = self.font.render(f"Number of evacuated people: {numberOfEscaped}", True, YELLOW)
        label_system_time = self.font.render(f"Time of evacuation: {round(round(time.time() - start_time, 2) * (SPEED/3),2)}s", True, YELLOW)
        label_user_time = self.font.render(f"Real time: {round(time.time() - start_time, 2)}s", True, YELLOW)
        label_speed = self.font.render(f"Speed to scale: x{SPEED/SCALE}", True, YELLOW)
        self.screen.fill(BLACK, (0, BOARD_HEIGHT+5, 400, HEIGHT - BOARD_HEIGHT - 10))
        self.screen.blit(label, (10, 200))
        self.screen.blit(label_system_time, (10, 250))
        self.screen.blit(label_user_time, (10, 300))
        self.screen.blit(label_speed, (10, 350))