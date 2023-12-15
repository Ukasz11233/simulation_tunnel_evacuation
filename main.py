from classes.Simulation import *


if __name__ == '__main__':
    simulation = Simulation()
    
    simulation.board.initializeFire(SOURCES)
    simulation.board.initializeSmoke(EXPERIMENT)
    simulation.run(SOURCES)