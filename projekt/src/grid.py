__author__ = 'mihkel'

from .behaviours import HoverBehavior
from .gameconfig import GridConfig
from .gameState import GameState
from .parentFinder import ParentFinder

import collections
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.graphics import *
from kivy.graphics import Color, Ellipse, Line
from kivy.core.text import Label as CoreLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
import random

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

    def __init__(self, sizeMultiplier=1 ):
        self.gameState=GameState( self )
        self.sizeMultiplier = sizeMultiplier
        self.gridConfig = GridConfig(sizeMultiplier=self.sizeMultiplier)
        super().__init__(col_default_width=self.gridConfig.gridElementSize[0], col_force_default=True, row_default_height=self.gridConfig.gridElementSize[1], row_force_default=True, cols=11)
        self.colWidth = self.gridConfig.gridElementSize[0]
        self.rowHeight = self.gridConfig.gridElementSize[1]
        #game.mainGrid = self

    def draw(self):
        self.getGame().testingMainGrid = self
        self.addGridElements()
        self.gameState.createGameStateMatrix()

    #def isShipInGridBounds(self, ship):

    def isElementInGridBounds(self, elementToCheck): #fixme: this has hardcoded stuff (most likely wont work with the smaller grid version), because i couldnt get the proper position for the grid
        elementToCheckX = elementToCheck.to_window(elementToCheck.x, elementToCheck.y)[0]
        elementToCheckY = elementToCheck.to_window(elementToCheck.x, elementToCheck.y)[1]
        gridBottomY = self.to_widget(self.x, self.y)[1]+100
        gridTopY = 11*self.rowHeight

        if elementToCheckY < gridBottomY or elementToCheckY>gridTopY or elementToCheckX < self.x+50 or 11*self.colWidth < elementToCheckX:
            return False
        else:
            return True

    def addTestingButton(self):
        button = Button(text='XXX',size=(100,50),size_hint=(None,None), pos_hint= { 'center_x' : 0.5 })
        self.game = self.get_root_window().children[0].game
        def testing(obj):
            self.game.testing()
        button.bind( on_press=testing)
        self.add_widget(button)

    def addGridElements(self):
        self.gridElements = collections.OrderedDict()
        self.get_root_window().children[0].gridElements = self.gridElements
        for rowNr in self.getGame().mainConfig.rowNumbers:
            self.gridElements[ rowNr ] = collections.OrderedDict()
            for colNr, colCharacter in enumerate(self.getGame().mainConfig.columnChars):
                if rowNr==0 and colNr==0:
                    self.addTestingButton()
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

    def __init__(self, gridConfig, rowNr, colChar, **kwargs):
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
        self.remove_widget( self.tooltipRectangle )

    def addPointerRectangle(self):
        ##print'addponter')
        self.tooltipRectangle = PointerRectangle( self.gridConfig )
        self.add_widget( self.tooltipRectangle )

    def calculateElementRectanglePosition(self):
        return (self.pos[0]+5, self.pos[1]+5)

    def bombard(self):
        #elementRectangle = Rectangle( pos_hint=(None,None), size=self.gridConfig.battlefieldRectangleSize, pos=self.calculateElementRectanglePosition() )
        #line = Line(points=[0,50], width=10)
        #self.canvas.add(Color(50,50,50))
        #self.canvas.add( line )
        self.isBombed = True
        self.canvas.clear()


# EVENT BINDINGS (start):
    def on_touch_down(self, touch): #this fires on the event that someone clicks on the grid
        #print'GridBattlefieldElement - click')
        if self.collide_point(*touch.pos):
            if self.game.canShipBePlaced(self.game.selectedShip, self): #todo should i check in game and then do placement in ship ?
                self.game.placeShipToGrid(self.game.selectedShip, self)
            elif self.game.canGridBeBombarded( self ):
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
        #self.bind(on_motion=on_motion)

        #def on_motion(self, etype, motionevent):
        #    2
    def draw(self):
        elementText = Label(text=self.text)
        self.add_widget( elementText )

#------------------------------------------------------------------------------------------------------------
#   POINTERS
#------------------------------------------------------------------------------------------------------------
class PointerRectangle( Widget ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__( **kwargs)
        #tooltipRectangleColor = Color(1, 0, 0, .5, mode='rgba')
        tooltipRectangleColor = Color(1, 0, 0, .5)
        self.canvas.add( tooltipRectangleColor )
        tooltipRectangle = Rectangle(size=gridConfig.battlefieldRectangleSize, pos=[5,5])
        self.canvas.add( tooltipRectangle )

        tooltipRectangleColor = Color(1,1,1)  #fixme: unless I do this, it doesnt display the pointerRectangle correctly. why??
        self.canvas.add( tooltipRectangleColor  )