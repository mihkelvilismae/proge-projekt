__author__ = 'mihkel'

# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.config import Config
# from kivy.graphics import *
# from kivy.graphics import Color, Ellipse, Line
# from kivy.core.text import Label as CoreLabel
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.relativelayout import RelativeLayout
# from kivy.uix.stacklayout import StackLayout
# import random

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
#---------------------------------------------------------------------------------------------------
#       Behaviours:
#---------------------------------------------------------------------------------------------------
class HoverBehavior():
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


    def checkIfMouseIsInWidget(self, mousePoint):
        widgetGlobalStartPosition = [self.to_window(self.pos[0], self.pos[1])[0], self.to_window(self.pos[0], self.pos[1])[1]]
        widgetGlobalEndPosition = [widgetGlobalStartPosition[0]+self.width, widgetGlobalStartPosition[1]+self.height]
        if widgetGlobalStartPosition[0] < mousePoint[0] and mousePoint[0] < widgetGlobalEndPosition[0] and widgetGlobalStartPosition[1] < mousePoint[1] and mousePoint[1] < widgetGlobalEndPosition[1]:
            return True
        else:
            return False

    def on_mouse_pos(self, *args):
        mousePosition = args[1]

        #inside = self.collide_point(*mousePosition) #- this uses the elements local position
        inside = self.checkIfMouseIsInWidget(mousePosition) #- this uses the elements global position, which it should
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = mousePosition
        self.hovered = inside
        if inside:
            #print('SIEENSE:',self)
            self.dispatch('on_enter')
        else:
            #print('VÖLJUS:',self)
            self.dispatch('on_leave')

    def on_enter(self):
        #print'onente')
        pass

    def on_leave(self):
        #print'onleave')
        pass
