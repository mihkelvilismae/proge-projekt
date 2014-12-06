__author__ = 'mihkel'
from .behaviours import HoverBehavior
from .parentFinder import ParentFinder
from .grid import Grid
from .views import BattleArea
from .gameconfig import *

from kivy.graphics import *
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.widget import Widget
import random
#---------------------------------------------------------------------------------------------------------------
#   ShipZone
#---------------------------------------------------------------------------------------------------------------
class ShipZone( RelativeLayout, HoverBehavior, ParentFinder ):

    STATUS_NOT_VISIBLE = 'notVisible'
    STATUS_GREEN = 'green'
    STATUS_RED = 'red'
    STATUS_GREY = 'grey'

    game = None
    ship = None

    zoneStatus = StringProperty( STATUS_NOT_VISIBLE )
    def __init__(self, ship, **kwargs):
        #self.game = game
        super().__init__(size_hint=(None,None), size=(50,50), **kwargs)
        #super().__init__(**kwargs)
        self.ship = ship
        self.bind(zoneStatus=self.on_zoneStatus)

    def draw(self):
        self.clear_widgets()
        self.canvas.clear()
        self.pos=(-50, -50)

        for shipZoneElement in self.createShipZoneElements():
            self.add_widget( shipZoneElement )
            shipZoneElement.draw()

        #elementRectangle = Rectangle(pos=self.pos, size=self.size)
        #elementRectangle = Rectangle(size=self.size)
        #print(elementRectangle)
        #self.canvas.add(Color(0,1,1))
        #self.canvas.add(elementRectangle)

    def createShipZoneElements(self):
        shipZoneElements = []
        #todo: take into account ship direction
        for x in range(0, self.ship.length+2):
            for y in [0,2]:
                shipZoneElement = ShipZoneElement( shipZone=self, xMultiplier=x, yMultiplier=y )
                shipZoneElements.append( shipZoneElement )
        shipZoneElement = ShipZoneElement( shipZone=self, xMultiplier=self.ship.length+1, yMultiplier=1 )
        shipZoneElements.append( shipZoneElement )
        shipZoneElement = ShipZoneElement( shipZone=self, xMultiplier=0, yMultiplier=1 )
        shipZoneElements.append( shipZoneElement )
        return shipZoneElements

    def getColor(self):
        if self.zoneStatus == self.STATUS_GREY:
            color = Color(0.8, 0.8, 0.6 , 0.5)
        #elif self.zoneStatus == self.STATUS_GREEN:
        else:
            color = Color(0, 1, 0, 0.5)
        return color

    def on_zoneStatus(self, instance, pos):
        self.draw()

    def on_enter(self):
        print('siesenes shipzonei', self)
        pass

#---------------------------------------------------------------------------------------------------------------
#   ShipZoneElement
#---------------------------------------------------------------------------------------------------------------
class ShipZoneElement( Widget, ParentFinder):
    shipzone = None
    game = None
    def __init__(self, shipZone, xMultiplier, yMultiplier, **kwargs):
        super().__init__(**kwargs)
        self.xMultiplier = xMultiplier
        self.yMultiplier = yMultiplier
        self.shipZone = shipZone

    def on_pos(self, instance, pos):
        self.draw()

    def draw(self):
        self.size = self.getZoneElementSize()
        self.pos = self.calculateZoneElementPos()
        self.canvas.add( self.shipZone.getColor() )
        self.canvas.add(Rectangle(size=self.size, pos=self.pos))

    def calculateZoneElementPos(self):
        xPosition = self.getZoneElementSize()[0]*self.xMultiplier
        yPosition = self.getZoneElementSize()[1]*self.yMultiplier
        return (xPosition, yPosition)

    def getZoneElementSize(self):
        #fixme: sometimes the first check fails? it should already be added and have a parent?
        if self.getParentByClass(BattleArea)!=None: #if parent is battleArea, then sizeMulttplier is 1
            size = GridConfig(sizeMultiplier=1).gridElementSize
        else:
            size = GridConfig(sizeMultiplier=1).gridElementSize
        return size
        #return self.getGame()