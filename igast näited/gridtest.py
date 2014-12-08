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
 
class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.run()
 
    def run(self):
        gridLayout = GridLayoutWidget()
        self.add_widget( gridLayout )
        gridLayout.addChildren()

        gridLayout = GridLayoutWidget()
        self.add_widget( gridLayout )
        gridLayout.addChildren()

 
class GridLayoutWidget( GridLayout ):
    def __init__(self, **kwargs):
        super().__init__(cols=1,**kwargs)
 
    def addChildren(self):
        for i in range(0,3):
            child = Child( i )
            self.add_widget( child )
            child.draw()
            print('How can I get the absolute position of the child here ?')
            print("And how can I get the Child widget's position relative to the position of its parent, the GridLayoutWidget?")
            print(child.pos) #this only gives me [0,0]
 
class Child( BoxLayout ):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = str(text)
 
    def draw(self):
        btn = Button(text=self.text)
        self.add_widget( btn )
        def xxx(self):
            print(self.pos)
            print(self.to_local(self.x, self.y))
            print(self.to_window(self.x, self.y))
            print(self.to_window(self.x, self.y))
        btn.bind( on_press=xxx)

 
 
class TestApp(App):
    def build(self):
        return RootWidget()
 
 
if __name__ == '__main__':
    TestApp().run()