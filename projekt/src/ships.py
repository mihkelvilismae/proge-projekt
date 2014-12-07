__author__ = 'mihkel'

from .behaviours import HoverBehavior
from .gameconfig import MainConfig
from .shipzone import ShipZone
from .parentFinder import ParentFinder
from .grid import Grid
from .views import GridArea

from kivy.clock import Clock
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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
import random

#---------------------------------------------------------------------------------------------------
#       @Ship
#---------------------------------------------------------------------------------------------------

class Ship( RelativeLayout, HoverBehavior, ParentFinder ):
    STATUS_WAITING_TO_BE_PICKED_UP = 'waitingToBePickedUp'
    STATUS_PLACED = 'placed'
    STATUS_SELECTED = 'selected'

    isInPort = False

    DIRECTION_HORIZONTAL = 'H'
    DIRECTION_VERTICAL = 'V'

    shipStatus = StringProperty( STATUS_WAITING_TO_BE_PICKED_UP ) # baseerub nupp.py näitel
    length = 1
    color = Color(1,1,0)
    position = (0,0)
    direction = 'H'
    shipPier = None
    shipRectangles = []
    shipZone = None
    startRowNr = int
    startColChar = str
    temporarilyRemovedFromMatrix = False
    gridConfig = None

    #shipStateMatrixElements = []
    #shipZoneStateMatrixElements = []

    def __init__(self, gridConfig, length=1, **kwargs):
        self.mainConfig = MainConfig()
        self.gridConfig = gridConfig
        super().__init__(size_hint=(None,None), pos=self.position, size=self.calculateShipSize(length), **kwargs)
        self.length = length
        self.drawShip()
        self.bind(shipStatus=self.on_status)
        self.shipStateMatrixElements = []
        self.shipZoneStateMatrixElements = []

    def drawShip(self):
        self.clear_widgets()
        self.canvas.clear()
        #for i,elementRectangle in zip([Color(0,1,1),Color(1,1,0),Color(0,0,1),Color(1,1,1)], self.createShipElementRectangles()):
        for shipRectToRemove in self.shipRectangles.copy(): #FIXME: SHIPRECTANGLES STAY IN LOWER-LEFT PART OF CANVAS AND DONT DISAPPEAR
            self.remove_widget( shipRectToRemove )
            self.shipRectangles.remove(shipRectToRemove)
        for elementRectangle in self.createShipElementRectangles():
            self.add_widget(elementRectangle)
            self.shipRectangles.append( elementRectangle )
            elementRectangle.draw()

    def getGrid(self):
        return self.getParentByClass( GridArea ).grid

# EVENT BINDINGS (start):
    def on_status(self, instance, pos): #this fires when the status changes
        if self.shipStatus==self.STATUS_SELECTED:
            self.color = Color(1,0,1)
            self.game.setSelectedShip(self)
            self.getGame().temporarilyRemoveShipFromMatrix(self)
        elif self.shipStatus==self.STATUS_WAITING_TO_BE_PICKED_UP:
            self.color = Color(1,1,0)
        elif self.shipStatus==self.STATUS_PLACED:
            self.addZone()
            self.color = Color(0,1,1)

        self.drawShip()

    def addZone(self):
        print('addzone-----------------------')
        if self.shipZone:
            self.remove_widget(self.shipZone)
            self.shipZone = None

        def drawZone(dt): #fixme: why is the clock required, how can i do it without it :S
            self.shipZone = ShipZone( self, self.gridConfig )
            self.add_widget(self.shipZone)
            self.shipZone.zoneStatus = ShipZone.STATUS_GREY
            self.shipZone.draw()
        Clock.schedule_once(drawZone, 0)

    #def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
    #    return super(Ship, self).on_touch_down(touch) #propagates to children ,        http://kivy.org/docs/guide/events.html#trigger-events -  search: 'At Line 5:'
    # event bindings:
    def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
        if self.collide_point(*touch.pos):
            #if self.ship.shipStatus == self.ship.STATUS_SELECTED:
                #if game.canRotateShip( self.ship):
                #    game.rotateShip( self.ship )
            self.shipStatus = self.STATUS_SELECTED

            return True

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

    def createShipElementRectangles(self):
        shipBlockWidth = self.gridConfig.shipBlockWidth
        elementRectangles = list()
        elementPosition = (0,0)
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
    #   pass

    def bombardGridxxx(self):
        pass

    def calculateShipSize(self, shipLength):
        #todo: direction
        return (self.gridConfig.shipBlockWidth * shipLength, self.gridConfig.shipBlockHeight)
        #return (self.mainConfig.shipBlockWidth * shipLength, self.mainConfig.shipBlockHeight)

    def on_pos(self, a,b):
        if self.getGame()!=None:
            self.getGame().shipPlacementArea.grid.gameState.removeShipFromGameStateMatrix(self)

#---------------------------------------------------------------------------------------------------------------
#   ShipElementRectangle
#---------------------------------------------------------------------------------------------------------------
class ShipElementRectangle( Widget, HoverBehavior, ParentFinder ):
     ship = None
     color = Color()

     def __init__(self, ship, elementPosition, **kwargs):
        super().__init__(size_hint=(None,None), pos=elementPosition, **kwargs)
        self.ship = ship


     def draw(self):
         #grid = self.getParentByClass(Grid)
         #size = grid.gridConfig().gridElementSize
         self.size=self.parent.gridConfig.shipBlockSize
         self.canvas.clear()
         elementRectangle = Rectangle(pos=self.pos, size=self.size)
         self.canvas.add( self.ship.color )
         self.canvas.add( elementRectangle )
         #self.ship.shipRectangles.append( elementRectangle )

# event bindings:
     def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
         2
        #---if self.collide_point(*touch.pos):
            #print('sai pihta')
            #if self.ship.shipStatus == self.ship.STATUS_SELECTED:
                #if game.canRotateShip( self.ship):
                #    game.rotateShip( self.ship )
        #----    self.ship.shipStatus = self.ship.STATUS_SELECTED

        #----  return True

     def on_enter(self):
         2
         #self.draw()

     def on_leave(self):
         2
         #self.draw()