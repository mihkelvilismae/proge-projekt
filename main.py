import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

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

#---------------------------------------------------------------------------------------------------
#       MainMenuView
#---------------------------------------------------------------------------------------------------
class GridConfig():
    def __init__(self, sizeMultiplier=1, **kwargs):
        if sizeMultiplier==1:
            self.gridSize = (800,800)
            self.gridElementSize = (50,50)
            self.battlefieldRectangleSize = (20,20)
        else:
            self.gridSize = (400,400)
            self.gridElementSize = (25,25)
            self.battlefieldRectangleSize = (40,40)

class MainMenuView( Widget ):

    def draw(self):
        self.addStartButtonLabel()

    def addStartButtonLabel(self):
        randomlabel = Label(text='[ref=startGame]START[/ref]', markup=True)
        self.add_widget( randomlabel )
        def drawGameScreenView( object, value ):
            self.parent.drawGameScreenView()
        randomlabel.bind(on_ref_press=drawGameScreenView)

#---------------------------------------------------------------------------------------------------
#       GameScreenView
#---------------------------------------------------------------------------------------------------
class GameScreenView( BoxLayout ):
    smallerGrid = None
    mainGrid = None

    def __init__(self, **kwargs):
        super().__init__(cols=2,size=(1200,600),**kwargs)

    def draw(self):
        self.drawMainGrid()
        #self.drawSmallerGrid()

    def drawSmallerGrid(self): #todo: can be joined with drawMainGrid()?
        self.smallerGrid = Grid(sizeMultiplier=2)
        self.smallerGrid.addGridElements()
        self.add_widget( self.smallerGrid )

    def drawMainGrid(self):
        self.mainGrid = Grid(sizeMultiplier=1)
        self.mainGrid.addGridElements()
        self.add_widget( self.mainGrid )

#---------------------------------------------------------------------------------------------------
#       GRID
#---------------------------------------------------------------------------------------------------
class Grid( GridLayout ):
    sizeMultiplier = 1
    gridElements = dict()
    gridConfig = None

    def __init__(self, sizeMultiplier=1 ):
        self.sizeMultiplier = sizeMultiplier #TODO implement this
        self.gridConfig = GridConfig(sizeMultiplier=self.sizeMultiplier)
        super().__init__(cols=11, size_hint=(None,None), size = self.gridConfig.gridSize)

    def addGridElements(self):
        self.gridElements = dict()
        for rowNr in range(0,11):
            self.gridElements[ rowNr ] = dict()
            for colNr, colCharacter in enumerate(list(' ABCDEFGHIJ')):
                if 1 and (rowNr==0 or colNr==0):
                    if rowNr==0:
                        gridLabelElementText = colCharacter
                    elif colNr==0:
                        gridLabelElementText = rowNr
                    gridElement = GridLabelElement(text=gridLabelElementText, gridConfig = self.gridConfig)
                else:
                    gridElement = GridBattlefieldElement(gridConfig = self.gridConfig)
                self.add_widget( gridElement )

#---------------------------------------------------------------------------------------------------
#       GRID ELEMENTS
#---------------------------------------------------------------------------------------------------
class GridElement( RelativeLayout ):
    def __init__(self, text='', size_hint = (None,None), size=(600,600), **kwargs): #xxxxxxxxxxxxxxxxx
        super().__init__(**kwargs)
        print(self.size)

class GridBattlefieldElement( GridElement ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__(size_hint = (None,None), size=(600,600), **kwargs)
        elementRectangle = Rectangle( pos=[5,5] )
        self.canvas.add( elementRectangle )

class GridLabelElement( GridElement ):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        print(self.height)
        print(self.width)
        elementText = Label(text=str(text))
        self.add_widget( elementText )

#---------------------------------------------------------------------------------------------------
#       PAGE INITALIZATIONS
#---------------------------------------------------------------------------------------------------
class Screen( Widget ):

    MainMenuView = None

    def __init__(self, **kwargs):
        Config.set('graphics', 'width', '1600') #this has to be done before calling super()
        Config.set('graphics', 'height', '700') #todo  somekind of config?
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

#---------------------------------------------------------------------------------------------------
#       APP START
#---------------------------------------------------------------------------------------------------
class BattleshipApp(App):

    screen = None

    def build(self):
        self.screen = Screen()
        return self.screen

    def on_start(self):
        print('start')


if __name__ == '__main__':
    BattleshipApp().run()
