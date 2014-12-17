__author__ = 'rainvagel'

from random import randint
class AI():

    playerGrid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    computerGrid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    computerPlanningGrid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #Seda pole kelelgile näha, see lihtsalt arvutile, et ta saaks paremini planeerida
                                        #ning et programmeerijal oleks lihtsam

    # 0 tähendab, et pole pommitatud
    # 1 tähendab, et on pommitatud
    # 2 tähendab, et seal on laev

    ships = {"battleship": 1, "cruiser": 2, "destroyer": 3, "submarine": 4} #Mitu laeva saab mängijal olla
    #Kui mängijate oma on tühi, siis mäng on läbi
    playerShips = {}
    computerShips = {}

    pikkus = 0 #Laeva pikkus
    laevadPikkus = 4
    submarineNumber = 4
    destroyerNumber = 3
    cruiserNumber = 2
    xxx = [1,2,3]

    def isEmpty(anyStructure):  #Vaatab, kas dictionary, list vms on tühi
        if anyStructure:
            return False
        else:
            return True

    def gameOver(self, ships):  #Kui tagastab True, siis on mäng läbi
        if self.isEmpty(ships) is True:
            return True
        else:
            return False

    def checkValue(self, x, y, grid): #Vaatab, mis märge on nendel koordinaatidel
        if grid[y][x] == 0:
            return 0
        elif grid[y][x] == 1:
            return 1
        else:
            return 2

    def controlIso(self, grid):
        for x in grid:
            if x is 1 or x is 2:
                return False
        return True

    def controlForSign(self, grid):
        for x in grid:
            if x is 1:
                return 1
            elif x is 2:
                return 2
            elif x is 0:
                return 0

    def placeShip(self, x, y, grid):
        if self.checkValue(x, y, grid) == 0:
            grid[y][x] = 1
        return grid

    def placeSubmarine(self, grid, submarineNumber):
        shipType = 0
        while submarineNumber != 0:
            x = randint(0, 9)
            y = randint(0, 9)
            pos = 1
            if self.checkValue(x, y, grid) == 0 and self.isolateArea(x, y, grid, shipType, pos) is True:
                self.placeShip(x, y, grid)
            submarineNumber -= 1
        return grid

    def isolateAreaHelp(self, x, y, grid, shipLenght, pos, controlArea):
        if pos == 1:
            if x + shipLenght <= 9 and x - 1 >= 0 and y + 1 <= 9 and y - 1 >= 0:
                a = -1
                while a < y + 1:
                    i = -1
                    while i < x + shipLenght:
                        controlArea.append(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
            elif x + shipLenght <= 9 and x - 1 >= 0 and y + 1 <= 9 and y - 1 < 0:
                a = 0
                while a < y + 1:
                    i = -1
                    while i < x + shipLenght:
                        controlArea.appned(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
            elif x + shipLenght <= 9 and x - 1 >= 0 and y + 1 > 9 and y - 1 >= 0:
                a = -1
                while a + y < 9:
                    i = -1
                    while i < x + shipLenght:
                        controlArea.append(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
            elif x + shipLenght > 9 and x - 1 >= 0 and y + 1 <= 9 and y - 1 >= 0:
                return grid
            elif x + shipLenght <= 9 and x - 1 < 0 and y + 1 <= 9 and y - 1 >= 0:
                a = -1
                while a < y + 1:
                    i = 0
                    while i < x + shipLenght:
                        controlArea.append(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
        elif pos == 2:
            if y + shipLenght <= 9 and y - 1 >= 0 and x + 1 <= 9 and x - 1 >= 0:
                a = -1
                while a < y + shipLenght:
                    i = -1
                    while i < x + 1:
                        controlArea.append(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
            elif y + shipLenght <= 9 and y - 1 >= 0 and x + 1 <= 9 and x - 1 < 0:
                a = -1
                while a < y + shipLenght:
                    i = 0
                    while i < x + 1:
                        controlArea.append(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
            elif y + shipLenght <= 9 and y - 1 >= 0 and x + 1 > 9 and x - 1 >= 0:
                a = -1
                while a < y + shipLenght:
                    i = -1
                    while i + x < 9:
                        controlArea.append(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
            elif y + shipLenght <= 9 and y - 1 < 0 and x + 1 <= 9 and x - 1 >= 0:
                a = 0
                while a < y + shipLenght:
                    i = -1
                    while i < y + shipLenght:
                        controlArea.append(grid[y + a][x + i])
                        i += 1
                    a += 1
                return controlArea
            elif y + shipLenght > 9 and y - 1 >= 0 and x + 1 <= 9 and x - 1 >= 0:
                return grid


    def isolateArea(self, x, y, grid, shipType, pos):  #Pos 1 = horisontaalselt ja pos 2 = vertikaalselt
        length = [1, 2, 3, 4]
        shipLenght = length[shipType]
        controlArea = []
        return self.controlIso(self.isolateAreaHelp(x, y, grid, shipLenght, pos, controlArea))

    def placeDestroyer(self, grid, destroyerNumber):
        shipType = 1
        while destroyerNumber != 0:
            x = randint(0, 9)
            y = randint(0, 9)
            pos = randint(1, 2)
            if self.checkValue(x, y, grid) == 0 and self.isolateArea(x, y, grid, shipType, pos) is True:
                if pos == 1:
                    i = 0
                    while i < 2:
                        self.placeShip(x + i, y, grid)
                        i += 1
                elif pos == 2:
                    i = 0
                    while i < 2:
                        self.placeShip(x, y + i, grid)
                        i += 1
                destroyerNumber -= 1
        return grid

    def placeCruiser(self, grid, cruiserNumber):
        shipType = 2
        while cruiserNumber != 0:
            x = randint(0, 9)
            y = randint(0, 9)
            pos = randint(1, 2)
            if self.checkValue(x, y, grid) == 0 and self.isolateArea(x, y, grid, shipType, pos) is True:
                if pos == 1:
                    i = 0
                    while i < 3:
                        self.placeShip(x + i, y, grid)
                        i += 1
                elif pos == 2:
                    i = 0
                    while i < 3:
                        self.placeShip(x, y + i, grid)
                        i += 1
                cruiserNumber -= 1
        return grid

    def placeBattleship(self, grid):
        shipType = 3
        x = randint(0, 9)
        y = randint(0, 9)
        pos = randint(1, 2)
        if self.checkValue(x, y, grid) == 0 and self.isolateArea(x, y, grid, shipType, pos) is True:
            if pos == 1:
                i = 0
                while i < 4:
                    self.placeShip(x + i, y, grid)
                    i += 1
            elif pos == 2:
                i = 0
                while i < 4:
                    self.placeShip(x, y + i, grid)
                    i += 1
        return grid

    def bombingCoord(self, grid):
        if self.controlIso(self.gridToLine(grid)) is True:
            return self.bombingCoordRandom()
        elif self.controlForSign(self.gridToLine(grid)) is 1 or 2:
            a = self.bombingCoordRandom()
            x = a[0]
            y = a[1]
            if self.checkValue(x, y, grid) is 1:
                return self.bombingCoord(grid)
            else:
                return x, y
        # else: #Leidub pommitatud koht
        #     bombed = findBombed(grid)
        #     x = bombed[0]
        #     y = bombed[1]
        #

    def findBombed(self, grid):
        x = 0
        y = 0
        for i in grid:
            for a in i:
                if a is 2:
                    return x, y
                x += 1
            y += 1

    def bombingCoordRandom(self):
        x = randint(0, 9)
        y = randint(0, 9)
        return x, y

    def gridToLine(self, grid):
        line = []
        for y in grid:
            for x in y:
                line.append(x)
        return line

    #-----------------------------------------------------------------------------------------------------
    #            These functions are called by the game:
    #-----------------------------------------------------------------------------------------------------

    # bombingResult = dict('status'=> ['hit', 'miss', 'sunk'], 'sunkShipInfo'=> [siia tuleb info ainult siis, kui status='sunk', aga sellele tuleb mõelda hiljem] )
    def setBombingResult(self, bombingResult):
        print('pommitmise tulemus:', bombingResult)

        #kui on plaanis hakata arvestama pommitamise tulemust uue pommitmaise korral, siis seda pead täiendama
        #
        #-küsin sinu funktsioonilt koordinaate pommitamiseks:
        #- sa annad vastuseks ('A',1)
        #- mina ütlen sulle, et 'hit' (said pihta)
        #(nüüd teen oma pommitamise, aga see pole tähtis hetkel)
        #- nüüd küsin sult uuesti koordinaate:
        #
        ...

    def giveCoordinatesToBomb(self):

        #return ('A',self.xxx.pop()) #vms
        return ('A',randint(1,10)) #vms

    def getEnemyShipPlacement(self):
        return {'positionsByShip': {}, 'shipsByLength': {2: [{'direction': 'H', 'startColChar': 'D', 'shipId': 'D5', 'startRowNr': 5}]}, 'ships': {'D5': {'shipPositions': {('D', 5), ('E', 5)}, 'shipId': 'D5', 'startRowNr': 5, 'direction': 'H', 'length': 2, 'startColChar': 'D'}}, 'shipsByPosition': {'E5': 'D5', 'D5': 'D5'}}
        pass

def numbersToLetters(self, coord):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    return letters[coord[0]], coord[1]

def coords(x, y):
    return x, y
