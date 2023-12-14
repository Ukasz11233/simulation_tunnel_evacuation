from classes.Simulation import *


if __name__ == '__main__':
    simulation = Simulation()

    # Specify fire sources as a list of tuples (x, y, size)
    fire_sources = [(10, 10, 3, 50), (30, 20, 4, 100), (50, 30, 3, 75)]  # Example fire sources
    simulation.board.initializeFire(fire_sources)

    simulation.board.initializeSmoke()
    simulation.run(fire_sources)
    # simulation.run()