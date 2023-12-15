from classes.Simulation import *


if __name__ == '__main__':
    simulation = Simulation()

    fire_sources = []
    # fire_sources = [(120, 10, 3, 50), (125, 25, 4, 100), (130, 40, 3, 75), (220, 40, 3, 75), (250, 25, 3, 75)]  # źródła dymu (x, y, size, intensity)
    simulation.board.initializeFire(fire_sources)

    experiment_no = EXPERIMENT # (0-4) patrz numer eksperymentu z rys.5 pkt2.2 dokumentacji - modyfikacja gestosci dymu w zależności od eksperymentu
    simulation.board.initializeSmoke(experiment_no)
    simulation.run(fire_sources)