from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import *
 
class RootWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.run()
 
    def run(self):
        gridLayout = GridLayoutWidget()
        self.add_widget( gridLayout )
        gridLayout.addChildren()
 
 
class GridLayoutWidget( GridLayout ):
    def __init__(self, **kwargs):
        super().__init__(cols=3,**kwargs)
 
    def addChildren(self):
        for i in range(0,3):
            child = Child( i )
            self.add_widget( child )
            child.draw()
 
    #def addChildrenAlternative(self):
    #    for i in range(0,3):
    #        btn = Button(text=str(i))
    #        self.add_widget( btn )
 
 
class Child( Widget ):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = str(text)
 
    def draw(self):
        self.add_widget( Button(text=self.text) )
 
 
class TestApp(App):
    def build(self):
        return RootWidget()
 
 
if __name__ == '__main__':
    TestApp().run()