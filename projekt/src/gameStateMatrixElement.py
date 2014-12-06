__author__ = 'mihkel'

class GameStateMatrixElement():
    STATE_EMPTY = 'empty'
    STATE_SHIPZONE = 'shipzone'

    gameState = None
    children = []
    countOfZones = 0

    def __init__(self, gameState):
        self.gameState = gameState

    def getCountOfZones(self):
        return len([x for x in self.children if x==self.STATE_SHIPZONE ])

    def setChildren(self, children):
        self.children = children

    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, child):
        self.children.remove(child)

    def setAsEmpty(self):
        self.setChildren([])

    def geSimplifiedElement(self):
        simplifiedElement = []
        for child in self.children():
            if child==self.STATE_EMPTY:
                simplifiedElement = '0'
            elif child==self.STATE_SHIPZONE:
                simplifiedElement = 'Z'
            else:
                simplifiedElement = 'X'
            simplifiedElement.append( child )

        return simplifiedElement



