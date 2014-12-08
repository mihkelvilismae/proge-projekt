__author__ = 'mihkel'
#---------------------------------------------------------------------------------------------------
#       Config
#---------------------------------------------------------------------------------------------------
class MainConfig():
    def __init__(self, **kwargs):
        self.columnChars = list(' ABCDEFGHIJ')
        self.rowNumbers = list(range(0,11))
    # application window size:
        self.windowWidth = 1400
        self.windowHeight = 700
        self.windowSize = (self.windowWidth, self.windowHeight)

class GridConfig():

    gridElementSize = tuple
    battlefieldRectangleSize = tuple

    def __init__(self, sizeMultiplier=1, **kwargs):
        if sizeMultiplier==1:
            self.gridHeight = 600
            self.gridWidth = 600
        else:
            self.gridHeight = 350
            self.gridWidth = 350

        self.gridElementSize = (self.gridWidth/11, self.gridHeight/11)
        self.battlefieldRectangleSize = (self.gridWidth/11-5, self.gridHeight/11-5)
        self.shipBlockHeight = self.gridElementSize[0]
        self.shipBlockWidth = self.gridElementSize[1]
        self.shipBlockSize = (self.gridElementSize[0], self.gridElementSize[1])
