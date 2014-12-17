__author__ = 'mihkel'
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty

#---------------------------------------------------------------------------------------------------
#       @ShipPort
#---------------------------------------------------------------------------------------------------
class ShipPort( BoxLayout ):
    shipPiers = {}
    shipsInPort = ListProperty([])
    game = None
    isSelectShipsAllowed = True

    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(orientation='vertical', **kwargs)
        self.bind(shipsInPort=self.onShipsInPort)

    def getShipByLength(self, length):
        return self.shipPiers[ length ].shipsInPier[0]

    def draw(self):
        for shipLength in range(1,5):
            shipPier = ShipPier( game=self.game )
            self.shipPiers[ shipLength ] = shipPier
            self.add_widget( shipPier )
            shipPier.draw()

    def onShipsInPort(self, instance, pos):
        if len(self.shipsInPort)==0:
            self.game.allShipsOnGrid = True

#---------------------------------------------------------------------------------------------------
#       @ShipPier
#---------------------------------------------------------------------------------------------------
class ShipPier( RelativeLayout ):
    shipsInPier = ListProperty([])
    shipCount = None
    game = None

    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(size=(300, 80), size_hint=(None, None), **kwargs)
        self.bind(shipsInPier=self.on_shipsInPier)

    def draw(self):
        self.drawShipCount()

    def getShipCountInPier(self):
        return len(self.shipsInPier)

    def drawShipCount(self):
        shipsInPierCount = self.getShipCountInPier()
        self.shipCount = Label( font_size='40sp', text = str(shipsInPierCount)) #todo put font size in conf
        self.add_widget( self.shipCount )
        self.shipCount.x = 200 #fixme: this works, but the backend part isnt beautiful

    def addShip(self, ship):
        ship.shipPier = self
        self.game.shipPort.shipsInPort.append( ship )
        self.shipsInPier.append(ship)
        self.add_widget( ship )

    def removeShip(self, ship):
        self.game.shipPort.shipsInPort.remove( ship )
        self.shipsInPier.remove( ship )
        self.remove_widget( ship )

    def updateShipCount(self):
        self.remove_widget(self.shipCount)
        self.drawShipCount()

    def on_shipsInPier(self, instance, pos ):
        if self.getShipCountInPier()==0:
            self.parent.remove_widget(self)
        else:
            self.updateShipCount()
