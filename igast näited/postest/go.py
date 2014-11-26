import kivy
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.animation import Animation
 
class GoGame(Widget):
    def __init__(self, **kwargs):
        super(GoGame, self).__init__(**kwargs)
        self.stone = GoStone(size=(40,40))
        self.stone.center = (100,100)
        anim = Animation(x=500, y=500, duration=3)
        anim.start(self.stone)
        self.add_widget( self.stone )
 
class GoStone(Widget):
    def __init__(self, **kwargs):
        super(GoStone, self).__init__(**kwargs)
        with self.canvas:
            Color(1,1,1,.5)
            Rectangle(pos=self.pos, size=self.size)
 
class TTGoApp(App):
    def build(self):
        return GoGame()
 
 
if __name__ == '__main__':
    TTGoApp().run()