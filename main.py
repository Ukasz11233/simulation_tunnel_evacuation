from classes.Simulation import *


if __name__ == '__main__':
    simulation = Simulation()
    
    simulation.board.initializeFire()
    simulation.board.initializeSmoke()

    # fire_sources = [
    #     (20, 30, 50, 50),
    #     (30, 50, 80, 100),
    #     (40, 70, 80, 80),
    # ]
    # simulation.board.initializeFireAndSmoke(fire_sources)

    simulation.board.calculateFireAndSmoke()
    
    simulation.run()