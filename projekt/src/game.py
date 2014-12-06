__author__ = 'mihkel'

from .ships import Ship
from .grid import Grid

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
        shipsCountByLength = {1:4, 2:3, 3:2, 4:1}
        shipsCountByLength = {4:1}
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
        if not isinstance( ship, Ship ):
            return False
        return True

    def placeShipToGrid(self, ship, battlefieldGridElement):

        #removes ship from port
        if ship.isInPort:
            ship.isInPort = False
            ship.shipPier.removeShip( ship )
            self.battleArea.add_widget( ship )
            ship.drawShip()

        ship.shipStatus = ship.STATUS_PLACED
        ship.placeShip( battlefieldGridElement.pos )
        self.setSelectedShip( ObjectProperty(None) )
        grid = battlefieldGridElement.getParentByClass(Grid)
        grid.gameState.placeShipToGrid( ship, battlefieldGridElement)

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
                ship.shipStatus = ship.STATUS_WAITING_TO_BE_PICKED_UP

    def onAllShipsOnGrid(self, instance, pos):
        self.screen.gameScreenView.drawStartingButton()
        self.screen.gameScreenView.removeShipPort()

    # @testing
    def testing(self):
        print('-----------------TESTING START------------------------')
        #print(self.testingMainGrid.gameState.getStateOnAreaCoordinates('A',2))
        #print(self.testingMainGrid.gameState.printGameStateMatrix())
        #self.testingMainGrid.gameState.generateSimplifiedMatrix()
        for ship in self.ships:
            ship.addZone()
            #ship.shipZone.draw()
        #for rect in ship.shipRectangles:
        #    print('rect',rect, rect.pos, rect.to_window(rect.pos[0],rect.pos[1]))
        print('-----------------TESTING END------------------------')


