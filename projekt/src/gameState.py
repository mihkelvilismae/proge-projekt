__author__ = 'mihkel'
from .gameconfig import MainConfig
from .gameStateMatrixElement import GameStateMatrixElement


import collections
#----------------------------------------------------------------------------------------------------------------
#   GameStateMatrix
#----------------------------------------------------------------------------------------------------------------
class GameStateMatrix():

    def getStateOnAreaCoordinates(self, colChar, rowNr):
        return self.getMatrixElement(colChar, rowNr)

    def getMatrixElement(self, colChar, rowNr):
        if rowNr in self.gameStateMatrix and colChar in self.gameStateMatrix[rowNr]:
            return self.gameStateMatrix[ rowNr ][ colChar ]
        else:
            return False

    def addShipZoneToMatrix(self, ship, colChar, rowNr):
        for areaPosition in self.getAreasAroundShip(  ship, colChar, rowNr ):
            if self.checkIfPositionExists(areaPosition[0], areaPosition[1]):
                matrixElement = self.getMatrixElement(areaPosition[0], areaPosition[1])
                matrixElement.addChild( self.STATE_SHIPZONE )
                ship.shipZoneStateMatrixElements.append( matrixElement )

    def print_matrix(self, matrix):
        for row,x in enumerate(matrix):
            print(x)

    def getStateOnCoordinates(self, absoluteX, absoluteY):
        123
        #todo: gets state on given global coordinates

    def printGameStateMatrix(self):
        for rowNr, rowValues in self.gameStateMatrix.items():
            print(rowNr, rowValues)

    def getAreasAroundShip(self, ship, colChar, rowNr):
        areasAroundShip = []
        if ship.direction == ship.DIRECTION_HORIZONTAL:
            zoneAreaWidth = ship.length+2
            zoneAreaHeight = 3
        else:
            zoneAreaHeight = ship.length+2
            zoneAreaWidth = 3

        zoneAreaColChar = self.decrementChar( colChar )
        for _ in range(0, zoneAreaWidth):
            zoneAreaRowNr = rowNr-1
            for _ in range(0, zoneAreaHeight):
                if zoneAreaColChar in MainConfig().columnChars and zoneAreaRowNr in MainConfig().rowNumbers:
                #if self.checkIfPositionExists(zoneAreaColChar, zoneAreaRowNr):
                    areasAroundShip.append((zoneAreaColChar, zoneAreaRowNr))
                zoneAreaRowNr += 1
            zoneAreaColChar = self.incrementChar(zoneAreaColChar)

        return areasAroundShip

    def incrementChar(self, char):
        return chr(ord(char) + 1)

    def decrementChar(self, char):
       return chr(ord(char) - 1)

    def checkIfPositionExists(self, colChar, rowNr):
        return rowNr in self.gameStateMatrix and colChar in self.gameStateMatrix[rowNr]

    def generateSimplifiedMatrix(self):
        simplifiedMatrix = []
        for rowNr, rowElements in self.gameStateMatrix.items():
            row = []
            for colChar, matrixElement in rowElements.items():
                simplifiedElement = matrixElement.getSimplifiedElement()
                row.append( simplifiedElement )
            simplifiedMatrix.append(row)
        self.print_matrix(simplifiedMatrix)
        return simplifiedMatrix

    def print_matrix(self, matrix):
        for row,x in enumerate(matrix):
            print(x)

    def isShipPositionValidX( self, ship, colChar, rowNr ):
        #todo: make this work when direction='vertical'
        for _ in range(0, ship.length):
            stateOnPosition = self.getStateOnAreaCoordinates( colChar, rowNr )
            if stateOnPosition == False or not stateOnPosition.isEmpty():
                return False
            colChar = self.incrementChar( colChar )
        return True


#----------------------------------------------------------------------------------------------------------------
#   GameState
#       This class handles most checks, such as possibility to rotate or place ships
#----------------------------------------------------------------------------------------------------------------
class GameState( GameStateMatrix ):
    STATE_EMPTY = 'empty'
    STATE_SHIPZONE = 'shipzone'

    gameStateMatrix = collections.OrderedDict()

    def __init__(self, grid):
        self.grid = grid

    def createGameStateMatrix(self):
        for rowNr, rowElements in self.grid.gridElements.items():
            self.gameStateMatrix[ rowNr ] = collections.OrderedDict()
            for colChar, element in rowElements.items():
                self.gameStateMatrix[ rowNr ][ colChar ] = GameStateMatrixElement(self, colChar, rowNr)

    def placeShipInGameStateMatrix(self, ship, colChar, rowNr):
        self.addShipZoneToMatrix( ship, colChar, rowNr )
        #todo: make this work when direction='vertical'

        for _ in range(0, ship.length):
            self.getMatrixElement(colChar, rowNr).addShip( ship )
            colChar = self.incrementChar( colChar )

    def removeShipFromGameStateMatrix(self, ship):
        for shipStateMatrixElement in ship.shipStateMatrixElements.copy():
            shipStateMatrixElement.removeShip()
        for shipZoneStateMatrixElement in ship.shipZoneStateMatrixElements.copy():
            ship.shipZoneStateMatrixElements = []
            shipZoneStateMatrixElement.removeChild(self.STATE_SHIPZONE)


    def isShipPositionValid(self, ship, colChar, rowNr):
        return self.isShipPositionValidX( ship, colChar, rowNr )


