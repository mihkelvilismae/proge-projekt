__author__ = 'mihkel'

from .shipport import ShipPort
from .grid import Grid
from .gameState import GameState

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
        self.game.activeArea = self.game.battleArea
        self.addWidgetToGameScreenView( self.game.battleArea )
        self.game.battleArea.draw(1)

    def drawOwnShipGridArea(self):
        self.game.ownShipGridArea = BattleArea()
        self.addWidgetToGameScreenView( self.game.ownShipGridArea )
        self.game.ownShipGridArea.draw(2)

    def drawEnemyShipGridArea(self):
        self.game.enemyShipGridArea = BattleArea()
        self.addWidgetToGameScreenView( self.game.enemyShipGridArea )
        self.game.enemyShipGridArea.draw(1)

    def drawShipPort(self):
        self.game.shipPort = ShipPort(game=self.game)
        self.addWidgetToGameScreenView( self.game.shipPort )
        self.game.shipPort.draw()

    def drawStartingButton(self):
        self.startingButton = Button(text='ALUSTA MÄNGU!')
        self.startingButton.bind(on_press=self.game.startBattle)
        self.addWidgetToGameScreenView( self.startingButton )

    #def

    def removeShipPort(self):
        self.remove_widget( self.game.shipPort )

#---------------------------------------------------------------------------------------------------
#       BattleArea
#---------------------------------------------------------------------------------------------------
class BattleArea( RelativeLayout ):
    grid = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw(self, sizeMultiplier):
        self.drawGrid( sizeMultiplier )

    def drawGrid(self, sizeMultiplier):
        self.grid = Grid(sizeMultiplier=sizeMultiplier)
        #self.parent.mainGrid = self.mainGrid
        self.add_widget( self.grid )
        self.grid.draw()
