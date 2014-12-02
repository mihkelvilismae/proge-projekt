__author__ = 'mihkel'

from .behaviours import HoverBehavior
from .gameconfig import GridConfig

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
class Grid( GridLayout ):
    sizeMultiplier = 1
    gridElements = dict()
    gridConfig = None

    def __init__(self, sizeMultiplier=1 ):
        self.sizeMultiplier = sizeMultiplier
        self.gridConfig = GridConfig(sizeMultiplier=self.sizeMultiplier)
        super().__init__(col_default_width=self.gridConfig.gridElementSize[0], col_force_default=True, cols=11)
        #game.mainGrid = self

    def addTestingButton(self):
        button = Button(text='XXX',size=(100,50),size_hint=(None,None), pos_hint= { 'center_x' : 0.5 })
        def testing(obj):
            game.testing()
        button.bind( on_press=testing)
        self.add_widget(button)

    def addGridElements(self):

        self.gridElements = dict()
        self.get_root_window().children[0].gridElements = self.gridElements
        for rowNr in range(0,11):
            self.gridElements[ rowNr ] = dict()
            for colNr, colCharacter in enumerate(list(' ABCDEFGHIJ')):
                if rowNr==0 and colNr==0:
                    self.addTestingButton()
                    continue

                if 1 and (rowNr==0 or colNr==0):
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


#---------------------------------------------------------------------------------------------------
#       Grid Elements
#---------------------------------------------------------------------------------------------------
#class GridElement( RelativeLayout):
class GridElement( RelativeLayout, HoverBehavior ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__(size_hint = (None,None), size=gridConfig.gridElementSize, **kwargs)

class GridBattlefieldElement( GridElement ):
    game = None
    rowCoordinate = None
    columnCoordinate = None

    def __init__(self, gridConfig, rowCoordinate, columnCoordinate, **kwargs):
        self.rowCoordinate = rowCoordinate
        self.columnCoordinate = columnCoordinate
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
        tooltipRectangleColor = Color(1, 0, 0, .5, mode='rgba')
        self.canvas.add( tooltipRectangleColor )
        tooltipRectangle = Rectangle(size=gridConfig.battlefieldRectangleSize, pos=[5,5])
        self.canvas.add( tooltipRectangle )

        tooltipRectangleColor = Color(1,1,1)  #fixme: unless I do this, it doesnt display the pointerRectangle correctly. why??
        self.canvas.add( tooltipRectangleColor  )