__author__ = 'mihkel'
from kivy.uix.widget import Widget

class ParentFinder():

    def getGame(self): #return the Game object - I dont know how else to achieve it
        instance = self.parent
        while isinstance(instance, Widget):
            if instance.game!=None:
                return instance.game
            instance = instance.parent
        return None

    def getParentByClass(self, className): #return the parent object that has the given clas
        instance = self.parent
        #print('ise', self)
        #print('parent', instance)
        #print('getaparentbulcaaa')
        while isinstance(instance, Widget):
            if isinstance(instance, className):
                return instance
            #print(instance.parent)
            instance = instance.parent
        return None
