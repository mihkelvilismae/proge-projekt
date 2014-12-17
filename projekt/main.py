import kivy
#kivy.require('1.0.6') # replace with your current kivy version !
#from src.gameonfig import *

from src.game import Game
from src.gameconfiguration import MainConfig, GridConfig
from src.views import MainMenuView, GameScreenView
from src.behaviours import HoverBehavior
from src.screen import Screen

from kivy.app import App
from kivy.config import Config

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

if __name__ == '__main__':
    BattleshipApp().run()