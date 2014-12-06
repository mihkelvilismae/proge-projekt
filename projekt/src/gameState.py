__author__ = 'mihkel'
from .gameconfig import MainConfig



import collections
#----------------------------------------------------------------------------------------------------------------
#   GameStateMatrix
#----------------------------------------------------------------------------------------------------------------
class GameStateMatrix():

    def addShipZoneToMatrix(self, ship, battlefieldGridElement):
        for areaPosition in self.getAreasAroundShip(  ship, battlefieldGridElement ):
            self.setStateOnAreaCoordinates( areaPosition[0], areaPosition[1], self.STATE_SHIPZONE)

    def print_matrix(self, matrix):
        for row,x in enumerate(matrix):
            print(x)
    def setStateOnAreaCoordinates(self, colChar, rowNr, state):
        #currentState = self.gameStateMatrix[rowNr][colChar]
        #if currentState == self.STATE_EMPTY:
        #    newState = state
        #else:
        self.gameStateMatrix[rowNr][colChar] = state

    def getStateOnCoordinates(self, absoluteX, absoluteY):
        123
        #todo: gets state on given global coordinates

    #gets state on given grid coordinates
    def getStateOnAreaCoordinates(self, colChar, rowNr):
        if rowNr in self.gameStateMatrix and colChar in self.gameStateMatrix[rowNr]:
            return self.gameStateMatrix[ rowNr ][ colChar ]
        else:
            return False

    def printGameStateMatrix(self):
        for rowNr, rowValues in self.gameStateMatrix.items():
            print(rowNr, rowValues)

    def getAreasAroundShip(self, ship, battlefieldGridElement):
        areasAroundShip = []
        if ship.direction == ship.DIRECTION_HORIZONTAL:
            zoneAreaWidth = ship.length+2
            zoneAreaHeight = 3
        else:
            zoneAreaHeight = ship.length+2
            zoneAreaWidth = 3

        zoneAreaColChar = self.decrementChar( battlefieldGridElement.colChar )
        for _ in range(0, zoneAreaWidth):
            zoneAreaRowNr = battlefieldGridElement.rowNr-1
            for _ in range(0, zoneAreaHeight):
                if zoneAreaColChar in MainConfig().columnChars and zoneAreaRowNr in MainConfig().rowNumbers:
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
            for colChar, element in rowElements.items():
                simplifiedElement = self.generateSimplifiedElement( element )
                row.append( simplifiedElement )
            simplifiedMatrix.append(row)
        self.print_matrix(simplifiedMatrix)
        return simplifiedMatrix

#TODO: REPLACED THIS:
    def generateSimplifiedElement(self, gameStateMatrixElement):
        if gameStateMatrixElement==self.STATE_EMPTY:
            simplifiedElement = '0'
        elif gameStateMatrixElement==self.STATE_SHIPZONE:
            simplifiedElement = 'Z'
        else:
            simplifiedElement = 'X'
        return simplifiedElement

    def print_matrix(self, matrix):
        for row,x in enumerate(matrix):
            print(x)

    def isShipPositionValidX( self, ship, battlefieldGridElement ):
        #todo: make this work when direction='vertical'
        colChar = battlefieldGridElement.colChar
        rowNr = battlefieldGridElement.rowNr
        for _ in range(0, ship.length):
            stateOnPosition = self.getStateOnAreaCoordinates( colChar, rowNr )
            if stateOnPosition != self.STATE_EMPTY:
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
                self.gameStateMatrix[ rowNr ][ colChar ] = self.STATE_EMPTY

    def placeShipInGameStateMatrix(self, ship, battlefieldGridElement):
        self.addShipZoneToMatrix( ship, battlefieldGridElement )
        #todo: make this work when direction='vertical'

        colChar = battlefieldGridElement.colChar
        rowNr = battlefieldGridElement.rowNr
        for _ in range(0, ship.length):
            self.setStateOnAreaCoordinates( colChar, rowNr, ship)
            colChar = self.incrementChar( colChar )


    def isShipPositionValid(self, ship, battlefieldGridElement):
        return self.isShipPositionValidX( ship, battlefieldGridElement )


