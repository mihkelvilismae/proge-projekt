__author__ = 'mihkel'
from .behaviours import HoverBehavior
from .parentFinder import ParentFinder
from .views import GridArea

from kivy.graphics import *
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.widget import Widget
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
    gridConfig = None

    zoneStatus = StringProperty( STATUS_NOT_VISIBLE )
    def __init__(self, ship, gridConfig, **kwargs):
        self.gridConfig = gridConfig
        super().__init__(size_hint=(None,None), size=self.gridConfig.battlefieldRectangleSize, **kwargs)
        self.ship = ship
        self.bind(zoneStatus=self.on_zoneStatus)

    def draw(self):
        self.clear_widgets()
        self.canvas.clear()
        self.pos=self.calculateShipZonePosition()
        self.shipZoneElements = self.createShipZoneElements()
        for shipZoneElement in self.shipZoneElements.copy():
            self.add_widget( shipZoneElement )
            shipZoneElement.draw()
            if self.ship.getGrid().isElementInGridBounds( shipZoneElement ):
                pass
            else:
                self.remove_widget( shipZoneElement )
                self.shipZoneElements.remove( shipZoneElement )

    def calculateShipZonePosition(self):
        if self.ship.direction==self.ship.DIRECTION_HORIZONTAL:
            position = (-self.gridConfig.battlefieldRectangleSize[0],-self.gridConfig.battlefieldRectangleSize[1])
        else:
            position = (-self.gridConfig.battlefieldRectangleSize[0],-self.gridConfig.shipBlockHeight*self.ship.length)
        return position

    def createShipZoneElements(self):
        shipZoneElements = []
        if self.ship.direction == self.ship.DIRECTION_HORIZONTAL:
            widthLength = self.ship.length+2
            heightLength = 3
        else:
            widthLength = 3
            heightLength = self.ship.length+2

        for x in range(0, widthLength):
            for y in range(0, heightLength):
                if self.ship.direction==self.ship.DIRECTION_HORIZONTAL:
                    if y==1 and x not in [0, widthLength-1]:
                        continue
                else:
                    if x==1 and y not in [0, heightLength-1]:
                        continue
                shipZoneElement = ShipZoneElement( shipZone=self, xMultiplier=x, yMultiplier=y )
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
        pass

#---------------------------------------------------------------------------------------------------------------
#   ShipZoneElement
#---------------------------------------------------------------------------------------------------------------
class ShipZoneElement( Widget, ParentFinder, HoverBehavior):
    shipzone = None
    xMultiplier = int
    yMultiplier = int
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
        return self.shipZone.getParentByClass(GridArea).grid.gridConfig.gridElementSize

    def on_enter(self):
        pass