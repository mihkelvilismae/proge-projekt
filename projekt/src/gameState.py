__author__ = 'mihkel'
import collections
# This class handles most checks, such as possibility to rotate or place ships
class GameState():
    STATE_EMPTY = 'empty'

    gameStateMatrix = collections.OrderedDict()

    def __init__(self, grid):
        self.grid = grid

    def createGameStateMatrix(self):
        for rowNr, rowElements in self.grid.gridElements.items():
            self.gameStateMatrix[ rowNr ] = collections.OrderedDict()
            for colChar, element in rowElements.items():
                self.gameStateMatrix[ rowNr ][ colChar ] = self.STATE_EMPTY

    def setStateOnAreaCoordinates(self, colChar, rowNr, state):
        self.gameStateMatrix[rowNr][colChar] = state

    def getStateOnCoordinates(self, absoluteX, absoluteY):
        123
        #todo: gets state on given global coordinates

    #gets state on given grid coordinates
    def getStateOnAreaCoordinates(self, colChar, rowNr):
        return self.gameStateMatrix[ rowNr ][ colChar ]

    def printGameStateMatrix(self):
        for rowNr, rowValues in self.gameStateMatrix.items():
            print(rowNr, rowValues)

    def placeShipToGrid(self, ship, battlefieldGridElement):
        #todo: make this work when direction='vertical'

        colChar = battlefieldGridElement.colChar
        rowNr = battlefieldGridElement.rowNr
        for _ in range(0, ship.length):
            self.setStateOnAreaCoordinates( colChar, rowNr, ship)
            colChar = self.incrementChar( colChar )

    def incrementChar(self, char):
        return chr(ord(char) + 1)

    def generateSimplifiedMatrix(self):
        simplifiedMatrix = []
        for rowNr, rowElements in self.gameStateMatrix.items():
            row = []
            for colChar, element in rowElements.items():
                simplifiedElement = self.generateSimplifiedElement( element )
                row.append( simplifiedElement )
            simplifiedMatrix.append(row)
        self.print_matrix(simplifiedMatrix)
        return simplifiedMatrix

    def generateSimplifiedElement(self, gameStateMatrixElement):
        if gameStateMatrixElement==self.STATE_EMPTY:
            simplifiedElement = '0'
        else:
            simplifiedElement = 'X'
        return simplifiedElement

    def print_matrix(self, matrix):
        for row in matrix:
            print(row)
