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
        # self.people = [Man(BOARD_WIDTH - 2, 120, self.screen), Man(BOARD_WIDTH - 2, 80, self.screen), Man(BOARD_WIDTH-3, 30, self.screen)]
        self.peopleInTunnel = []
        self.peopleInBus = self.bus_position()
        self.font = pygame.font.Font(None, 25)

    def run(self):
        validator = Validation()
        start_time = time.time()
        while validator.final() and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            updated_people = []
            if len(self.peopleInBus) > BUS_EXIT_BUFFOR:
                peopleWhoLeft = self.peopleInBus[:5]
                self.peopleInBus = self.peopleInBus[5:]
                self.peopleInTunnel += peopleWhoLeft
            self.board.updateBoardLayers()
            for man in self.peopleInTunnel:
                man.move(self.board.calculateMove(man.getXYPosition(), man.getSpeed()))
                if not validator.update(man.getXYPosition()):
                    updated_people.append(man)
                # print(validator.getNumOfEscaped())                    
                man.draw()
            
            self.peopleInTunnel = updated_people
            self.displayStatistics(validator.getNumOfEscaped(), start_time)    
            
            pygame.display.flip()
        
        end_time = time.time()
        print(SPEED * (end_time - start_time))
    
    def input(self, events):
        for event in events:
            if(input(event.key.get_pressed(pygame.K_ESCAPE)) == True) or (event.type == pygame.QUIT):
                self.running = False
            
    def bus_position(self):
        # TODO: changing speed and adjusting it to the inner walls -- !!! DONE !!!
        table = []
        random_values_x = random.sample(range(-EVACUATORS, EVACUATORS+1), EVACUATORS)#[random.randint(-10, 10) for _ in range(EVACUATORS)]
        random_values_y = [random.randint(-5, 5) for _ in range(EVACUATORS)]
        # random_speed = [random.randint(1,2) for _ in range(EVACUATORS)]
        # print(random_values_x, random_values_y)
        for i in range(EVACUATORS // BUS_EXIT_BUFFOR):
            for j in range(BUS_EXIT_BUFFOR):
                table.append(Man(BUS_TOP_LEFT_X+j, BUS_TOP_LEFT_Y,self.screen, SPEED))
        return table
    
    def displayStatistics(self, numberOfEscaped, start_time):
        label = self.font.render(f"Number of evacuated people: {numberOfEscaped}", True, (255,255,0))
        label_time = self.font.render(f"Time of evacuation: {round(time.time() - start_time, 2) * SCALE}s", True, (255,255,0))
        self.screen.fill(BLACK, (0, BOARD_HEIGHT+5, 400, HEIGHT - BOARD_HEIGHT - 10))
        self.screen.blit(label, (10, 200))
        self.screen.blit(label_time, (10, 250))