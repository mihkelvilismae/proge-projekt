__author__ = 'mihkel'

from .behaviours import HoverBehavior
from .gameconfiguration import GridConfig
from .gameState import GameState
from .parentFinder import ParentFinder
from .battleStatus import BattleStatus

import collections
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout

#---------------------------------------------------------------------------------------------------
#       @Grid
#---------------------------------------------------------------------------------------------------
class Grid( GridLayout, ParentFinder):
    game = None
    sizeMultiplier = 1
    gridElements = dict()
    gridConfig = None
    gameState = None
    colWidth = 0
    rowHeight = 0

    isBombardmentAllowed = False
    isPlacementAllowed = False

    def __init__(self, sizeMultiplier=1 ):
        self.gameState=GameState( self )
        self.sizeMultiplier = sizeMultiplier
        self.gridConfig = GridConfig(sizeMultiplier=self.sizeMultiplier)
        super().__init__(col_default_width=self.gridConfig.gridElementSize[0], col_force_default=True, row_default_height=self.gridConfig.gridElementSize[1], row_force_default=True, cols=11)
        self.colWidth = self.gridConfig.gridElementSize[0]
        self.rowHeight = self.gridConfig.gridElementSize[1]

    def draw(self):
        self.addGridElements()
        self.gameState.createGameStateMatrix()

    def isElementInGridBounds(self, elementToCheck):

        elementToCheckX = elementToCheck.to_window(elementToCheck.x, elementToCheck.y)[0]
        elementToCheckY = elementToCheck.to_window(elementToCheck.x, elementToCheck.y)[1]

        gridLeftX = self.getGridTopLeft()[0]
        gridTopY = self.getGridTopLeft()[1]
        gridRightX = self.getGridBottomRight()[0]
        gridBottomY =  self.getGridBottomRight()[1]

        # the "elementToCheckY > gridTopY-10" check is just a hacky way of solving the problem of upper-out-of-bounds shipZones not displaying correctly
        if elementToCheckY < gridBottomY or elementToCheckY > gridTopY-10 or elementToCheckX < gridLeftX or gridRightX < elementToCheckX:
            return False
        else:
            return True

    def getGridTopLeft(self):
        return self.getGridElementOnPosition('A',1).to_window(self.getGridElementOnPosition('A',1).x, self.getGridElementOnPosition('A',1).top)

    def getGridBottomRight(self):
        return self.getGridElementOnPosition('J',10).to_window(self.getGridElementOnPosition('J',10).right, self.getGridElementOnPosition('J',10).y)

    def addTestingButton(self):
        button = Button(text='XXX',size=(100,50),size_hint=(None,None), pos_hint= { 'center_x' : 0.5 })
        self.game = self.get_root_window().children[0].game
        def testing(obj):
            self.game.testing()
        button.bind( on_press=testing)
        self.add_widget(button)

    def addGridElements(self):
        self.gridElements = collections.OrderedDict()
        for rowNr in self.getGame().mainConfig.rowNumbers:
            self.gridElements[ rowNr ] = collections.OrderedDict()
            for colNr, colCharacter in enumerate(self.getGame().mainConfig.columnChars):
                if rowNr==0 and colNr==0:
                    #self.addTestingButton()
                    self.add_widget(Widget())
                    continue

                if rowNr==0 or colNr==0:
                    if rowNr==0:
                        gridLabelElementText = colCharacter
                    elif colNr==0:
                        gridLabelElementText = rowNr
                    gridElement = GridLabelElement(text=gridLabelElementText, gridConfig = self.gridConfig) #pos=self.calculcateGridElementPosition(rowNr,colNr)
                else:
                    gridElement = GridBattlefieldElement( self.gridConfig, rowNr, colCharacter) #, pos=self.calculcateGridElementPosition(rowNr,colNr
                    self.gridElements[rowNr][colCharacter] = gridElement
                self.add_widget( gridElement )
                gridElement.draw()

    def calculcateGridElementPosition(self, rowNr, colNr):
        position = (self.gridConfig.battlefieldRectangleSize[0] * rowNr, self.gridConfig.battlefieldRectangleSize[1] * colNr)
        return position

    def getGridElementOnPosition(self, colChar, rowNr):
        return self.gridElements[ rowNr ][ colChar ]

#---------------------------------------------------------------------------------------------------
#       Grid Elements
#---------------------------------------------------------------------------------------------------
class GridElement( RelativeLayout, HoverBehavior, ParentFinder ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__(size_hint = (None,None), size=gridConfig.gridElementSize, **kwargs)

    def getGrid(self):
        return self.getParentByClass(Grid)

    def getGameState(self):
        return self.getParentByClass(Grid).gameState

class GridBattlefieldElement( GridElement ):
    game = None
    rowNr = None
    colChar = None
    isBombed = False
    isLocked = False

    def __init__(self, gridConfig, rowNr, colChar, **kwargs):
        self.tooltipRectangle = None
        self.rowNr = rowNr
        self.colChar = colChar
        self.gridConfig = gridConfig
        super().__init__(gridConfig=gridConfig, **kwargs)

    def draw(self):
    #this is the coloured area inside the element (that makes it look as a grid):
        elementRectangle = Rectangle( pos_hint=(None,None), size=self.gridConfig.battlefieldRectangleSize, pos=self.calculateElementRectanglePosition() )
        self.canvas.add( elementRectangle )
        self.game = self.get_root_window().children[0].game

    def removePointerRectangle(self):
        if self.tooltipRectangle in self.children:
            self.remove_widget( self.tooltipRectangle )

    def addPointerRectangle(self):
        if self.getGame():
            canShipBePlaced = self.getGame().selectedShip!=None and self.getGame().canShipBePlaced(self.getGame().selectedShip, self)
            canBombard = self.getGame().canGridElementBeBombarded(self)
            if  canShipBePlaced or canBombard:
                tooltipRectangleColor = Color(0, 1, 0, .5)
            else:
                tooltipRectangleColor = Color(1, 0, 0, .5)
            self.tooltipRectangle = PointerRectangle( self.gridConfig, tooltipRectangleColor )
            self.add_widget( self.tooltipRectangle )

    def calculateElementRectanglePosition(self):
        return (5, 5)

    def bombard(self, bombardmentResult):
        self.isBombed = True
        self.canvas.clear()
        if bombardmentResult==BattleStatus.BOMBARD_RESULT_HIT:
            hitRectangleSize = (self.gridConfig.battlefieldRectangleSize[0]/2, self.gridConfig.battlefieldRectangleSize[1]/2)
            elementRectangle = Rectangle( size_hint=(None,None), size=hitRectangleSize, pos=self.calculateElementRectanglePosition() )
            self.canvas.add( Color(1,0,0) )
            self.canvas.add( elementRectangle )
        elif bombardmentResult==BattleStatus.BOMBARD_RESULT_MISS:
            elementRectangle = Rectangle( size_hint=(None,None), size=self.gridConfig.battlefieldRectangleSize, pos=self.calculateElementRectanglePosition() )
            self.canvas.add( Color(0.7, 0.7, 0.7, 0.5), )
            self.canvas.add( elementRectangle )
        elif bombardmentResult==BattleStatus.BOMBARD_RESULT_ENEMY_BOMBED_MY_GRID: #this shouldnt be here
            self.add_widget( Label(text='X', font_size='30sp',pos=(4,0)))
        self.canvas.add( Color(1,1,1) ) #i dont know why this is necessary

# EVENT BINDINGS (start):
    def on_touch_down(self, touch): #this fires on the event that someone clicks on the grid
        #print'GridBattlefieldElement - click')
        if self.collide_point(*touch.pos):
            if self.game.canShipBePlaced(self.game.selectedShip, self): #todo should i check in game and then do placement in ship ?
                self.game.placeShipToGrid(self.game.selectedShip, self)
            elif self.game.canGridElementBeBombarded( self ):
                self.game.bombardGrid(self)
            return True

    def on_enter(self):
        self.addPointerRectangle()

    def on_leave(self):
        self.removePointerRectangle()
# EVENT BINDINGS (end):

class GridLabelElement( GridElement ):
    def __init__(self, gridConfig, text='', **kwargs):
        self.text = str(text)
        super().__init__(gridConfig=gridConfig, **kwargs)

    def draw(self):
        elementText = Label(text=self.text)
        self.add_widget( elementText )

#------------------------------------------------------------------------------------------------------------
#   POINTERS
#------------------------------------------------------------------------------------------------------------
class PointerRectangle( Widget ):
    def __init__(self, gridConfig, color, **kwargs):
        super().__init__( **kwargs)
        tooltipRectangleColor = color
        self.canvas.add( tooltipRectangleColor )
        tooltipRectangle = Rectangle(size=gridConfig.battlefieldRectangleSize, pos=[5,5])
        self.canvas.add( tooltipRectangle )

        tooltipRectangleColor = Color(1,1,1)  #fixme: unless I do this, it doesnt display the pointerRectangle correctly. why??
        self.canvas.add( tooltipRectangleColor  )