__author__ = 'mihkel'


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
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        #print'onleave')
        pass
