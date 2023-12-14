from classes.Simulation import *


if __name__ == '__main__':
    simulation = Simulation()

    fire_sources = [(10, 10, 3, 50), (30, 20, 4, 100), (50, 40, 3, 75)]  # Example fire sources (x, y, size, intensity)
    simulation.board.initializeFire(fire_sources)

    simulation.board.initializeSmoke()
    simulation.run(fire_sources)
    # simulation.run()