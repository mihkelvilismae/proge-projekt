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
from kivy.properties import StringProperty, ObjectProperty



#---------------------------------------------------------------------------------------------------
#       Config
#---------------------------------------------------------------------------------------------------
class MainConfig():
    def __init__(self, sizeMultiplier=1, **kwargs):
        self.gridConfig = GridConfig()
    # application window size:
        self.windowWidth = 1600
        self.windowHeight = 800
        self.windowSize = (self.windowWidth, self.windowHeight)
    #ship size
        self.shipBlockHeight = self.gridConfig.gridElementSize[0]+5
        self.shipBlockWidth = self.gridConfig.gridElementSize[0]+5

class GridConfig():
    def __init__(self, sizeMultiplier=1, **kwargs):
        if sizeMultiplier==1:
            self.gridHeight = 600
            self.gridWidth = 600
        else:
            self.gridHeight = 400
            self.gridWidth = 400
        self.gridElementSize = (self.gridWidth/11, self.gridHeight/11)
        self.battlefieldRectangleSize = (self.gridWidth/11-5, self.gridHeight/11-5)

#---------------------------------------------------------------------------------------------------
#       SessionStatus
#---------------------------------------------------------------------------------------------------
sessionStatus = None #FIXME: SEE BELOW IN MAIN APP
class SessionStatus( Widget ):
    selectedShip = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.bind(selectedShip=self.onSelectedShipChange)

    def onSelectedShipChange(self, instance, newValue):
        print('seelectedwdaw')

    def canShipBePlaced(self):
        1
#---------------------------------------------------------------------------------------------------
#       MainMenuView
#---------------------------------------------------------------------------------------------------
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
    shipPlacementLocation = None
    smallerGrid = None
    mainGrid = None

    def __init__(self, **kwargs):
        super().__init__(cols=2,**kwargs)

    def draw(self):
        self.drawMainGrid()
        #self.drawSmallerGrid()
        self.drawShipPlacementLocation()

    def drawShipPlacementLocation(self):
        self.shipPlacementLocation = ShipPlacementLocation()
        self.add_widget( self.shipPlacementLocation )

    def drawSmallerGrid(self): #todo: can be joined with drawMainGrid()?
        self.smallerGrid = Grid(sizeMultiplier=2)
        self.smallerGrid.addGridElements()
        self.add_widget( self.smallerGrid )

    def drawMainGrid(self):
        self.mainGrid = Grid(sizeMultiplier=1)
        self.mainGrid.addGridElements()
        self.add_widget( self.mainGrid )

#---------------------------------------------------------------------------------------------------
#       Ship
#---------------------------------------------------------------------------------------------------
class Ship( Widget ):
    STATUS_WAITING_TO_BE_PICKED_UP = 'waitingToBePickedUp'
    STATUS_PLACED = 'placed'
    STATUS_SELECTED = 'selected'

    shipStatus = StringProperty( STATUS_WAITING_TO_BE_PICKED_UP ) # baseerub nupp.py näitel
    length = 1
    color = Color(1,1,0)
    position = [0,100]

    def __init__(self, length=1, **kwargs):
        self.mainConfig = MainConfig()
        super().__init__(size_hint=(None,None), pos=self.position, size=self.calculateShipSize(length), **kwargs)
        self.length = length
        self.drawShip()
        self.bind(shipStatus=self.on_status)

# EVENT BINDINGS (start):
    def on_status(self, instance, pos): #this fires when the status changes
        if self.shipStatus==self.STATUS_SELECTED:
            self.color = Color(1,0,1)
            self.pos = (150,222)
            sessionStatus.selectedShip = self
        elif self.shipStatus==self.STATUS_WAITING_TO_BE_PICKED_UP:
            self.color = Color(1,1,0)

        self.drawShip()

    def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
        if self.collide_point(*touch.pos):
            self.shipStatus = self.STATUS_SELECTED
            return True
# EVENT BINDINGS (end)

    def drawShip(self):
        self.canvas.clear()
        elementRectangle = Rectangle(pos=self.pos, size=self.size)
        self.canvas.add( self.color )
        self.canvas.add( elementRectangle )

    def calculateShipSize(self, shipLength):
        return (self.mainConfig.shipBlockWidth * shipLength, self.mainConfig.shipBlockHeight)


#---------------------------------------------------------------------------------------------------
#       Ship placement location
#---------------------------------------------------------------------------------------------------
class ShipPlacementLocation( RelativeLayout ): #todo: this should also show status of bombed ships
    def __init__(self, **kwargs):
        super().__init__(cols=2,**kwargs)
        self.add_widget( Ship(2) )
        #self.add_widget( Ship() )

class ShipCount( Widget ):
    def __init__(self, **kwargs):
        super().__init__(cols=2,**kwargs)
#---------------------------------------------------------------------------------------------------
#       Grid
#---------------------------------------------------------------------------------------------------
class Grid( GridLayout ):
    sizeMultiplier = 1
    gridElements = dict()
    gridConfig = None

    def __init__(self, sizeMultiplier=1 ):
        self.sizeMultiplier = sizeMultiplier
        self.gridConfig = GridConfig(sizeMultiplier=self.sizeMultiplier)
        super().__init__(cols=11)

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
#       Grid Elements
#---------------------------------------------------------------------------------------------------
class GridElement( RelativeLayout ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__(size_hint = (None,None),size=gridConfig.gridElementSize, **kwargs)

class GridBattlefieldElement( GridElement ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__(gridConfig=gridConfig, **kwargs)
    #this is the coloured area inside the element (that makes it look as a grid):
        elementRectangle = Rectangle( size=gridConfig.battlefieldRectangleSize, pos=[5,5] )
        self.canvas.add( elementRectangle )

class GridLabelElement( GridElement ):
    def __init__(self, gridConfig, text='', **kwargs):
        super().__init__(gridConfig=gridConfig, **kwargs)
        elementText = Label(text=str(text))
        self.add_widget( elementText )

#---------------------------------------------------------------------------------------------------
#       Page Initializations
#---------------------------------------------------------------------------------------------------
class Screen( Widget ):

    config = None
    MainMenuView = None

    def __init__(self, **kwargs):
        self.config = MainConfig()
        Config.set('graphics', 'width', self.config.windowWidth) #this has to be done before calling super()
        Config.set('graphics', 'height', self.config.windowHeight) #todo  somekind of config?
        super().__init__(**kwargs)
        self.drawMainMenuView()

    def drawMainMenuView(self):
        self.clear_widgets()
        self.MainMenuView = MainMenuView()
        self.add_widget( self.MainMenuView )
        self.MainMenuView.draw()

    def drawGameScreenView(self):
        self.clear_widgets()
        self.gameScreenView = GameScreenView( size=self.config.windowSize)
        self.add_widget( self.gameScreenView )
        self.gameScreenView.draw()

#---------------------------------------------------------------------------------------------------
#       App Start
#---------------------------------------------------------------------------------------------------
class BattleshipApp(App):

    screen = None

    def build(self):
        global sessionStatus #FIXME: THIS IS MOST CERTAINLY NOT THE WAY TO DO IT, BUT HOW ELSE ?!?!?
        sessionStatus = SessionStatus()
        self.screen = Screen()
        return self.screen

    def on_start(self):
        print('start')


if __name__ == '__main__':
    BattleshipApp().run()
