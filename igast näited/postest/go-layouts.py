from __future__ import division, absolute_import, print_function
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
 
 
class GoGame(FloatLayout):
    def __init__(self, **kwargs):
        super(GoGame, self).__init__(**kwargs)
        s = min( Config.getint('graphics', 'width'), Config.getint('graphics', 'height') ) - 50
        self.board = GoBoard( size=(s,s), pos_hint={'center_x': .5, 'center_y': .5}, cols=2, rows=2, spacing=2 )
        self.add_widget( self.board )
 
class GoBoard(GridLayout):
    def __init__(self, **kwargs):
        super(GoBoard, self).__init__(**kwargs)
 
        with self.canvas:
            Color(1,0,0)
            Line( points=( 99,30, 99,700 ) )
            Line( points=( 30,99, 700,99 ) )
            Color(0,1,0)
            Line( points=( 101,30, 101,700 ) )
            Line( points=( 30,101, 700,101 ) )
 
        self.a_stone = GoStone()
        self.b_stone = GoStone()
        self.c_stone = GoStone()
        self.d_stone = GoStone()
        self.add_widget( self.a_stone )
        self.add_widget( self.b_stone )
        self.add_widget( self.c_stone )
        self.add_widget( self.d_stone )
 
class GoStone(Widget):
    def __init__(self, **kwargs):
        super(GoStone, self).__init__(**kwargs)
        with self.canvas:
            Color(1,1,1,.25)
            Rectangle(pos=self.pos, size=self.size)
 
class TTGoApp(App):
    def build(self):
        self.game = GoGame()
        return self.game
 
 
if __name__ == '__main__':
    TTGoApp().run()