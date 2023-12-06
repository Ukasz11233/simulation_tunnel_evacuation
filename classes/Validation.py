from settings import *

class Validation:
    def __init__(self) -> None:
        self.x = EXIT_X + EXIT_WIDTH
        self.y = EXIT_Y - EXIT_HEIGHT
        self.numOfEscaped = 0
    
    def update(self, positionXY):
        if positionXY[0] < self.x  and positionXY[1] > self.y:
            self.numOfEscaped += 1
            return True
        return False
    
    def final(self):
        return not self.numOfEscaped >= 80
    

    def getNumOfEscaped(self):
        return self.numOfEscaped