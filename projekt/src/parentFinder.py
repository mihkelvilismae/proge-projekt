__author__ = 'mihkel'
from kivy.uix.widget import Widget

class ParentFinder():

    def getGame(self): #return the Game object - I dont know how else to achieve it
        instance = self.parent
        while isinstance(instance, Widget):
            if hasattr(instance, 'game') and instance.game!=None:
                return instance.game
            instance = instance.parent
        return None

    def getParentByClass(self, className): #return the parent object that has the given clas
        instance = self.parent
        while isinstance(instance, Widget):
            if isinstance(instance, className):
                return instance
            instance = instance.parent
        return None
