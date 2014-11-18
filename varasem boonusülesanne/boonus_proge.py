from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.graphics import Ellipse
from kivy.graphics import Color

# Kasutasin teeki(?) nimega Kivy (http://kivy.org/#home)
# Varem pole seda kasutanud

class BudgetScreen(BoxLayout):

    dataValues = {}
    motherGrossInput = None
    fatherGrossInput = None
    numberOfChildrenInput = None
    hasDataBeenEntered = False

    def __init__(self, **kwargs):
        Config.set('graphics', 'width', '300') #this has to be done before calling super()
        Config.set('graphics', 'height', '600')
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.resetDataValues()
        self.startDrawing()

    def startDrawing(self):
        self.clear_widgets()
        self.add_widget( self.inputElementsLayout() )
        self.add_widget( self.calculationButton() )
        self.add_widget( self.calculationResultLayout() )
        if self.hasDataBeenEntered:
            self.add_widget( self.drawCircleGraph() )

#------------------------------------------------------------------------------------------

    def resetDataValues(self):
        self.dataValues[ 'father' ] = {'grossIncome':0, 'netIncome':0, 'color': Color(1,0,0)}
        self.dataValues[ 'mother' ] = {'grossIncome':0, 'netIncome':0, 'color': Color(0,1,0)}
        self.dataValues[ 'childSupport' ] = {'numberOfChildren':0, 'netIncome':0, 'value':0, 'color': Color(1,1,0)}

    def getFamilySum(self):
        familyData = self.getDataValues()
        sumOfValues = sum([ familyData[key]['netIncome'] for key in familyData ])

        return round(sumOfValues,2)

    def setDataValue(self, person, type, value):
        self.dataValues[person][type] = value

    def getDataValues(self):
        return self.dataValues

    def getDataValue(self, person, type):
        return self.dataValues[person][type]

    def getNewValuesFromInputFields(self):
        self.hasDataBeenEntered = True
        motherGross =  int(self.motherGrossInput.text)
        fatherGross =  int(self.fatherGrossInput.text)
        numberOfChildren =  int(self.numberOfChildrenInput.text)

        self.setDataValue('mother','grossIncome', motherGross )
        self.setDataValue('mother','netIncome', round(self.calculateNet(motherGross),2))
        self.setDataValue('father','grossIncome', fatherGross )
        self.setDataValue('father','netIncome', round(self.calculateNet(fatherGross),2))
        self.setDataValue('childSupport','numberOfChildren', numberOfChildren )
        self.setDataValue('childSupport','netIncome', numberOfChildren*20 )

    def calculateNet( self, grossPay ):
        taxFreeSum = 144
        taxPercentage = 21
        #childSupport = 20
        taxableSum = grossPay-taxFreeSum
        taxSum = taxableSum * (taxPercentage/100)
        if (taxSum>0):
            grossPay = grossPay - taxSum
        return grossPay

#----------------------------------------------------------------
#   GRAPHICS:
#----------------------------------------------------------------
    def inputElementsLayout(self):
        inputElementsLayout = GridLayout()
        inputElementsLayout.cols = 2

        motherGrossLabel = Label(text='Ema bruto (€)')
        self.motherGrossInput = TextInput(multiline=False, text=str(self.getDataValue('mother','grossIncome')))
        fatherGrossLabel = Label(text='Isa bruto (€)')
        self.fatherGrossInput = TextInput(multiline=False, text=str(self.getDataValue('father','grossIncome')))
        numberOfChildrenLabel = Label(text='Lapsi (tk)')
        self.numberOfChildrenInput = TextInput(multiline=False, text=str(self.getDataValue('childSupport','numberOfChildren')))

        inputElementsLayout.add_widget( motherGrossLabel )
        inputElementsLayout.add_widget( self.motherGrossInput )
        inputElementsLayout.add_widget( fatherGrossLabel )
        inputElementsLayout.add_widget( self.fatherGrossInput )
        inputElementsLayout.add_widget( numberOfChildrenLabel )
        inputElementsLayout.add_widget( self.numberOfChildrenInput )

        return inputElementsLayout

    def calculationResultLayout(self):
        calculationResultsLayout = GridLayout()
        calculationResultsLayout.cols = 2

        dataValues = self.getDataValues()
        familyNetLabel = Label(text='Sissetulek (€)')
        familyNetResult = Label(text=str(self.getFamilySum()))
        motherNetLabel = Label(text='* ema neto (€)', color=(1,0,0,1))
        motherNetResult = Label(text=str(dataValues['mother']['netIncome']))
        fatherNetLabel = Label(text='* isa neto (€)', color=(0,1,0,1))
        fatherNetResult = Label(text=str(dataValues['father']['netIncome']))
        childSupportLabel = Label(text='* lastetoetus neto (€)', color=(1,1,0,1))
        childSupportResult = Label(text=str(dataValues['childSupport']['netIncome']))

        def doCalculation(obj):
            print('xxx')
            self.getNewValuesFromInputFields()
            self.startDrawing()

        childSupportResult.bind( on_press=doCalculation)


        calculationResultsLayout.add_widget( familyNetLabel )
        calculationResultsLayout.add_widget( familyNetResult )
        calculationResultsLayout.add_widget( motherNetLabel )
        calculationResultsLayout.add_widget( motherNetResult )
        calculationResultsLayout.add_widget( fatherNetLabel )
        calculationResultsLayout.add_widget( fatherNetResult )
        calculationResultsLayout.add_widget( childSupportLabel )
        calculationResultsLayout.add_widget( childSupportResult )

        return calculationResultsLayout

    def calculationButton(self):
        button = Button(text='Arvuta',size=(100,50),size_hint=(None,None), pos_hint= { 'center_x' : 0.5 })

        def doCalculation(obj):
            self.getNewValuesFromInputFields()
            self.startDrawing()

        button.bind( on_press=doCalculation)

        return button


    def drawCircleGraph(self):
        return self.circleGraph()

    def circleGraph(self):
        calculationResultsLayout = BoxLayout()
        chart_size = 175
        offset_rotation = 0

        sumOfValues = self.getFamilySum()
        dataValues = self.getDataValues()

        if sumOfValues>0:
            for key in dataValues:
                sectorAngle = 360/sumOfValues * dataValues[key]['netIncome']
                zone = Ellipse(
                            size=(chart_size, chart_size),
                            #segments=value * 3.6,
                            angle_start=offset_rotation,
                            angle_end= offset_rotation + sectorAngle,
                            #angle_end=offset_rotation + (value * 3.6),
                            t='in_quad'
                        )
                self.canvas.add( dataValues[key]['color'] )
                self.canvas.add(zone)

                offset_rotation += sectorAngle

        return calculationResultsLayout

#----------------------------------------------------------------


class MyApp(App):

    def build(self):
        main = BudgetScreen()

        return main


if __name__ == '__main__':
    MyApp().run()