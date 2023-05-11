from PyQt6.QtWidgets import *
import csv
from view import *
import sys

labelNames = [[f'self.label_ItemList{j + 1}_{i + 1}' for i in range(0, 5)] for j in range(0, 21)]
pushButtonNames = [[f'self.pushButton_ItemList{j + 1}_{i + 1}' for i in range(0, 3)] for j in range(0, 21)]
print(labelNames)
print(pushButtonNames)

def readData():
    try:
        global items
        items = list(csv.reader(open('items.csv', 'r')))
        global displayNames
        displayNames = []
        for row in items:
            displayNames.append(row[0])
        items.pop(0)
        displayNames.pop(0)
    except:
        sys.exit('Error with Items data. Confirm file format and path.')

    try:
        global boxes
        boxes = list(csv.reader(open('boxes.csv', 'r')))
        global boxNames
        boxNames = []
        for row in boxes:
            boxNames.append(row[0])
        boxes.pop(0)
        boxNames.pop(0)
    except:
        sys.exit('Error with Boxes data. Confirm file format and path.')
    print(boxes)
    print(boxNames)

class Controller(QMainWindow, Ui_mainWindow):
    uniqueItems = {}
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
        self.pushButton_ItemList1_1.clicked.connect(lambda: self.clearItem())
        self.pushButton_ItemList1_2.clicked.connect(lambda: self.decreaseItem())
        self.pushButton_ItemList1_3.clicked.connect(lambda: self.increaseItem())

    def addItem(self):
        try:
            item = self.comboBox_Items.currentText()
            quantity = int(self.lineEdit_Quantity.text())
            index = displayNames.index(item)

            if quantity < 1:
                raise Exception

            if item in self.uniqueItems:
                position = list(self.uniqueItems.keys()).index(item)
                oldQuantity = int(self.uniqueItems[item])
                self.uniqueItems[item] = str(oldQuantity + quantity)
                exec(labelNames[position][1] + '.setText(str(self.uniqueItems[item]))')
            else:
                position = len(list(self.uniqueItems.keys()))
                self.uniqueItems[item] = quantity
                exec(labelNames[position][0] + '.setText(item)')
                exec(labelNames[position][1] + '.setText(str(quantity))')

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
            index = boxNames.index(box)
            self.label_BoxException.setText('')
            contents = boxes[index]

            if contents[0] in boxNames:
                contents.pop(0)

            for i in range(0, int(len(contents)), 2):
                quantity = int(contents[i])
                item = contents[i + 1]
                if item in self.uniqueItems:
                    position = list(self.uniqueItems.keys()).index(item)
                    oldQuantity = int(self.uniqueItems[item])
                    self.uniqueItems[item] = str(oldQuantity + quantity)
                    exec(labelNames[position][1] + '.setText(str(self.uniqueItems[item]))')
                else:
                    position = len(list(self.uniqueItems.keys()))
                    self.uniqueItems[item] = quantity
                    exec(labelNames[position][0] + '.setText(item)')
                    exec(labelNames[position][1] + '.setText(str(quantity))')

            self.label_BoxException.setText('')
            self.comboBox_Boxes.setCurrentText('Select or Type Item')
        except:
            self.label_BoxException.setText('')
            self.comboBox_Boxes.setCurrentText('Select or Type Item')
            self.label_BoxException.setText('Invalid box type (see dropdown list)')

    def addCustom(self):
        pass

    def clear(self):
        pass

    def editItems(self):
        position = len(list(self.uniqueItems.keys()))
        currentState = self.pushButton_EditItems.text()
        if currentState == 'Edit Item Quantity':
            for i in range(position):
                exec(pushButtonNames[i][0] + '.setEnabled(True)')
                exec(pushButtonNames[i][0] + ".setText('X')")
                exec(pushButtonNames[i][0] + '.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))')
            for i in range(position):
                exec(pushButtonNames[i][1] + '.setEnabled(True)')
                exec(pushButtonNames[i][1] + ".setText('-')")
                exec(pushButtonNames[i][1] + '.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))')
            for i in range(position):
                exec(pushButtonNames[i][2] + '.setEnabled(True)')
                exec(pushButtonNames[i][2] + ".setText('+')")
                exec(pushButtonNames[i][2] + '.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))')
            self.pushButton_EditItems.setText('Done')
        else:
            for i in range(position):
                exec(pushButtonNames[i][0] + ".setText('')")
                exec(pushButtonNames[i][0] + '.setEnabled(False)')
                exec(pushButtonNames[i][0] + '.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))')
            for i in range(position):
                exec(pushButtonNames[i][1] + ".setText('')")
                exec(pushButtonNames[i][1] + '.setEnabled(False)')
                exec(pushButtonNames[i][1] + '.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))')
            for i in range(position):
                exec(pushButtonNames[i][2] + ".setText('')")
                exec(pushButtonNames[i][2] + '.setEnabled(False)')
                exec(pushButtonNames[i][2] + '.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))')
            self.pushButton_EditItems.setText('Edit Item Quantity')

    def addMisc(self):
        pass

    def vsDiscount(self):
        pass

    def clearItem(self):
        pass

    def decreaseItem(self):
        pass

    def increaseItem(self):
        pass

    def calcTotals(self):
        pass