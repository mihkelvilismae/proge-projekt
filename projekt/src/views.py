__author__ = 'mihkel'

from .shipport import ShipPort
from .grid import Grid

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
#       MainMenuView
#---------------------------------------------------------------------------------------------------
class MainMenuView( Widget ):
    game = None
    def __init__(self, **kwargs):
        print('xxx')
        super().__init__(**kwargs)

    def draw(self):
        self.addStartButtonLabel()
        self.game = self.parent.game

    def addStartButtonLabel(self):
        randomlabel = Label(text='[ref=startGame]START[/ref]', markup=True)
        self.add_widget( randomlabel )
        def drawGameScreenView( object, value ):
            self.game.startGame()
        randomlabel.bind(on_ref_press=drawGameScreenView)

#---------------------------------------------------------------------------------------------------
#       GameScreenView
#---------------------------------------------------------------------------------------------------
class GameScreenView( BoxLayout ):
    game = None
    #shipPort = None
    #smallerGrid = None
    #mainGrid = None
    startingButton = None

    def __init__(self, **kwargs):
        super().__init__(cols=2,**kwargs)
        #self.size_hint = (1,1)
        #self.size = (900,600)

    def draw(self):
        self.game = self.parent.game
        #self.game = self.get_root_window().children[0]
        self.size = self.parent.size
        self.drawBattleArea()
        self.drawShipPort()

    def addWidgetToGameScreenView(self, widgetToAdd):
        self.add_widget( widgetToAdd )

    def drawBattleArea(self):
        self.game.battleArea = BattleArea()
        self.addWidgetToGameScreenView( self.game.battleArea )
        self.game.battleArea.draw()

    def drawShipPort(self):
        self.game.shipPort = ShipPort(game=self.game)
        self.addWidgetToGameScreenView( self.game.shipPort )
        self.game.shipPort.draw()

    def drawStartingButton(self):
        self.startingButton = Button(text='ALUSTA MÄNGU!')
        self.startingButton.bind(on_press=self.game.startBattle)
        self.addWidgetToGameScreenView( self.startingButton )

    def removeShipPort(self):
        self.remove_widget( self.game.shipPort )

#---------------------------------------------------------------------------------------------------
#       BattleArea
#---------------------------------------------------------------------------------------------------
class BattleArea( RelativeLayout ):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw(self):
        self.drawMainGrid()

    def drawSmallerGrid(self): #todo: can be joined with drawMainGrid()?
        self.smallerGrid = Grid(sizeMultiplier=2)
        self.add_widget( self.smallerGrid )
        self.smallerGrid.addGridElements()

    def drawMainGrid(self):
        self.mainGrid = Grid(sizeMultiplier=1)
        self.parent.mainGrid = self.mainGrid
        print(self.parent)
        self.add_widget( self.mainGrid )
        self.mainGrid.addGridElements()
