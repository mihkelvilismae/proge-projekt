__author__ = 'mihkel'

from .ships import Ship
from .grid import Grid
from .gameconfig import MainConfig

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
#---------------------------------------------------------------------------------------------------
#       @Game
#---------------------------------------------------------------------------------------------------
game = None #FIXME: SEE BELOW IN MAIN APP

class Game( Widget ):
    selectedShip = ObjectProperty(None)
    ships = list()
    screen = None
    mainGrid = None
    shipPort = None
    battleArea = None
    allShipsOnGrid = BooleanProperty(False)

    testingMainGrid = None #fixme: remove this later
    #gameState = None

    def __init__(self, **kwargs):
        self.mainConfig = MainConfig()
        self.bind(allShipsOnGrid=self.onAllShipsOnGrid)

    def startGame(self):
        self.screen.drawGameScreenView()
        self.createShips()
        self.setupShipsInPort()

    def startBattle(self, instance):
        pass

    def setSelectedShip(self, ship):
        self.unselectShips( ship )
        self.selectedShip = ship


    #def onSelectedShipChange(self, instance, newValue):
    #    1

    def createShips(self):
        shipsCountByLength = {1:1}
        shipsCountByLength = {1:4, 2:3, 3:2, 4:1}
        for shipLength, shipCount in shipsCountByLength.items():
            for _ in range(0, shipCount):
                ship = Ship( shipLength )
                ship.game = self
                self.ships.append( ship )

    def setupShipsInPort(self):
        for ship in self.ships:
            self.placeShipToPort( ship )

    def placeShipToPort(self, ship):
        self.shipPort.shipPiers[ship.length].addShip( ship )

    def canShipBePlaced(self, ship, battlefieldGridElement): #todo implement logic for out of borders etc
        colChar = battlefieldGridElement.colChar
        rowNr = battlefieldGridElement.rowNr
        if isinstance( ship, Ship ) and battlefieldGridElement.getGameState().isShipPositionValid( ship, colChar, rowNr ):
            return True
        return False

    def temporarilyRemoveShipFromMatrix(self, ship):
        if ship.isInPort==False:
            ship.temporarilyRemovedFromMatrix = True
            ship.getGrid().gameState.removeShipFromGameStateMatrix( ship )
        #    ship.shipStateMatrixElementsTemp = ship.shipStateMatrixElements.copy()
        #    ship.shipStateMatrixElementsTemp = ship.shipStateMatrixElements.copy()


    def placeShipToGrid(self, ship, battlefieldGridElement):
        ship.temporarilyRemovedFromMatrix = False
        #removes ship from port
        if ship.isInPort:
            ship.isInPort = False
            ship.shipPier.removeShip( ship )
            self.battleArea.add_widget( ship )
            ship.drawShip()

        ship.shipStatus = ship.STATUS_PLACED
        ship.placeShip( battlefieldGridElement.pos )
        ship.startColChar = battlefieldGridElement.colChar
        ship.startRowNr = battlefieldGridElement.rowNr
        self.setSelectedShip( ObjectProperty(None) )
        grid = battlefieldGridElement.getGrid()
        grid.gameState.placeShipInGameStateMatrix( ship, battlefieldGridElement.colChar, battlefieldGridElement.rowNr )

        #def drawZone(dt):
        #    ship.addZone()
        #Clock.schedule_once(drawZone, 0)

    def canRotateShip(self, ship): #todo implement this
        if not isinstance( ship, Ship ):
            return False
        return True

    def rotateShip(self, ship):
        ship.rotateShip()

    def canGridBeBombarded(self, gridElement):
        if gridElement.isBombed == False:
            return True

    def bombardGrid(self, gridElement):
        gridElement.bombard()

    def unselectShips(self, shipNotToUnselect=None):
        for ship in self.ships:
            if ship!=shipNotToUnselect:
                if ship.temporarilyRemovedFromMatrix == True:
                    ship.temporarilyRemovedFromMatrix = False
                    ship.getGrid().gameState.placeShipInGameStateMatrix( ship, ship.startColChar, ship.startRowNr )
                ship.shipStatus = ship.STATUS_WAITING_TO_BE_PICKED_UP

    def onAllShipsOnGrid(self, instance, pos):
        self.screen.gameScreenView.drawStartingButton()
        self.screen.gameScreenView.removeShipPort()

    # @testing
    def testing(self):
        print('-----------------TESTING START------------------------')
        #print(self.testingMainGrid.gameState.getStateOnAreaCoordinates('A',2))
        #print(self.testingMainGrid.gameState.printGameStateMatrix())
        self.testingMainGrid.gameState.getGameStateMatrixSerialized()
        #for ship in self.ships:
        #     if ship.length==4:
        #        print(ship)
        #    ship.addZone()
            #ship.shipZone.draw()
        #for rect in ship.shipRectangles:
        #    print('rect',rect, rect.pos, rect.to_window(rect.pos[0],rect.pos[1]))
        print('-----------------TESTING END------------------------')


