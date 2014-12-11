__author__ = 'mihkel'

from .behaviours import HoverBehavior
from .gameconfig import MainConfig
from .shipzone import ShipZone
from .parentFinder import ParentFinder
from .views import GridArea
from .shipport import ShipPort

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty

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
    position = (0,0)
    direction = 'H'
    shipPier = None
    shipRectangles = []
    shipZone = None
    startRowNr = int
    startColChar = str
    temporarilyRemovedFromMatrix = False
    gridConfig = None
    shipPositions = set()

    def __init__(self, gridConfig, length=1, **kwargs):
        self.color = color = Color(1,1,0)
        self.mainConfig = MainConfig()
        self.gridConfig = gridConfig
        super().__init__(size_hint=(None,None), pos=self.calculateShipPosition(), size=self.calculateShipSize(length), **kwargs)
        self.length = length
        self.drawShip()
        self.bind(shipStatus=self.on_status)
        self.shipStateMatrixElements = []
        self.shipZoneStateMatrixElements = []
        self.shipPositions = set()

    def getShipId(self):
        return self.startColChar+str(self.startRowNr)

    def getShipPort(self):
        return self.getParentByClass(ShipPort)

    def drawShip(self):
        self.clear_widgets()
        self.canvas.clear()
        for shipRectToRemove in self.shipRectangles.copy(): #FIXME: SHIPRECTANGLES STAY IN LOWER-LEFT PART OF CANVAS AND DONT DISAPPEAR
            self.remove_widget( shipRectToRemove )
            self.shipRectangles.remove(shipRectToRemove)
        for elementRectangle in self.createShipElementRectangles():
            self.add_widget(elementRectangle)
            self.shipRectangles.append( elementRectangle )
            elementRectangle.draw()

    def calculateShipPosition(self):
        if self.direction==Ship.DIRECTION_HORIZONTAL:
            position = self.pos
        else:
            position = (self.pos[0], self.pos[1]-self.gridConfig.shipBlockHeight*self.length)
        return position

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
            self.color = Color(1,0.2,0.2)
            if self.getGrid().sizeMultiplier==2: # ownGrid ship color
                self.color = Color(1,1,0, 0.5)
            self.addZone()

        self.drawShip()

    def addZone(self):
        if self.shipZone:
            self.remove_widget(self.shipZone)
            self.shipZone = None

        def drawZone(dt): #fixme: why is the clock required, how can i do it without it :S
            self.shipZone = ShipZone( self, self.gridConfig )
            self.add_widget(self.shipZone)
            self.shipZone.zoneStatus = ShipZone.STATUS_GREY
            self.shipZone.draw()
        Clock.schedule_once(drawZone, 0)

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
        self.shipStatus = self.STATUS_PLACED

    def createShipElementRectangles(self):
        shipBlockWidth = self.gridConfig.shipBlockWidth
        elementRectangles = list()
        elementPosition = (0,0)
        for i in range(0, self.length):
            elementRectangle = ShipElementRectangle( self, elementPosition )
            elementRectangles.append(elementRectangle)
            if self.direction == self.DIRECTION_HORIZONTAL:
                elementPosition = ( elementPosition[0]+shipBlockWidth, elementPosition[1] )
            else:
                elementPosition = ( elementPosition[0], elementPosition[1]-shipBlockWidth )
        return elementRectangles

    def calculateShipSize(self, shipLength):
        if self.direction==Ship.DIRECTION_HORIZONTAL:
            return (self.gridConfig.shipBlockWidth * shipLength, self.gridConfig.shipBlockHeight)
        else:
            return (self.gridConfig.shipBlockWidth, self.gridConfig.shipBlockHeight * shipLength)
        #return (self.mainConfig.shipBlockWidth * shipLength, self.mainConfig.shipBlockHeight)

    def on_pos(self, a,b): # TODO: WTF IS THIS?!?!
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
         self.size=self.parent.gridConfig.shipBlockSize
         self.canvas.clear()
         elementRectangle = Rectangle(pos=(self.pos[0]+4,self.pos[1]+4), size=self.size) #todo: pos shoudl come from conf
         self.canvas.add( self.ship.color )
         self.canvas.add( elementRectangle )

# event bindings:
     def on_touch_down(self, touch): #this fires on the event that someone clicks on the ship
        if self.collide_point(*touch.pos):
            if self.getGame().canSelectShip( self.ship ):
                if self.ship.shipStatus == self.ship.STATUS_SELECTED:
                    if self.ship.getGame().canRotateShip( self.ship):
                        self.ship.getGame().rotateShip( self.ship )
                self.ship.shipStatus = self.ship.STATUS_SELECTED

                return True
