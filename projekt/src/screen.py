__author__ = 'mihkel'
from kivy.uix.widget import Widget
from src.gameconfig import MainConfig, GridConfig
from src.views import MainMenuView, GameScreenView
#---------------------------------------------------------------------------------------------------
#       Page Initializations
#---------------------------------------------------------------------------------------------------
class Screen( Widget ):

    game = None
    config = None
    MainMenuView = None

    def __init__(self, game=game, **kwargs):
        self.game = game
        self.config = MainConfig()
        super().__init__(**kwargs)
        self.drawMainMenuView()

    def drawMainMenuView(self):
        self.clear_widgets()
        self.MainMenuView = MainMenuView()
        self.add_widget( self.MainMenuView )
        self.MainMenuView.draw()

    def drawGameScreenView(self):
        self.clear_widgets()
        self.gameScreenView = GameScreenView()
        self.add_widget( self.gameScreenView )
        self.gameScreenView.draw()
