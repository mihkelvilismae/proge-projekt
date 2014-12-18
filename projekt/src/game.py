__author__ = 'mihkel'

from .ships import Ship
from .battleStatus import BattleStatus
from .gameconfiguration import MainConfig
from .ai import AI
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

    def __init__(self, **kwargs):
        self.AI = AI()
        self.xxx = [('A',1),('B',1),('C',1)]
        self.mainConfig = MainConfig()
        self.bind(allShipsOnGrid=self.onAllShipsOnGrid)
        self.enemyShipGridArea = None

        #fixme: temporary
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

        #----------------------------
        #----------------------------
        # kui self.AI.getEnemyShipPlacement() on allpool, siis kasutab sinu funktsiooni tulemust,
        # kui self.shipPlacementArea.grid.gameState.getGameStateMatrixSerialized() on allpool, siis kasutab sama paigust, mida sinu laevad omavad
        serializedGameState = self.AI.getEnemyShipPlacementDict()
        serializedGameState = self.shipPlacementArea.grid.gameState.getGameStateMatrixSerialized()
        print('AI-ST', serializedGameState)
        #----------------------------
        #----------------------------


        self.battleStatus = BattleStatus( serializedGameState )
        self.screen.gameScreenView.removeWidgetFromGameScreenView( self.screen.gameScreenView.startingButton )
        self.screen.gameScreenView.removeWidgetFromGameScreenView( self.shipPlacementArea )
        self.screen.gameScreenView.drawEnemyShipGridArea()
        self.screen.gameScreenView.drawOwnShipGridArea()
        self.allowBombardment( self.enemyShipGridArea.grid )

        self.screen.gameScreenView.drawShipPort()
        self.shipPort.isSelectShipsAllowed = False
        self.populateEnemyPort()

        serializedGameState = self.shipPlacementArea.grid.gameState.getGameStateMatrixSerialized()
        def populateGridFromSerializedGameState(dt): #fixme: why is the clock required, how can i do it without it :S
            self.populateGridFromSerializedGameState( self.ownShipGridArea.grid, serializedGameState )
        Clock.schedule_once(populateGridFromSerializedGameState, 0)

    def bombardGrid(self, gridElement):
        bombardResult = self.battleStatus.bombardGrid( gridElement.colChar, gridElement.rowNr)
        if bombardResult['result']==BattleStatus.BOMBARD_RESULT_HIT:
            #print('XXXXX PROCESS HIT')
            pass
        elif bombardResult['result']==BattleStatus.BOMBARD_RESULT_MISS:
            #print('XXXXX PROCESS miss')
            pass
        else: #a ship is sunk
            print(bombardResult['sunkship'])
            sunkShip = self.putSunkShipOnEnemyGrid( bombardResult['sunkship'] )
            self.lockShipZoneGridElements( sunkShip )
            if bombardResult['gameOver']==True:
                self.endGame( True )
        gridElement.bombard( bombardResult['result'] )

        self.enemyTurn()

    def enemyTurn(self):
        enemyBombardmentResult = None
        myShipsLeftOnGrid = self.ownShipGridArea.grid.gameState.getNumberOfShipsLeftOnGrid()
        enemyBombardment = self.getEnemyBombardmentPosition()
        self.ownShipGridArea.grid.getGridElementOnPosition( enemyBombardment[0], enemyBombardment[1] ).bombard(BattleStatus.BOMBARD_RESULT_ENEMY_BOMBED_MY_GRID) #todo: this should use mode complex logic
        if self.ownShipGridArea.grid.gameState.getMatrixElement( enemyBombardment[0], enemyBombardment[1] ).ship != None:
            enemyBombardmentResult = BattleStatus.BOMBARD_RESULT_HIT
            self.ownShipGridArea.grid.gameState.getMatrixElement( enemyBombardment[0], enemyBombardment[1] ).removeShip(  )
        if myShipsLeftOnGrid!=self.ownShipGridArea.grid.gameState.getNumberOfShipsLeftOnGrid():
            enemyBombardmentResult = BattleStatus.BOMBARD_RESULT_SUNK
        if self.ownShipGridArea.grid.gameState.areUnsunkShipsLeftOnGrid()==False:
            self.endGame(False)

        if enemyBombardmentResult == None:
            enemyBombardmentResult = BattleStatus.BOMBARD_RESULT_MISS

        self.AI.setBombingResult( enemyBombardmentResult )

    def getEnemyBombardmentPosition(self):
        import random
        position = random.randint(0,len(self.suitableEnemyPositions)-1)
        return self.suitableEnemyPositions.pop(position)

        return self.AI.giveCoordinatesToBomb()


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

    def createShips(self, gridConfig):
        ships = []
        shipsCountByLength = {1:4}
        shipsCountByLength = {4:1}
        shipsCountByLength = {2:2}
        shipsCountByLength = {2:1}
        shipsCountByLength = {1:1, 4:1}
        shipsCountByLength = {1:4, 2:3, 3:2, 4:1}
        shipsCountByLength = {1:1}
        for shipLength, shipCount in shipsCountByLength.items():
            for _ in range(0, shipCount):
                ship = Ship( gridConfig, shipLength )
                ship.game = self
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

    def onAllShipsOnGrid(self, instance, pos):
        self.screen.gameScreenView.drawStartingButton()
        self.screen.gameScreenView.removeShipPort()

    def testing(self):

        print('-----------------TESTING START------------------------')
        #print('ownshps', self.ownShipGridArea.grid.gameState.getGameStateMatrixSerialized())
        #self.AI.isolateAreaHelp(9,9,None,3,2,None)
        print(self.AI.ships)

        print('-----------------TESTING END------------------------')
        #print('enemyships', self.enemyShipGridArea.ships)