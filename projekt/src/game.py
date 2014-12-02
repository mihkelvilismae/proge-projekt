__author__ = 'mihkel'

from .ships import Ship
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

    def startGame(self):
        self.screen.drawGameScreenView()
        self.createShips()
        self.setupShipsInPort()

    def __init__(self, **kwargs):
        1
        #self.bind(selectedShip=self.onSelectedShipChange)

    def setSelectedShip(self, ship):
        self.unselectShips( ship )
        self.selectedShip = ship

    #def onSelectedShipChange(self, instance, newValue):
    #    #print('seelectedwdaw')
    #    1

    def createShips(self):
        shipsCountByLength = {1:4, 2:3, 3:2, 4:1}
        #shipsCountByLength = {4:1}
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
        if ship.isInPort:
            ship.isInPort = False
            ship.shipPier.removeShip( ship )
            self.battleArea.add_widget( ship )
            ship.drawShip()
        ship.shipStatus = ship.STATUS_PLACED
        ship.placeShip( battlefieldGridElement.pos )
        self.setSelectedShip( ObjectProperty(None) )

    def canRotateShip(self, ship): #todo implement this
        if not isinstance( ship, Ship ):
            return False
        return True

    def rotateShip(self, ship):
        ship.rotateShip()

    def canGridBeBombarded(self, gridElement):
        return True

    def bombardGrid(self, gridElement):
        print('bombardGrid toimus')
        print(gridElement)

    def unselectShips(self, shipNotToUnselect=None):
        for ship in self.ships:
            if ship!=shipNotToUnselect:
                ship.shipStatus = ship.STATUS_WAITING_TO_BE_PICKED_UP

    # @testing
    def testing(self):
        print('-----------------TESTING START------------------------')
        xxx = self.shipPort
        print('shipport', xxx.pos, xxx.to_window(xxx.pos[0],xxx.pos[1]))
        xxx = xxx.parent
        print('parent', xxx)
        print('parent', xxx.pos, xxx.to_window(xxx.pos[0],xxx.pos[1]))
        print('parent', xxx.size)
        #for rect in ship.shipRectangles:
        #    print('rect',rect, rect.pos, rect.to_window(rect.pos[0],rect.pos[1]))
        print('-----------------TESTING END------------------------')


