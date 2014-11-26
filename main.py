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
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
import random

#---------------------------------------------------------------------------------------------------
#       Config
#---------------------------------------------------------------------------------------------------
class MainConfig():
    def __init__(self, sizeMultiplier=1, **kwargs):
        self.gridConfig = GridConfig()
    # application window size:
        self.windowWidth = 1400
        self.windowHeight = 700
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
#       Behaviours:
#---------------------------------------------------------------------------------------------------
class HoverBehavior(): #todo change this from relativeLayout to widget
    # taken from here: https://groups.google.com/forum/#!topic/kivy-users/So0NMyLa6Vs

    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        from kivy.core.window import Window # fixme: why does importing this fk up the screen size ?!?!?
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        pos = args[1]
        inside = self.collide_point(*pos)
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        #print'onente')
        pass

    def on_leave(self):
        #print'onleave')
        pass

#---------------------------------------------------------------------------------------------------
#       @Game
#---------------------------------------------------------------------------------------------------
game = None #FIXME: SEE BELOW IN MAIN APP

class Game( Widget ):
    selectedShip = ObjectProperty(None)
    ships = list()
    screen = None
    mainGrid = None
    shipPort = None

    def startGame(self):
        self.screen.drawGameScreenView()
        self.createShips()
        self.setupShipsInPort()

    def __init__(self, **kwargs):
        1
        #self.bind(selectedShip=self.onSelectedShipChange)

    def setSelectedShip(self, ship):
        self.unselectShips( ship )
        self.selectedShip = ship

    #def onSelectedShipChange(self, instance, newValue):
    #    #print('seelectedwdaw')
    #    1

    def createShips(self):
        for i in range(1,5):
            ship = Ship(i)
            game.ships.append( ship )

    def setupShipsInPort(self):
        for ship in self.ships:
            2

    #def placeShipToPort(self):

    def canShipBePlaced(self, ship, battlefieldGridElement): #todo implement logic for out of borders etc
        if not isinstance( ship, Ship ):
            return False
        return True

    def placeShipToGrid(self, ship, battlefieldGridElement):
        ship.shipStatus = ship.STATUS_PLACED
        ship.placeShip( battlefieldGridElement.pos )
        self.setSelectedShip(ObjectProperty(None))

    def canRotateShip(self, ship): #todo implement this
        if not isinstance( ship, Ship ):
            return False
        return True

    def rotateShip(self, ship):
        ship.rotateShip()

    def unselectShips(self, shipNotToUnselect=None):
        for ship in self.ships:
            if ship!=shipNotToUnselect:
                ship.shipStatus = ship.STATUS_WAITING_TO_BE_PICKED_UP

#---------------------------------------------------------------------------------------------------
#       MainMenuView
#---------------------------------------------------------------------------------------------------
class MainMenuView( Widget ):

    #def __init__(self, **kwargs):
    #    super().__init__(cols=2,**kwargs)

    def draw(self):
        self.addStartButtonLabel()

    def addStartButtonLabel(self):
        randomlabel = Label(text='[ref=startGame]START[/ref]', markup=True)
        self.add_widget( randomlabel )
        def drawGameScreenView( object, value ):
            game.startGame()
        randomlabel.bind(on_ref_press=drawGameScreenView)

#---------------------------------------------------------------------------------------------------
#       GameScreenView
#---------------------------------------------------------------------------------------------------
class GameScreenView( BoxLayout ):
    shipPort = None
    smallerGrid = None
    mainGrid = None

    def __init__(self, **kwargs):
        super().__init__(cols=2,**kwargs)
        #self.size_hint = (1,1)
        #self.size = (900,600)


    def draw(self):
        self.size = self.parent.size
        self.drawMainGrid()
        #self.drawSmallerGrid()
        self.drawShipPort()

    def drawShipPort(self):
        game.shipPort = ShipPort()
        self.add_widget( game.shipPort )

    def drawSmallerGrid(self): #todo: can be joined with drawMainGrid()?
        self.smallerGrid = Grid(sizeMultiplier=2)
        self.add_widget( self.smallerGrid )
        self.smallerGrid.addGridElements()

    def drawMainGrid(self):
        self.mainGrid = Grid(sizeMultiplier=1)
        self.add_widget( self.mainGrid )
        self.mainGrid.addGridElements()

#---------------------------------------------------------------------------------------------------
#       @Ship
#---------------------------------------------------------------------------------------------------
class Ship( Widget ):
    STATUS_WAITING_TO_BE_PICKED_UP = 'waitingToBePickedUp'
    STATUS_PLACED = 'placed'
    STATUS_SELECTED = 'selected'

    DIRECTION_HORIZONTAL = 'H'
    DIRECTION_VERTICAL = 'V'

    shipStatus = StringProperty( STATUS_WAITING_TO_BE_PICKED_UP ) # baseerub nupp.py näitel
    length = 1
    color = Color(1,1,0)
    position = (0,0)
    direction = 'H'

    def __init__(self, length=1, **kwargs):
        self.mainConfig = MainConfig()
        super().__init__(size_hint=(None,None), pos=self.position, size=self.calculateShipSize(length), **kwargs)
        self.length = length
        self.drawShip()
        self.bind(shipStatus=self.on_status)

# EVENT BINDINGS (start):
    def on_status(self, instance, pos): #this fires when the status changes
        #print( self.shipStatus )
        if self.shipStatus==self.STATUS_SELECTED:
            self.color = Color(1,0,1)
            game.setSelectedShip(self)
        elif self.shipStatus==self.STATUS_WAITING_TO_BE_PICKED_UP:
            self.color = Color(1,1,0)
        elif self.shipStatus==self.STATUS_PLACED:
            self.color = Color(0,1,1)

        self.drawShip()

    def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
        return super(Ship, self).on_touch_down(touch) #propagates to children ,        http://kivy.org/docs/guide/events.html#trigger-events -  search:'At Line 5:'


# EVENT BINDINGS (end)

    def rotateShip(self):
        self.size = (self.height, self.width)
        if self.direction == self.DIRECTION_HORIZONTAL:
            self.direction = self.DIRECTION_VERTICAL
        else:
            self.direction = self.DIRECTION_HORIZONTAL
        self.drawShip()

    def placeShip(self, position):
        self.pos = position
        self.drawShip()

    def drawShip(self):
        self.clear_widgets()
        self.canvas.clear()
        #for i,elementRectangle in zip([Color(0,1,1),Color(1,1,0),Color(0,0,1),Color(1,1,1)], self.createShipElementRectangles()):
        for elementRectangle in self.createShipElementRectangles():
            self.add_widget(elementRectangle)

    def createShipElementRectangles(self):
        shipBlockWidth = self.mainConfig.shipBlockWidth
        elementRectangles = list()
        elementPosition = self.pos
        for i in range(0, self.length):
            #elementRectangle = Rectangle(pos=elementPosition, size=(shipBlockWidth, shipBlockWidth))
            elementRectangle = ShipElementRectangle( self, elementPosition )
            elementRectangles.append(elementRectangle)
            if self.direction == self.DIRECTION_HORIZONTAL:
                elementPosition = ( elementPosition[0]+shipBlockWidth, elementPosition[1] )
            else:
                elementPosition = ( elementPosition[0], elementPosition[1]+shipBlockWidth )
        return elementRectangles

    #def bombardShipPart(self):
    1

    def calculateShipSize(self, shipLength):
        return (self.mainConfig.shipBlockWidth * shipLength, self.mainConfig.shipBlockHeight)

class ShipElementRectangle( Widget, HoverBehavior ):
     ship = None
     color = Color()

     def __init__(self, ship, elementPosition, **kwargs):
        size = (MainConfig().shipBlockWidth, MainConfig().shipBlockWidth)
        super().__init__(size_hint=(None,None), pos=elementPosition, size=size, **kwargs)
        self.ship = ship
        self.draw()

     def draw(self):
         self.canvas.clear()
         elementRectangle = Rectangle(pos=self.pos, size=self.size)
         self.canvas.add( self.ship.color )
         self.canvas.add( elementRectangle )

# event bindings:
     def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
        ##print('ShipElementRectangle - click')
        if self.collide_point(*touch.pos):
            #print('sai pihta')
            #if self.ship.shipStatus == self.ship.STATUS_SELECTED:
                #if game.canRotateShip( self.ship):
                #    game.rotateShip( self.ship )
            self.ship.shipStatus = self.ship.STATUS_SELECTED

            return True

     def on_enter(self):
         print('xxxx')
         self.draw()

     def on_leave(self):
         print('xxxx')
         self.draw()
#---------------------------------------------------------------------------------------------------
#       Ship placement location
#---------------------------------------------------------------------------------------------------
class ShipPort( GridLayout ): #todo: this should also show status of bombed ships
    shipPier = {}

    def __init__(self, **kwargs):
        super().__init__(cols=2,**kwargs)
        #self.createShips() #todo move this somewhere else
        #self.add_widget(Button(text='vajutaaaaaaaaaaaaa'))
        self.draw()

    def draw(self):
        for shipLength in range(1,5):
            shipPier = ShipPier( str(shipLength) )
            shipCount = ShipCount( shipPier )
            shipPier.shipCount = shipCount
            self.add_widget( shipPier )
            self.add_widget( shipCount )

class ShipPier( RelativeLayout ):
    shipsInPier = ListProperty([])
    shipCount = None
    def __init__(self, shipLength, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text = shipLength))
        self.bind(shipsInPier=self.on_shipsInPier)
        #game.shipPort.shipPier[ int(shipLength) ] = []

    def addShip(self, ship):
        self.add_widget( ship )

    def on_shipsInPier(self):
        self.shipCount.updateShipCount()

class ShipCount( RelativeLayout ):
    shipPier = None
    def __init__(self, shipPier, **kwargs):
        self.shipPier = shipPier
        super().__init__(**kwargs)
        self.updateShipCount()

    def updateShipCount(self):
        self.clear_widgets()
        shipsInPierCount = len(self.shipPier.shipsInPier)
        self.add_widget(Label(text = str(shipsInPierCount)))


#---------------------------------------------------------------------------------------------------
#       @Grid
#---------------------------------------------------------------------------------------------------
class Grid( GridLayout ):
    sizeMultiplier = 1
    gridElements = dict()
    gridConfig = None

    def __init__(self, sizeMultiplier=1 ):
        self.sizeMultiplier = sizeMultiplier
        self.gridConfig = GridConfig(sizeMultiplier=self.sizeMultiplier)
        super().__init__(cols=11)
        game.mainGrid = self

    def addGridElements(self):

        self.gridElements = dict()
        game.gridElements = self.gridElements
        for rowNr in range(0,11):
            self.gridElements[ rowNr ] = dict()
            for colNr, colCharacter in enumerate(list(' ABCDEFGHIJ')):
                if 1 and (rowNr==0 or colNr==0):
                    if rowNr==0:
                        gridLabelElementText = colCharacter
                    elif colNr==0:
                        gridLabelElementText = rowNr
                    gridElement = GridLabelElement(text=gridLabelElementText, gridConfig = self.gridConfig) #pos=self.calculcateGridElementPosition(rowNr,colNr)
                else:
                    gridElement = GridBattlefieldElement( self.gridConfig, rowNr, colCharacter) #, pos=self.calculcateGridElementPosition(rowNr,colNr
                    self.gridElements[rowNr][colCharacter] = gridElement
                self.add_widget( gridElement )
                gridElement.draw()

    def calculcateGridElementPosition(self, rowNr, colNr):
        position = (self.gridConfig.battlefieldRectangleSize[0] * rowNr, self.gridConfig.battlefieldRectangleSize[1] * colNr)
        return position


#---------------------------------------------------------------------------------------------------
#       Grid Elements
#---------------------------------------------------------------------------------------------------
class GridElement( RelativeLayout, HoverBehavior ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__(size_hint = (None,None), size=gridConfig.gridElementSize, **kwargs)

class PointerRectangle( Widget ):
    def __init__(self, gridConfig, **kwargs):
        super().__init__( **kwargs)
        tooltipRectangleColor = Color(1, 0, 0, .5, mode='rgba')
        self.canvas.add( tooltipRectangleColor )
        tooltipRectangle = Rectangle(size=gridConfig.battlefieldRectangleSize, pos=[5,5])
        self.canvas.add( tooltipRectangle )

        tooltipRectangleColor = Color(1,1,1)  #fixme: unless I do this, it doesnt display the pointerRectangle correctly. why??
        self.canvas.add( tooltipRectangleColor  )

class GridBattlefieldElement( GridElement ):
    rowCoordinate = None
    columnCoordinate = None

    def __init__(self, gridConfig, rowCoordinate, columnCoordinate, **kwargs):
        #printkwargs)
        self.rowCoordinate = rowCoordinate
        self.columnCoordinate = columnCoordinate
        self.gridConfig = gridConfig
        super().__init__(gridConfig=gridConfig, **kwargs)
        #self.draw()

    def draw(self):
    #this is the coloured area inside the element (that makes it look as a grid):
        elementRectangle = Rectangle( pos_hint=(None,None), size=self.gridConfig.battlefieldRectangleSize, pos=self.calculateElementRectanglePosition() )
        self.canvas.add( elementRectangle )

    def removePointerRectangle(self):
        self.remove_widget( self.tooltipRectangle )

    def addPointerRectangle(self):
        ##print'addponter')
        self.tooltipRectangle = PointerRectangle( self.gridConfig )
        self.add_widget( self.tooltipRectangle )

    def calculateElementRectanglePosition(self):
        return (self.pos[0]+5, self.pos[1]+5)

# EVENT BINDINGS (start):
    def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
        #print'GridBattlefieldElement - click')
        if self.collide_point(*touch.pos):
            #print'sai pihta')
            if game.canShipBePlaced(game.selectedShip, self): #todo should i check in game and then do placement in ship ?
                game.placeShipToGrid(game.selectedShip, self)
            return True

    def on_enter(self):
        self.addPointerRectangle()

    def on_leave(self):
        self.removePointerRectangle()
# EVENT BINDINGS (end):

class GridLabelElement( GridElement ):
    def __init__(self, gridConfig, text='', **kwargs):
        self.text = str(text)
        super().__init__(gridConfig=gridConfig, **kwargs)
        #self.bind(on_motion=on_motion)

        #def on_motion(self, etype, motionevent):
        #    2
    def draw(self):
        elementText = Label(text=self.text)
        self.add_widget( elementText )
#---------------------------------------------------------------------------------------------------
#       Page Initializations
#---------------------------------------------------------------------------------------------------
class Screen( Widget ):

    config = None
    MainMenuView = None

    def __init__(self, **kwargs):
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
        self.screen = Screen()
        game.screen = self.screen
        return self.screen

    def on_start(self):
        3
        #print'start')


if __name__ == '__main__':
    BattleshipApp().run()
