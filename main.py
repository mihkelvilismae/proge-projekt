#import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.graphics import Rectangle
from kivy.core.text import Label as CoreLabel

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

    grid = None
    def draw(self):
        self.drawGrid()

    def drawGrid(self):
        self.grid = Grid()
        self.add_widget( self.grid )

class Grid( Widget ):
    gridRectSize = 50
    sizeMultiplier = None
    gridElements = None

    def __init__(self, startX=0, startY=0, sizeMultiplier=1 ):
        super().__init__()
        self.sizeMultiplier = sizeMultiplier
        self.addGridElements()
        def doCalculation(x,u):
            print('click')
        self.bind( on_press=doCalculation)

    def addGridElements(self):  #FIXME - REDO USING LAYOUT
        self.gridElements = dict()
        rectStartX = 0
        rectStartY = 11*(self.gridRectSize+1)
        for rowNumber in range(0,11):
            self.gridElements[ rowNumber ] = dict()
            for colNr, colCharacter in enumerate(list(' ABCDEFGHIJ')):
                if rowNumber == 0 or colNr==0:
                    my_label = CoreLabel() #http://kivy.org/docs/api-kivy.core.text.html?highlight=text#
                    if rowNumber==0:
                        my_label.text = colCharacter
                    else:
                        my_label.text = str(rowNumber)
                    my_label.text_size = (25,25)
                    my_label.refresh()
                    hello_texture = my_label.texture
                    rectangle = Rectangle(texture=hello_texture, pos=[rectStartX, rectStartY], size=[self.gridRectSize, self.gridRectSize])
                    self.canvas.add( rectangle )
                else:
                    rectangle = Rectangle(pos=[rectStartX, rectStartY], size=[self.gridRectSize, self.gridRectSize])
                    self.gridElements[ rowNumber ][ colCharacter ] = rectangle
                    self.canvas.add( rectangle )
                rectStartX += self.gridRectSize + 1
                if colNr==0:
                    print(rowNumber, colCharacter)
                    print(rectangle.pos)
                    print('----')
            rectStartX = 0
            rectStartY -= self.gridRectSize + 1

    #def addGridElement(self, row):

class BattleshipApp(App):

    screen = None

    def build(self):
        self.screen = Screen()
        return self.screen

    def on_start(self):
        print('start')


if __name__ == '__main__':
    BattleshipApp().run()
