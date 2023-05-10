from PyQt6.QtWidgets import *
import csv

class Item():
    def __init__(self, disName, refName, unitCost, doctorCost, patientCost, itemDuration):
        self.disName = disName
        self.refName = refName
        self.unitCost = unitCost
        self.doctorCost = doctorCost
        self.patientCost = patientCost
        try:
            self.itemDuration = int(itemDuration)
        except:
            self.itemDuration = None

    def __str__(self):
        return f'display name: {self.name}, reference name: {self.refName}, unit cost: {self.unitCost}, doctor cost: {self.doctorCost}, patient cost: {self.patientCost}'

displayNames = []
boxNames = []

def readItems():
    try:
        file = open('items.csv', 'r')
    except:
        sys.exit('Error with Items File. Confirm file format and path.')
    reader = csv.DictReader(file)
    for line in reader:
        displayNames.append(line["Item Name"])
    file.close()

def readBoxes():
    try:
        file = open('boxes.csv', 'r')
    except:
        sys.exit('Error with Boxes file. Confirm file format and path.')
    reader = csv.DictReader(file)
    for line in reader:
        boxNames.append(line["Name"])
    print(boxNames)
    file.close()

from view import *
class Controller(QMainWindow, Ui_mainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton_AddItem.clicked.connect(lambda: self.addItem())
        self.pushButton_AddContents.clicked.connect(lambda: self.addBox())
        self.pushButton_AddCustom.clicked.connect(lambda: self.addCustom())
        self.pushButton_ClearItems.clicked.connect(lambda: self.clear())
        self.pushButton_EditItems.clicked.connect(lambda: self.editItems())
        self.checkBox_MiscCosts.toggled.connect(lambda: self.addMisc())
        self.checkBox_VisionSource.toggled.connect(lambda: self.vsDiscount())

    def addItem(self):
        try:
            item = self.comboBox_Items.currentText()
            quantity = int(self.lineEdit_Quantity.text())
            if item not in displayNames or quantity < 1:
                raise Exception

            self.label_ItemException.setText('')
            self.comboBox_Items.setCurrentText('Select or Type Item')
            self.lineEdit_Quantity.setText('1')

        except:
            self.comboBox_Items.setCurrentText('Select or Type Item')
            self.lineEdit_Quantity.setText('1')
            self.label_ItemException.setText('Invalid item type (see dropdown list) or quantity (must be nonzero integer)')

    def addBox(self):
        try:
            box = self.comboBox_Boxes.currentText()
            if box not in boxNames:
                raise Exception
            self.label_BoxException.setText('')
            print(item)
        except:
            self.label_BoxException.setText('Invalid box type (see dropdown list)')

    def addCustom(self):
        pass

    def clear(self):
        pass

    def editItems(self):
        pass

    def addMisc(self):
        pass

    def vsDiscount(self):
        pass
