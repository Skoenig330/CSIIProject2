from PyQt6.QtWidgets import *
import csv
from view import *
import sys
from functools import partial

labelNames = [[f'self.label_ItemList{j + 1}_{i + 1}' for i in range(0, 5)] for j in range(0, 21)]
pushButtonNames = [[f'self.pushButton_ItemList{j + 1}_{i + 1}' for i in range(0, 3)] for j in range(0, 21)]

def readData() -> None:
    '''
    Method to read data from the items.csv and boxes.csv files.
    :return:
    '''
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

class Controller(QMainWindow, Ui_mainWindow):
    '''
    A class representing details for a window object.
    '''
    uniqueItems = {}
    def __init__(self, *args, **kwargs) -> None:
        '''
        constructor object to create window.
        :param args:
        :param kwargs:
        '''
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton_AddItem.clicked.connect(lambda: self.addItem())
        self.pushButton_AddContents.clicked.connect(lambda: self.addBox())
        self.pushButton_AddCustom.clicked.connect(lambda: self.addCustom())
        self.pushButton_ClearItems.clicked.connect(lambda: self.clear())
        self.pushButton_EditItems.clicked.connect(lambda: self.editItems())
        self.checkBox_MiscCosts.toggled.connect(lambda: self.calcTotals())
        self.checkBox_VisionSource.toggled.connect(lambda: self.calcTotals())
        for button in pushButtonNames:
            row = str(pushButtonNames.index(button) + 1)
            exec('self.pushButton_ItemList' + row + '_1.clicked.connect(partial(self.clearItem, row))')
        for button in pushButtonNames:
            row = str(pushButtonNames.index(button) + 1)
            exec('self.pushButton_ItemList' + row + '_2.clicked.connect(partial(self.decreaseItem, row))')
        for button in pushButtonNames:
            row = str(pushButtonNames.index(button) + 1)
            exec('self.pushButton_ItemList' + row + '_3.clicked.connect(partial(self.increaseItem, row))')
        self.calcTotals()

    def addItem(self) -> None:
        '''
        Method to add an item to the item list on the right side of window.
        :return:
        '''
        editItemsState = self.pushButton_EditItems.text()
        if editItemsState == 'Done':
            self.editItems()

        try:
            item = self.comboBox_Items.currentText()
            quantity = int(self.lineEdit_Quantity.text())
            index = displayNames.index(item) # Checks that item is in displayNames, throws an error if not.
            if quantity < 1:
                raise Exception

            if item in self.uniqueItems:
                position = list(self.uniqueItems.keys()).index(item)
                newQuantity = int(self.uniqueItems[item]) + quantity
                self.uniqueItems[item] = str(newQuantity)
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
            self.label_ItemException.setText('Invalid item type (see dropdown list) or quantity (must be a positive integer)')
        self.calcTotals()

    def addBox(self) -> None:
        '''
        Method to add items from a box (group of items) to the item list on the right.
        :return:
        '''
        editItemsState = self.pushButton_EditItems.text()
        if editItemsState == 'Done':
            self.editItems()

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
                self.calcTotals()

            self.label_BoxException.setText('')
            self.comboBox_Boxes.setCurrentText('Select or Type Item')
        except:
            self.label_BoxException.setText('')
            self.comboBox_Boxes.setCurrentText('Select or Type Item')
            self.label_BoxException.setText('Invalid box type (see dropdown list)')


    def addCustom(self) -> None:
        '''
        Method to create and add a custom item to the item list on the right.
        :return:
        '''
        editItemsState = self.pushButton_EditItems.text()
        if editItemsState == 'Done':
            self.editItems()
        try:
            item = self.lineEdit_Name.text()
            quantity = int(self.lineEdit_QuantityCustom.text())
            uCost = int(self.lineEdit_UnitPrice.text())
            dCost = self.lineEdit_DoctorCost.text()
            minimum = self.lineEdit_Minimum.text()

            if item == "":
                raise ValueError

            if type(dCost) == '':
                dCost = float(uCost * 1.3)
            else:
                dCost = int(dCost)

            if type(minimum) == '':
                minimum = float(uCost * 1.5)
            else:
                minimum = int(minimum)

            if item in self.uniqueItems:
                raise Exception
            else:
                position = len(list(self.uniqueItems.keys()))
                self.uniqueItems[item] = quantity
                exec(labelNames[position][0] + '.setText(item)')
                exec(labelNames[position][1] + '.setText(str(quantity))')
                displayNames.append(item)

            values = [item, f'{uCost:.2f}', f'{dCost:.2f}', f'{minimum:.2f}']
            items.extend([values])
            self.calcTotals()
        except ValueError:
            self.label_CustomException.setText('Quantity and Unit Cost are required. Unit Cost, Doctor Cost, and Minimum must all be positive integer')
        except:
            self.label_CustomException.setText('Create unique name, cannot already be in use.')
        self.lineEdit_Name.setText('')
        self.lineEdit_UnitPrice.setText('')
        self.lineEdit_QuantityCustom.setText('1')
        self.lineEdit_DoctorCost.setText('')
        self.lineEdit_Minimum.setText('')

    def clear(self) -> None:
        '''
        Method for clearing all items in the item list on the right.
        :return:
        '''
        position = len(list(self.uniqueItems.keys()))
        for i in range(position):
            exec(labelNames[i][0] + '.setText("")')
            exec(labelNames[i][1] + '.setText("")')
            exec(labelNames[i][2] + '.setText("")')
            exec(labelNames[i][3] + '.setText("")')
            exec(labelNames[i][4] + '.setText("")')

        editItemsState = self.pushButton_EditItems.text()
        if editItemsState == 'Done':
            self.editItems()
        self.uniqueItems = {}
        self.calcTotals()

    def editItems(self) -> None:
        '''
        Method to enable and display the buttons needed to edit item quantities.
        :return:
        '''
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
            self.calcTotals()

    def clearItem(self, row: str) -> None:
        '''
        Method for clearing an individual item.
        :param row: Used to determine what row of the item list is being acted upon.
        :return:
        '''
        itemListLength = len(self.uniqueItems.keys())
        item = eval('self.label_ItemList' + str(row) + '_1.text()')
        del self.uniqueItems[item]
        for i in range(int(row), itemListLength):
            for j in range(5):
                exec('updatedText = self.label_ItemList' + str(i + 1) + '_' + str(j + 1) + '.text()')
                exec('self.label_ItemList' + str(i) + '_' + str(j + 1) + '.setText(updatedText)')

        for label in range(5):
            exec('self.label_ItemList' + str(itemListLength) + '_' + str(label + 1) + '.setText("")')

        for button in range(3):
            exec('self.pushButton_ItemList' + str(itemListLength) + '_' + str(button + 1) + '.setText("")')
        self.calcTotals()

    def decreaseItem(self, row: str) -> None:
        '''
        Method for decreasing the total quantity of an individual item.
        :param row: Used to determine what row of the item list is being acted upon.
        :return:
        '''
        item = eval('self.label_ItemList' + str(row) + '_1.text()')
        quantity = eval('int((self.label_ItemList' + str(row) + '_2.text()))')
        if quantity == 1:
            self.clearItem(row)
        else:
            quantity -= 1
            self.uniqueItems[item] = quantity
            exec('self.label_ItemList' + str(row) + '_2.setText(str(quantity))')
        self.calcTotals()

    def increaseItem(self, row: str) -> None:
        '''
        Method for increasing the total quantity of an individual item.
        :param row: Used to determine what row of the item list is being acted upon.
        :return:
        '''
        item = eval('self.label_ItemList' + str(row) + '_1.text()')
        quantity = eval('int((self.label_ItemList' + str(row) + '_2.text()))')
        quantity += 1
        self.uniqueItems[item] = quantity
        exec('self.label_ItemList' + str(row) + '_2.setText(str(quantity))')
        self.calcTotals()

    def calcTotals(self) -> None:
        '''
        Method for calculating and displaying the costs/prices for every item and the totals.
        :return:
        '''
        if len(self.uniqueItems.keys()) == 0:
            self.label_PeeqCostOutput.setText('$0.00')
            self.label_DoctorCostOutput.setText('$0.00')
            self.label_MinimumOutput.setText('$0.00')
        else:
            uCostTotal = 0.00
            dCostTotal = 5.00
            minimumTotal = 0.00
            if self.checkBox_MiscCosts.isChecked():
                uCostTotal += 3.00
                dCostTotal += 3.00
                minimumTotal += 3.00
            if self.checkBox_VisionSource.isChecked():
                dCostTotal -= 5.00
            itemsTotal = list(self.uniqueItems.keys())
            quantitiesTotal = list(self.uniqueItems.values())
            for i in range(len(itemsTotal)):
                index = displayNames.index(itemsTotal[i])
                uCost = float(items[index][1])
                dCost = float(items[index][2])
                minimum = float(items[index][3])
                uCostTotal += uCost
                dCostTotal += dCost
                minimumTotal += minimum
                exec('self.label_ItemList' + str(len(itemsTotal)) + '_3.setText("$" + "%.2f" % uCost)')
                exec('self.label_ItemList' + str(len(itemsTotal)) + '_4.setText("$" + "%.2f" % dCost)')
                exec('self.label_ItemList' + str(len(itemsTotal)) + '_5.setText("$" + "%.2f" % minimum)')
            self.label_PeeqCostOutput.setText('$%.2f' % uCostTotal)
            self.label_DoctorCostOutput.setText('$%.2f' % dCostTotal)
            self.label_MinimumOutput.setText('$%.2f' % minimumTotal)