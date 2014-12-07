import kivy
#kivy.require('1.0.6') # replace with your current kivy version !
from src.gameconfig import *

from src.game import Game
from src.gameconfig import MainConfig, GridConfig
from src.views import MainMenuView, GameScreenView
from src.behaviours import HoverBehavior
from src.screen import Screen

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
#       App Start
#---------------------------------------------------------------------------------------------------
class BattleshipApp(App):

    screen = None

    def build(self):
        global game #FIXME: THIS IS MOST CERTAINLY NOT THE WAY TO DO IT, BUT HOW ELSE ?!?!?
        game = Game()
        self.config = MainConfig()
        Config.set('graphics', 'width', self.config.windowWidth) #this has to be done before calling super()
        Config.set('graphics', 'height', self.config.windowHeight)
        self.screen = Screen(game=game)
        game.screen = self.screen
        return self.screen

    def on_start(self):
        3
        #print'start')


if __name__ == '__main__':
    BattleshipApp().run()
