__author__ = 'mihkel'

class BattleStatus():

    BOMBARD_RESULT_HIT = 'hit'
    BOMBARD_RESULT_SUNK = 'sunk'
    BOMBARD_RESULT_MISS = 'miss'
    #BOMBARD_SPECIAL_RESULT_GAME_OVER = 'gameOver'

    enemyShipsInfo = []

    def __init__(self, enemyShipsInfo):
        self.enemyShipsInfo = enemyShipsInfo

    def bombardGrid(self, colChar, rowNr):
        if self.isShipOnPosition( colChar, rowNr ):
            shipOnPosition = self.getShipOnPosition( colChar, rowNr)
            shipOnPosition['shipPositions'].remove((colChar,rowNr))
            if len(shipOnPosition['shipPositions'])==0:
                self.removeShipFromBattleStatus( shipOnPosition['shipId'] )
                bombardmentResult = {'sunkship':shipOnPosition, 'result':self.BOMBARD_RESULT_SUNK}
                if len(self.enemyShipsInfo['ships'])==0:
                    bombardmentResult['gameOver']=True
            else:
                bombardmentResult = {'result':self.BOMBARD_RESULT_HIT}
        else:
            bombardmentResult = {'result':self.BOMBARD_RESULT_MISS}
        bombardmentResult = dict(list({'gameOver':False}.items()) + list(bombardmentResult.items())) #merge
        return bombardmentResult

    def isShipOnPosition(self, colChar, rowNr):
        return self.getShipOnPosition(colChar, rowNr)!=None

    def getShipOnPosition(self, colChar, rowNr):
        if self.createPositionId(colChar,rowNr) in self.enemyShipsInfo['shipsByPosition']:
            return self.getShip( self.enemyShipsInfo['shipsByPosition'][ self.createPositionId(colChar,rowNr) ] )
        return None

    def removeShipFromBattleStatus(self, shipId):
        self.enemyShipsInfo['ships'].pop( shipId )
    #def getShipPositionsByShip(self, shipId):
    #    return self.enemyShipsInfo['positionsByShip'][shipId]

    def getShip(self, shipId):
        return self.enemyShipsInfo[ 'ships' ][ shipId ]

    def createPositionId(self, colChar, rowNr):
        return colChar+str(rowNr)
