from classes.Simulation import *

if __name__ == '__main__':
    simulation = Simulation()
    simulation.board.initializeFire()
    simulation.board.initializeSmoke()
    simulation.run()