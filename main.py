#import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config

class Screen( Widget ):

    MainMenuView = None

    def __init__(self, **kwargs):
        Config.set('graphics', 'width', '600') #this has to be done before calling super()
        Config.set('graphics', 'height', '600')
        super().__init__(**kwargs)
        self.drawMainMenuView()

    def drawMainMenuView(self):
        self.MainMenuView = MainMenuView()
        self.add_widget( self.MainMenuView )
        self.MainMenuView.draw()

    def drawGameScreenView(self):
        gameScreenView = GameScreenView()
        self.add_widget( gameScreenView )
        gameScreenView.draw()

class MainMenuView( Widget ):

    def draw(self):
        self.clear_widgets()
        randomlabel = Label(text='[ref=startGame]START[/ref]', markup=True)
        self.add_widget( randomlabel )
        def drawGameScreenView( object, value ):
            self.parent.drawGameScreenView()
        randomlabel.bind(on_ref_press=drawGameScreenView)

class GameScreenView( Widget ):

    def draw(self):
        self.clear_widgets()
        randomlabel = Label(text='GameScreenView')
        self.add_widget( randomlabel )

class BattleshipApp(App):

    game = None

    def build(self):
        self.game = Screen()
        return self.game

    def on_start(self):
        #self
        print('zzzz')


if __name__ == '__main__':
    BattleshipApp().run()
