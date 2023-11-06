from classes.Cell import *
from settings import *

class Layer:
    def __init__(self, _screen, _layerType) -> None:
        self.screen = _screen
        self.layerType = _layerType
        if(self.layerType == LayerType.POSITION.value):
            self.board = [[ManCell(self.screen, i, j) for i in range(BOARD_HEIGHT)]
                      for j in range(BOARD_WIDTH)]
        else:
            self.board = [[CellAdapter(self.screen) for _ in range(BOARD_HEIGHT)]
                      for _ in range(BOARD_WIDTH)]
        pass

    def drawLayer(self, x, y):
        if(not self.board[x][y].isSet()):
            return
        
        def _drawCellColored(color):
            pygame.draw.rect(
                self.screen, color, (x * CELL_SIZE, y, CELL_SIZE, CELL_SIZE))

        def _checkIfCellIsOnPath(x, y):
            return (y > TOP_TUNNEL_HEIGHT + PATH_HEIGHT or y < TOP_TUNNEL_HEIGHT or x < PATH_WIDTH or x > BOARD_WIDTH - PATH_WIDTH)

        if(self.layerType == LayerType.OBSTACLE.value):
            if(self.board[x][y].getValue() == ObstacleType.WALL):
                _drawCellColored(RED)
            elif(self.board[x][y].getValue() == ObstacleType.EXIT):
                _drawCellColored(GREEN)
        if(self.layerType == LayerType.STATIC.value):
            if(_checkIfCellIsOnPath(x, y)):
                scaledBlue = abs(
                    255 - (self.board[x][y].getValue() * 255) // 774)
                _drawCellColored((0, 0, scaledBlue))
        if(self.layerType == LayerType.POSITION.value):
            _drawCellColored(GREEN)


    def setCellValue(self, x, y, value):
        self.board[x][y].setValue(value)

    def getCellValue(self, x, y):
        return self.board[x][y].getValue()

    def move(self, x, y, positionXY):
        self.board[x][y].move(positionXY)
