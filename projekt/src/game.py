__author__ = 'mihkel'

from .ships import Ship
from .battleStatus import BattleStatus
from .grid import Grid
from .gameconfig import MainConfig
from .views import GridArea

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty, DictProperty
#---------------------------------------------------------------------------------------------------
#       @Game
#---------------------------------------------------------------------------------------------------
game = None #FIXME: SEE BELOW IN MAIN APP

class Game( Widget ):
    selectedShip = ObjectProperty(None)
    screen = None
    shipPort = ObjectProperty(None)
    battleStatus = None

    shipPlacementArea = None
    ownShipGridArea = None
    enemyShipGridArea = None

    allShipsOnGrid = BooleanProperty(False)
    activeArea = None

    #testingMainGrid = None #fixme: remove this later
    #gameState = None

    def __init__(self, **kwargs):
        self.mainConfig = MainConfig()
        self.bind(allShipsOnGrid=self.onAllShipsOnGrid)

    def startGame(self):
        self.screen.drawGameScreenView()
        self.allowPlacement( self.shipPlacementArea.grid )
        ships = self.createShips( self.shipPlacementArea.grid.gridConfig )
        self.activeArea.ships = ships
        self.setupShipsInPort( ships )

    def startBattle(self, instance):
        self.unselectShips()
        serializedGameState = self.shipPlacementArea.grid.gameState.getGameStateMatrixSerialized()
        print(serializedGameState)
        self.battleStatus = BattleStatus( serializedGameState )
        self.screen.gameScreenView.removeWidgetFromGameScreenView( self.screen.gameScreenView.startingButton )
        self.screen.gameScreenView.removeWidgetFromGameScreenView( self.shipPlacementArea )
        self.screen.gameScreenView.drawEnemyShipGridArea()
        self.screen.gameScreenView.drawOwnShipGridArea()
        self.allowBombardment( self.enemyShipGridArea.grid )

        self.screen.gameScreenView.drawShipPort()
        self.shipPort.isSelectShipsAllowed = False
        self.populateEnemyPort()

        print('luukas see shpport', self.shipPort, self.shipPort.isSelectShipsAllowed)


        def populateGridFromSerializedGameState(dt): #fixme: why is the clock required, how can i do it without it :S
            self.populateGridFromSerializedGameState( self.ownShipGridArea.grid, serializedGameState )
        Clock.schedule_once(populateGridFromSerializedGameState, 0)


    def disallowBombardment(self, grid):
        grid.isBombardmentAllowed = False
    def allowBombardment(self, grid):
        grid.isBombardmentAllowed = True
    def disallowPlacement(self, grid):
        grid.isPlacementAllowed = False
    def allowPlacement(self, grid):
        grid.isPlacementAllowed = True

    def canGridElementBeBombarded(self, gridElement):
        if gridElement.isBombed == False and gridElement.getGrid().isBombardmentAllowed==True:
            return True

    def bombardGrid(self, gridElement):
        bombardResult = self.battleStatus.bombardGrid( gridElement.colChar, gridElement.rowNr)
        if bombardResult['result']==BattleStatus.BOMBARD_RESULT_HIT:
            print('XXXXX PROCESS HIT')
        elif bombardResult['result']==BattleStatus.BOMBARD_RESULT_MISS:
            print('XXXXX PROCESS miss')
        else: #a ship is sunk
            self.putSunkShipOnEnemyGrid( bombardResult['sunkship'] )
            if bombardResult['gameOver']==True:
                self.endGame()
        gridElement.bombard()

    def endGame(self):
        self.disallowBombardment( self.enemyShipGridArea.grid )
        self.screen.gameScreenView.drawGameOverText()

    def populateEnemyPort(self):
        ships = self.createShips( self.enemyShipGridArea.grid.gridConfig )
        self.setupShipsInPort( ships )

    def populateGridFromSerializedGameState(self, grid, serializedGameState):
        ships = self.createShips( grid.gridConfig )
        grid.getParentByClass(GridArea).ships = ships
        for ship in ships:
            shipStatusInfo = serializedGameState['shipsByLength'][ship.length].pop()
            ship.direction = shipStatusInfo['direction']
            self.placeShipToGrid( ship, grid.getGridElementOnPosition(shipStatusInfo['startColChar'], shipStatusInfo['startRowNr']) )

    def canSelectShip(self, ship):
        if ship.isInPort:
            return ship.getShipPort().isSelectShipsAllowed
        else:
            return ship.getGrid().isPlacementAllowed

    def setSelectedShip(self, ship):
        self.unselectShips( ship )
        self.selectedShip = ship


    #def onSelectedShipChange(self, instance, newValue):
    #    1

    def createShips(self, gridConfig):
        ships = []
        shipsCountByLength = {1:4, 2:3, 3:2, 4:1}
        shipsCountByLength = {1:1, 4:1}
        shipsCountByLength = {1:4}
        shipsCountByLength = {4:1}
        for shipLength, shipCount in shipsCountByLength.items():
            for _ in range(0, shipCount):
                ship = Ship( gridConfig, shipLength )
                ship.game = self
                #self.ships.append( ship )
                ships.append( ship )
        return ships

    def setupShipsInPort(self, ships):
        for ship in ships:
            print('placeShipToPort')
            self.placeShipToPort( ship )

    def placeShipToPort(self, ship):
        ship.isInPort = True
        self.shipPort.shipPiers[ship.length].addShip( ship )

    def canShipBePlaced(self, ship, battlefieldGridElement): #todo implement logic for out of borders etc
        if battlefieldGridElement.getGrid().isPlacementAllowed==False:
            return False
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

        if ship.getParentByClass(GridArea)==None:
            shipPlacementArea = battlefieldGridElement.getGrid().getParentByClass( GridArea )
            shipPlacementArea.add_widget( ship )
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

    def putSunkShipOnEnemyGrid(self, sunkShipInfo):
        ship = self.shipPort.getShipByLength(sunkShipInfo['length'])
        self.placeShipToGrid( ship, self.enemyShipGridArea.grid.getGridElementOnPosition(sunkShipInfo['startColChar'], sunkShipInfo['startRowNr']) )
        print('sunkShipInfo', sunkShipInfo)

    def unselectShips(self, shipNotToUnselect=None):
        for ship in self.activeArea.ships:
            if ship!=shipNotToUnselect:
                if ship.temporarilyRemovedFromMatrix == True:
                    ship.temporarilyRemovedFromMatrix = False
                    ship.getGrid().gameState.placeShipInGameStateMatrix( ship, ship.startColChar, ship.startRowNr )
                ship.shipStatus = ship.STATUS_WAITING_TO_BE_PICKED_UP

    def onAllShipsOnGrid(self, instance, pos):
        self.screen.gameScreenView.drawStartingButton()
        self.screen.gameScreenView.removeShipPort()

    # @testing
    def __testing(self):
        for ship in (self.ownShipGridArea.ships):
            print(ship)
            print('zonei päran', ship.shipZone)
            for shipZoneElement in ship.shipZone.shipZoneElements:
                print('zonelemendi:', shipZoneElement, shipZoneElement.pos)
                print('parent:', shipZoneElement.parent)

    def testing(self):
        print('-----------------TESTING START------------------------')
        print(self.screen.gameScreenView)
        print('-----------------TESTING END------------------------')

    def _testing(self):
        print('-----------------TESTING START------------------------')
        #print(self.testingMainGrid.gameState.getStateOnAreaCoordinates('A',2))
        #print(self.testingMainGrid.gameState.printGameStateMatrix())
        print('BATTLEAREA-----------------------------------')
        self.shipPlacementArea.grid.gameState.generateSimplifiedMatrix()
        print(id(self.shipPlacementArea.grid.gameState))
        if self.ownShipGridArea:
            print('ownShipGridArea -----------------------------------')
            print(id(self.ownShipGridArea.grid.gameState))
            self.ownShipGridArea.grid.gameState.generateSimplifiedMatrix()
        #for ship in self.ships:
        #     if ship.length==4:
        #        print(ship)
        #    ship.addZone()
            #ship.shipZone.draw()
        #for rect in ship.shipRectangles:
        #    print('rect',rect, rect.pos, rect.to_window(rect.pos[0],rect.pos[1]))
        print('-----------------TESTING END------------------------')


