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


    allShipsOnGrid = BooleanProperty(False)
    activeArea = None

    #testingMainGrid = None #fixme: remove this later
    #gameState = None

    def __init__(self, **kwargs):

        self.xxx = [('A',1),('B',1),('C',1)]
        self.mainConfig = MainConfig()
        self.bind(allShipsOnGrid=self.onAllShipsOnGrid)
        self.enemyShipGridArea = None

        #fixme: temporary
        #self.suitableEnemyPositions = [(x.colChar, x.rowNr) for x in self.ownShipGridArea.grid.gridElements]
        self.suitableEnemyPositions = []
        for rowNumber in [1,2,3,4,5,6,7,8,9,10]:
            for colChar in list('ABCDEFGHIJ'):
                self.suitableEnemyPositions.append((colChar, rowNumber))

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

        def populateGridFromSerializedGameState(dt): #fixme: why is the clock required, how can i do it without it :S
            self.populateGridFromSerializedGameState( self.ownShipGridArea.grid, serializedGameState )
        Clock.schedule_once(populateGridFromSerializedGameState, 0)

    def bombardGrid(self, gridElement):
        bombardResult = self.battleStatus.bombardGrid( gridElement.colChar, gridElement.rowNr)
        if bombardResult['result']==BattleStatus.BOMBARD_RESULT_HIT:
            print('XXXXX PROCESS HIT')
        elif bombardResult['result']==BattleStatus.BOMBARD_RESULT_MISS:
            print('XXXXX PROCESS miss')
        else: #a ship is sunk
            print(bombardResult['sunkship'])
            sunkShip = self.putSunkShipOnEnemyGrid( bombardResult['sunkship'] )
            self.lockShipZoneGridElements( sunkShip )
            if bombardResult['gameOver']==True:
                self.endGame( True )
        gridElement.bombard( bombardResult['result'] )

        self.enemyTurn()

    def enemyTurn(self):
        enemyBombardment = self.getEnemyBombardmentPosition()
        self.ownShipGridArea.grid.getGridElementOnPosition( enemyBombardment[0], enemyBombardment[1] ).bombard(BattleStatus.BOMBARD_RESULT_ENEMY_BOMBED_MY_GRID) #todo: this should use mode complex logic
        if self.ownShipGridArea.grid.gameState.getMatrixElement( enemyBombardment[0], enemyBombardment[1] ).ship != None:
            self.ownShipGridArea.grid.gameState.getMatrixElement( enemyBombardment[0], enemyBombardment[1] ).removeShip(  )
        if self.ownShipGridArea.grid.gameState.areUnsunkShipsLeftOnGrid()==False:
            self.endGame(False)

    def getEnemyBombardmentPosition(self):
        #suitablePostition = self.ownShipGridArea.grid.gridElements
        #return self.xxx.pop()
        import random
        position = random.randint(0,len(self.suitableEnemyPositions)-1)
        return self.suitableEnemyPositions.pop(position)

    def disallowBombardment(self, grid):
        grid.isBombardmentAllowed = False
    def allowBombardment(self, grid):
        grid.isBombardmentAllowed = True
    def disallowPlacement(self, grid):
        grid.isPlacementAllowed = False
    def allowPlacement(self, grid):
        grid.isPlacementAllowed = True

    def canGridElementBeBombarded(self, gridElement):
        if gridElement.isBombed == False and gridElement.isLocked == False and gridElement.getGrid().isBombardmentAllowed==True:
            return True

    def lockShipZoneGridElements(self, ship):
        for shipZoneStateMatrixElement in ship.shipZoneStateMatrixElements:
            gridElement = self.enemyShipGridArea.grid.getGridElementOnPosition( shipZoneStateMatrixElement.colChar, shipZoneStateMatrixElement.rowNr)
            gridElement.isLocked = True

    def endGame(self, didHumanWin):
        self.disallowBombardment( self.enemyShipGridArea.grid )
        self.screen.gameScreenView.drawGameOverText( didHumanWin )

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
        shipsCountByLength = {1:4}
        shipsCountByLength = {4:1}
        shipsCountByLength = {1:1}
        shipsCountByLength = {1:1, 4:1}
        shipsCountByLength = {1:4, 2:3, 3:2, 4:1}
        for shipLength, shipCount in shipsCountByLength.items():
            for _ in range(0, shipCount):
                ship = Ship( gridConfig, shipLength )
                ship.game = self
                #self.ships.append( ship )
                ships.append( ship )
        return ships

    def setupShipsInPort(self, ships):
        for ship in ships:
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
        #print('placeshptogird', ship)
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
        #temporarily set other direction
        self.flipShipRotation(ship)
        print(ship.direction)
        if not isinstance( ship, Ship ) or ship.isInPort or not self.canShipBePlaced( ship, self.shipPlacementArea.grid.getGridElementOnPosition(ship.startColChar, ship.startRowNr)):
            result = False
        else:
            result = True
        self.flipShipRotation(ship)

        return result

    def flipShipRotation(self, ship):
        if ship.direction==Ship.DIRECTION_HORIZONTAL:
            ship.direction = Ship.DIRECTION_VERTICAL
        else:
            ship.direction=Ship.DIRECTION_HORIZONTAL

    def rotateShip(self, ship):
        ship.rotateShip()
        self.placeShipToGrid(ship, self.shipPlacementArea.grid.getGridElementOnPosition(ship.startColChar, ship.startRowNr))
        #ship.shipStatus = Ship.STATUS_PLACED
        self.unselectShips()

    def putSunkShipOnEnemyGrid(self, sunkShipInfo):
        ship = self.shipPort.getShipByLength(sunkShipInfo['length'])
        ship.direction = sunkShipInfo['direction']
        self.placeShipToGrid( ship, self.enemyShipGridArea.grid.getGridElementOnPosition(sunkShipInfo['startColChar'], sunkShipInfo['startRowNr']) )
        return ship

    def unselectShips(self, shipNotToUnselect=None):
        for ship in self.activeArea.ships:
            if ship!=shipNotToUnselect:
                if ship.temporarilyRemovedFromMatrix == True:
                    ship.temporarilyRemovedFromMatrix = False
                    ship.getGrid().gameState.placeShipInGameStateMatrix( ship, ship.startColChar, ship.startRowNr )
                    ship.shipStatus = ship.STATUS_PLACED
                ship.shipStatus = ship.STATUS_WAITING_TO_BE_PICKED_UP
                #if ship.isInPort==True:
                #    ship.shipStatus = ship.STATUS_WAITING_TO_BE_PICKED_UP

                #else:
                #    ship.shipStatus = ship.STATUS_PLACED

    def onAllShipsOnGrid(self, instance, pos):
        self.screen.gameScreenView.drawStartingButton()
        self.screen.gameScreenView.removeShipPort()

    def testing(self):

        print('-----------------TESTING START------------------------')
        if (self.selectedShip):
            print(self.selectedShip.length)
            print(self.selectedShip.shipStatus)
            print(self.selectedShip.direction)
        else:
            print('noe selectedd')
        print('-----------------TESTING END------------------------')
        #print('ownshps', self.ownShipGridArea.grid.gameState.ships)
        #print('enemyships', self.enemyShipGridArea.ships)

    def _testing(self):
        #print('-----------------TESTING START------------------------')
        #print(self.testingMainGrid.gameState.getStateOnAreaCoordinates('A',2))
        #print(self.testingMainGrid.gameState.printGameStateMatrix())
        #print('BATTLEAREA-----------------------------------')
        self.shipPlacementArea.grid.gameState.generateSimplifiedMatrix()
        print(id(self.shipPlacementArea.grid.gameState))
        if self.ownShipGridArea:
            #print('ownShipGridArea -----------------------------------')
            print(id(self.ownShipGridArea.grid.gameState))
            self.ownShipGridArea.grid.gameState.generateSimplifiedMatrix()
        #for ship in self.ships:
        #     if ship.length==4:
        #        print(ship)
        #    ship.addZone()
            #ship.shipZone.draw()
        #for rect in ship.shipRectangles:
        #    #print('rect',rect, rect.pos, rect.to_window(rect.pos[0],rect.pos[1]))
        #print('-----------------TESTING END------------------------')


