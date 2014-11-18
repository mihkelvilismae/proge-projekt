#import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.graphics import Rectangle

class Screen( Widget ):

    MainMenuView = None

    def __init__(self, **kwargs):
        Config.set('graphics', 'width', '600') #this has to be done before calling super()
        Config.set('graphics', 'height', '600')
        super().__init__(**kwargs)
        self.drawMainMenuView()

    def drawMainMenuView(self):
        self.clear_widgets()
        self.MainMenuView = MainMenuView()
        self.add_widget( self.MainMenuView )
        self.MainMenuView.draw()

    def drawGameScreenView(self):
        self.clear_widgets()
        gameScreenView = GameScreenView()
        self.add_widget( gameScreenView )
        gameScreenView.draw()

class MainMenuView( Widget ):

    def draw(self):
        self.addStartLabel()

    def addStartLabel(self):
        randomlabel = Label(text='[ref=startGame]START[/ref]', markup=True)
        self.add_widget( randomlabel )
        def drawGameScreenView( object, value ):
            self.parent.drawGameScreenView()
        randomlabel.bind(on_ref_press=drawGameScreenView)

class GameScreenView( Widget ):

    def draw(self):
        self.drawGrid()

        randomlabel = Label(text='GameScreenView')
        self.add_widget( randomlabel )

    def drawGrid(self):
        self.canvas.add(Rectangle(pos=(100, 100), size=(30, 30)))

    #def createGrid(self):

class BattleshipApp(App):

    screen = None

    def build(self):
        self.screen = Screen()
        return self.screen

    def on_start(self):
        print('start')


if __name__ == '__main__':
    BattleshipApp().run()
