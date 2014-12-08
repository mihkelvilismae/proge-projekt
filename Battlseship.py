__author__ = 'rainvagel'

playeGrid = [[0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0]]

computerGrid = [[0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0]]

computerPlanningGrid = [[0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0]] #Seda pole kelelgile näha, see lihtsalt arvutile, et ta saaks paremini planeerida
                                    #ning et programmeerijal oleks lihtsam

# 0 tähendab, et pole pommitatud
# 1 tähendab, et on pommitatud
# 2 tähendab, et seal on laev

ships = {"battleship": 1, "cruiser": 2, "destroyer": 3, "submarine": 4} #Mitu laeva saab mängijal olla
#Kui mängijate oma on tühi, siis mäng on läbi
playerShips = {}
computerShips = {}

pikkus = 0 # Laeva pikkus

def isEmpty(anyStructure):  #Vaatab, kas dictionary, list vms on tühi
    if anyStructure:
        return False
    else:
        return True

def gameOver(ships):  #Kui tagastab True, siis on mäng läbi
    if is_empty(ships) is True:
        return True
    else:
        return False

def checkValue(x, y, grid): #Vaatab, mis märge on nendel koordinaatidel
    if grid[x][y] == 0:
        return 0
    elif grid[x][y] == 1:
        return 1
    else:
        return 2

def checkShipHorizontalToRight(x, y, grid, pikkus):
    while checkValue(x, y, grid) == 2:
        checkShipHorizontalToRight(x, y + 1, grid, pikkus + 1)
    if pikkus == 4:
        #Siia funktsioon, mis eemaldab laevade nimekirjast battleship'i ja
        #compuerPlanningGrid'i märgib ära, et selle kõrvale ei saa pakkuda
        #ka funktsioon, mis vaatab, kas selle pikkusega laev on seal
    elif pikkus == 3:
        #Siia funktsioon, mis eemaldab laevade nimekirjast cruiser'i ja
        #computerPlanningGrid'il märgib ära, et selle kõrvale ei saa pakkuda
        #ka funktsioon, mis vaatab, kas selle pikkusega laev on seal
    elif pikkus == 2:
        #Siia funktsioon, mis eemaldab laevade nimekirjast destroyer'i ja
        #computerPlanningGrid'il märgib ära, et selle kõrvale ei saa pakkuda
        #ka funktsioon, mis vaatab, kas selle pikkusega laev on seal
    elif pikkus == 1:
        #Siia funktsioon, mis eemaldab laevade nimekirjast submarine'i ja
        #computerPlanningGrid'il märgib ära, et selle kõrvale ei saa pakkuda
        #Ka funktsioon, mis vaatab, kas selle pikkusega laev on seal
    else:
        return False #Näitab, et terve laev pole põhja lastud

def checkShipHorizontalToLeft(x, y, grid, pikkus):
    while checkValue(x, y, grid) == 2:
        checkShipHorizontalToLeft(x, y - 1, grid, pikkus + 1)
    if pikkus == 4:
        #Sama, mis eelmises
    elif pikkus == 3:
        #Sama, mis eelmises
    elif pikkus == 2:
        #Sama, mis eelmises
    elif pikkus == 1:
        #Sama, mis eelmises
    else:
        return False #Näitab, et terve laev pole põhja lastud

def checkShipVerticalUp(x, y, grid, pikkus):
    while checkValue(x, y, grid) == 2:
        checkShipVerticalUp(x + 1, y, grid, pikkus + 1)
    if pikkus == 4:
        #Sama, mis eelmises
    elif pikkus == 3:
        #Sama, mis eelmises
    elif pikkus == 2:
        #Sama, mis eelmises
    elif pikkus == 1:
        #Sama, mis eelmises
    else:
        return False
def checkShipVerticalDown(x, y, grid, pikkus):
    while checkValue(x, y, grid) == 2:
        checkShipVerticalDown(x - 1, y, grid, pikkus + 1)
    if pikkus == 4:
        #Sama, mis eelmises
    elif pikkus == 3:
        #Sama, mis eelmises
    elif pikkus == 2:
        #Sama, mis eelmises
    elif pikkus == 1:
        #Sama, mis eelmises
    else:
        return False

def makeShipLists(ships, gameShips):
    #Siia vaja funktsiooni, mis vaatab, mis laev on kusagil grid'il


def removeShipFromPlayer(ships, ship):
    if ships[ship] != 0:
        ships[ship] -= 1
        return ships
    #Funktsioon, mis eemaldab kasutaja olemasolevatest laevadest laeva

def changeGrid(x, y, gridComputer, gridPlayer): #Muudab mingis maatriksis mingit väärtust
    if checkValue(x, y, gridPlayer) == 0:
        gridComputer[x][y].replace(1)
        gridPlayer[x][y].replace(1)
    elif checkValue(x, y, gridPlayer) == 2: #Kui mängijal on seal laev
        gridComputer[x][y].replace(2)
    return gridPlayer, gridComputer

def bombPlayer(x, y, gridComputer, gridPlayer, gridComputerPlan):
    if checkValue(x, y, gridComputer) == 0: #Kas computerPlanningGrid'il on väärtus 0
        if checkValue(x, y, gridPlayer) == 2: #Kas playerGrid'il on väärtus 2
            changeGrid(x, y, gridComputer, gridPlayer)
            bombPlayer(x, y, gridComputer, gridPlayer, gridComputerPlan) #Arvuti saab kohe uuesti proovida
        elif checkValue(x, y, gridPlayer) == 0:
            return changeGrid(x, y, gridComputer, gridPlayer)
    elif checkValue(x, y, gridComputerPlan) == 2: #Siit kuni else'ini on vaja luuamingisugune funktsioon, mis vaatab, kuhu lasta
        if checkValue(x + 1, y, gridComputerPlan) == 0: #Vaatab, kas ülal on pommitamata koht
            bombPlayer(x + 1, y, gridComputer, gridPlayer, gridComputerPlan)
        elif checkValue(x - 1, y, gridComputerPlan) == 0: #vaatab, kas all on pommitamata koht
            bombPlayer(x - 1, y, gridComputer, gridPlayer, gridComputerPlan)
        elif checkValue(x, y + 1, gridPlayer) == 0: #Vaatab, kas paremal on pommitamat koht
            bombPlayer(x, y + 1, gridComputer, gridPlayer, gridComputerPlan)
        elif checkValue(x, y -1 , gridPlayer) == 0: #Vaatab, kas vasakul on pommitamata koht
            bombPlayer(x, y - 1, gridComputer, gridPlayer, gridComputerPlan)
    else:
        bombPlayer(x, y, gridComputer, gridPlayer, gridComputerPlan)

def bombingCoord(x, y, gridComputerPlan, gridPlayer): #vaatab, kuhu lasta pommi
    ...
    return x, y
