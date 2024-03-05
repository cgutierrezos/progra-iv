# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WIN_Product.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from datetime import date
from enum import Enum
from typing import cast
from PyQt5 import QtCore, QtGui, QtWidgets

from src.app.model.product.ProductModel import ANIMAL_TYPE, ANIMAL_TYPE_DICT, ProductModel, ProductNoneModel, ProductAntibioticModel, ProductFertilizerControlModel, ProductPlagueControlModel, PRODUCT_TYPE
from src.app.model.product.ProductModelCollection import ProductModelCollection

INDEX_ANIMAL_TYPE_DICT: dict[str, int] = {ANIMAL_TYPE.Bovino.name: 0, ANIMAL_TYPE.Caprino.name: 1, ANIMAL_TYPE.Porcino.name: 2}

class WIN_Product(QtWidgets.QMainWindow):

    onProductNew = QtCore.pyqtSignal()
    onProductCreate = QtCore.pyqtSignal(ProductModel)
    onProductUpdate = QtCore.pyqtSignal(ProductModel)
    onProductDelete = QtCore.pyqtSignal(ProductModel)
    onProductSelect = QtCore.pyqtSignal(int)

    state = Enum("state", ["init", "inSelection", "inEdition", "inCreation"])

    def __init__(self, parent: QtWidgets.QMainWindow) -> None:
        super().__init__(parent)
    
        self.products = ProductModelCollection()
        self.productSelected: ProductModel = ProductNoneModel()
        WIN_Product.state = WIN_Product.state.init

        self._setupUi()

    def selectProduct(self, productSelected: ProductModel):        
        self.productSelected = productSelected
        self._setToSelectState()

    def editProduct(self, productSelected: ProductModel):
        self.productSelected = productSelected
        self._setToEditState()

    def refreshProducts(self, products: ProductModelCollection):
        self.products = products
        self._displayProductsTable()
        self._setToInitialState()


    def connectEvents(self):

        self.BTN_New.clicked.connect(self._emitNewProduct)
        self.BTN_Edit.clicked.connect(self._emitEditProduct)
        self.BTN_Save.clicked.connect(self._emitSaveProduct)
        self.BTN_Delete.clicked.connect(self._emitDeleteProduct)
        self.BTN_Cancel.clicked.connect(self._emitCancel)

        self.tableView.clicked.connect(self._emitProductSelect)


    def _setupUi(self):
        self.setObjectName("self")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 210, 771, 341))
        self.tableView.setObjectName("tableView")
        self.tableModel = QtGui.QStandardItemModel()
        self.tableView.setModel(self.tableModel)
       
        self.BTN_New = QtWidgets.QPushButton(self.centralwidget)
        self.BTN_New.setGeometry(QtCore.QRect(10, 170, 93, 28))
        self.BTN_New.setObjectName("BTN_New")
        self.BTN_Edit = QtWidgets.QPushButton(self.centralwidget)
        self.BTN_Edit.setGeometry(QtCore.QRect(120, 170, 93, 28))
        self.BTN_Edit.setObjectName("BTN_Edit")
        self.BTN_Delete = QtWidgets.QPushButton(self.centralwidget)
        self.BTN_Delete.setGeometry(QtCore.QRect(230, 170, 93, 28))
        self.BTN_Delete.setObjectName("BTN_Delete")
        self.BTN_Save = QtWidgets.QPushButton(self.centralwidget)
        self.BTN_Save.setGeometry(QtCore.QRect(340, 170, 93, 28))
        self.BTN_Save.setObjectName("BTN_Save")
        self.BTN_Cancel = QtWidgets.QPushButton(self.centralwidget)
        self.BTN_Cancel.setGeometry(QtCore.QRect(450, 170, 93, 28))
        self.BTN_Cancel.setObjectName("BTN_Cancel")
       
        # self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(10, 170, 93, 28))
        # self.pushButton.setObjectName("pushButton")
        # self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton_2.setGeometry(QtCore.QRect(120, 170, 93, 28))
        # self.pushButton_2.setObjectName("pushButton_2")
        self.EDT_ICA = QtWidgets.QLineEdit(self.centralwidget)
        self.EDT_ICA.setGeometry(QtCore.QRect(80, 30, 261, 22))
        self.EDT_ICA.setObjectName("EDT_ICA")
        self.EDT_Name = QtWidgets.QLineEdit(self.centralwidget)
        self.EDT_Name.setGeometry(QtCore.QRect(470, 30, 261, 22))
        self.EDT_Name.setObjectName("EDT_Name")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 30, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 60, 55, 16))
        self.label_4.setObjectName("label_4")
        self.EDT_Frecuency = QtWidgets.QSpinBox(self.centralwidget)
        self.EDT_Frecuency.setGeometry(QtCore.QRect(80, 60, 261, 22))
        self.EDT_Frecuency.setObjectName("EDT_Frecuency")
        self.EDT_Price = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.EDT_Price.setGeometry(QtCore.QRect(470, 60, 261, 22))
        self.EDT_Price.setObjectName("EDT_Price")
        self.TAB_ProductType = QtWidgets.QTabWidget(self.centralwidget)
        self.TAB_ProductType.setGeometry(QtCore.QRect(10, 90, 721, 71))
        self.TAB_ProductType.setObjectName("TAB_ProductType")
        self.tab_ControlPlagas = QtWidgets.QWidget()
        self.tab_ControlPlagas.setObjectName("tab_ControlPlagas")
        self.label_6 = QtWidgets.QLabel(self.tab_ControlPlagas)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_6.setObjectName("label_6")
        self.EDT_GracePeriod = QtWidgets.QSpinBox(self.tab_ControlPlagas)
        self.EDT_GracePeriod.setGeometry(QtCore.QRect(150, 10, 261, 22))
        self.EDT_GracePeriod.setObjectName("EDT_GracePeriod")
        self.TAB_ProductType.addTab(self.tab_ControlPlagas, "")
        self.tab_ControlFertilizante = QtWidgets.QWidget()
        self.tab_ControlFertilizante.setObjectName("tab_ControlFertilizante")
        self.label_8 = QtWidgets.QLabel(self.tab_ControlFertilizante)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label_8.setObjectName("label_8")
        self.EDT_LastApplication = QtWidgets.QDateEdit(self.tab_ControlFertilizante)
        self.EDT_LastApplication.setGeometry(QtCore.QRect(170, 10, 261, 22))
        self.EDT_LastApplication.setObjectName("EDT_LastApplication")
        self.TAB_ProductType.addTab(self.tab_ControlFertilizante, "")
        self.TAB_Antibiotic = QtWidgets.QWidget()
        self.TAB_Antibiotic.setObjectName("TAB_Antibiotic")
        self.label_7 = QtWidgets.QLabel(self.TAB_Antibiotic)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.TAB_Antibiotic)
        self.label_9.setGeometry(QtCore.QRect(370, 10, 71, 16))
        self.label_9.setObjectName("label_9")
        self.CBOX_ANIMAL = QtWidgets.QComboBox(self.TAB_Antibiotic)
        self.CBOX_ANIMAL.setGeometry(QtCore.QRect(450, 10, 241, 22))
        self.CBOX_ANIMAL.setObjectName("CBOX_ANIMAL")
        self.CBOX_ANIMAL.addItem("")
        self.CBOX_ANIMAL.addItem("")
        self.CBOX_ANIMAL.addItem("")
        self.EDT_Dose = QtWidgets.QSlider(self.TAB_Antibiotic)
        self.EDT_Dose.setGeometry(QtCore.QRect(80, 10, 201, 22))
        self.EDT_Dose.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.EDT_Dose.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.EDT_Dose.setMinimum(400)
        self.EDT_Dose.setMaximum(600)
        self.EDT_Dose.setPageStep(50)
        self.EDT_Dose.setObjectName("EDT_Dose")
        self.TAB_ProductType.addTab(self.TAB_Antibiotic, "")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.TAB_ProductType.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("WIN_Product", "Productos"))
        self.BTN_New.setText(_translate("WIN_Product", "Nuevo"))
        self.BTN_Edit.setText(_translate("WIN_Product", "Editar"))
        self.BTN_Save.setText(_translate("WIN_Product", "Guardar"))
        self.BTN_Delete.setText(_translate("WIN_Product", "Eliminar"))
        self.BTN_Cancel.setText(_translate("WIN_Product", "Cancelar"))
        self.label.setText(_translate("WIN_Product", "ICA"))
        self.label_2.setText(_translate("WIN_Product", "Nombre"))
        self.label_3.setText(_translate("WIN_Product", "Frecuencia"))
        self.label_4.setText(_translate("WIN_Product", "Precio"))
        self.label_6.setText(_translate("WIN_Product", "Periodo Carencia"))
        self.TAB_ProductType.setTabText(self.TAB_ProductType.indexOf(self.tab_ControlPlagas), _translate("WIN_Product", "Control Plagas"))
        self.label_8.setText(_translate("WIN_Product", "Fecha Ultima Aplicacion"))
        self.TAB_ProductType.setTabText(self.TAB_ProductType.indexOf(self.tab_ControlFertilizante), _translate("WIN_Product", "Control Fertilizante"))
        self.label_7.setText(_translate("WIN_Product", "dosis"))
        self.label_9.setText(_translate("WIN_Product", "tipo animal"))

      
        self.CBOX_ANIMAL.setItemText(INDEX_ANIMAL_TYPE_DICT[ANIMAL_TYPE.Bovino.name], _translate("WIN_Product", ANIMAL_TYPE.Bovino.name))
        self.CBOX_ANIMAL.setItemText(INDEX_ANIMAL_TYPE_DICT[ANIMAL_TYPE.Caprino.name], _translate("WIN_Product", ANIMAL_TYPE.Caprino.name))
        self.CBOX_ANIMAL.setItemText(INDEX_ANIMAL_TYPE_DICT[ANIMAL_TYPE.Porcino.name], _translate("WIN_Product", ANIMAL_TYPE.Porcino.name))
        self.TAB_ProductType.setTabText(self.TAB_ProductType.indexOf(self.TAB_Antibiotic), _translate("WIN_Product", "Antibiotico"))

    def _displayProductsTable(self):
        self.tableModel.setRowCount(self.products.count()) 

        self.tableModel.setColumnCount(5)
        self.tableModel.setHorizontalHeaderLabels(["ICA", "Nombre", "Frecuencia", "Precio", "Tipo"])

        row = 0

        def productsCb(product: ProductModel):
            nonlocal row
            
            icaItem = QtGui.QStandardItem(product.ica)
            icaItem.setEditable(False)
            self.tableModel.setItem(row, 0, icaItem)

            nameItem = QtGui.QStandardItem(product.name)
            nameItem.setEditable(False)
            self.tableModel.setItem(row, 1, nameItem)

            frecuencyItem = QtGui.QStandardItem(str(product.frecuency))
            frecuencyItem.setEditable(False)
            self.tableModel.setItem(row, 2, frecuencyItem)

            priceItem = QtGui.QStandardItem(str(product.price))
            priceItem.setEditable(False)
            self.tableModel.setItem(row, 3, priceItem)

            typeItem = QtGui.QStandardItem(product.type.name)
            typeItem.setEditable(False)
            self.tableModel.setItem(row, 4, typeItem)

            row += 1

        self.products.forEach(productsCb)

    def _emitProductSelect(self, index: QtCore.QModelIndex):
        self.onProductSelect.emit(index.row())

    def _emitNewProduct(self):
        self._setToNewProductState()

    def _emitEditProduct(self):
        self._setToEditState()

    def _emitSaveProduct(self):
        
        selectedIndex = self.TAB_ProductType.currentIndex()
        
        if WIN_Product.state == WIN_Product.state.inCreation:
            product: ProductModel

            # plaga
            if selectedIndex == 0:
                product = ProductPlagueControlModel()
                product.name = self.EDT_Name.text()
                product.ica = self.EDT_ICA.text()
                product.frecuency = self.EDT_Frecuency.value()
                product.price = self.EDT_Price.value()
                product.type = PRODUCT_TYPE.PlageControl
                product.gracePeriod = self.EDT_GracePeriod.value()
            
            #fertilizante
            if selectedIndex == 1:
                product = ProductFertilizerControlModel()
                product.name = self.EDT_Name.text()
                product.ica = self.EDT_ICA.text()
                product.frecuency = self.EDT_Frecuency.value()
                product.price = self.EDT_Price.value()
                product.type = PRODUCT_TYPE.FertilizerControl
                product.lastApplicationDate = self.EDT_LastApplication.date().toPyDate()
            
            #antibiotic
            if selectedIndex == 2:
                product = ProductAntibioticModel()
                product.name = self.EDT_Name.text()
                product.ica = self.EDT_ICA.text()
                product.frecuency = self.EDT_Frecuency.value()
                product.price = self.EDT_Price.value()
                product.type = PRODUCT_TYPE.Antibiotic
                product.dose = self.EDT_Dose.value()
                product.animalType = ANIMAL_TYPE_DICT[self.CBOX_ANIMAL.currentText()]
 
        
         
            self.onProductCreate.emit(product)
            return

        # plaga
        if selectedIndex == 0:
            self.productSelected = cast(ProductPlagueControlModel, self.productSelected)
            self.productSelected.name = self.EDT_Name.text()
            self.productSelected.ica = self.EDT_ICA.text()
            self.productSelected.frecuency = self.EDT_Frecuency.value()
            self.productSelected.price = self.EDT_Price.value()
            self.productSelected.type = PRODUCT_TYPE.PlageControl
            self.productSelected.gracePeriod = self.EDT_GracePeriod.value()
        
        #fertilizante
        if selectedIndex == 1:
            self.productSelected = cast(ProductFertilizerControlModel, self.productSelected)
            self.productSelected.name = self.EDT_Name.text()
            self.productSelected.ica = self.EDT_ICA.text()
            self.productSelected.frecuency = self.EDT_Frecuency.value()
            self.productSelected.price = self.EDT_Price.value()
            self.productSelected.type = PRODUCT_TYPE.FertilizerControl
            self.productSelected.lastApplicationDate = self.EDT_LastApplication.date().toPyDate()
        
        #antibiotic
        if selectedIndex == 2:
            self.productSelected = cast(ProductAntibioticModel, self.productSelected)
            self.productSelected.name = self.EDT_Name.text()
            self.productSelected.ica = self.EDT_ICA.text()
            self.productSelected.frecuency = self.EDT_Frecuency.value()
            self.productSelected.price = self.EDT_Price.value()
            self.productSelected.type = PRODUCT_TYPE.Antibiotic
            self.productSelected.dose = self.EDT_Dose.value()
            self.productSelected.animalType = ANIMAL_TYPE_DICT[self.CBOX_ANIMAL.currentText()]

        self.onProductUpdate.emit(self.productSelected)


    def _emitDeleteProduct(self):
        self.onProductDelete.emit(self.productSelected)
    
    def _emitCancel(self): 
        self._setToInitialState()



    def _setToInitialState(self):

        self.tableView.setEnabled(True)

        self.BTN_New.setEnabled(True)
        self.BTN_Edit.setEnabled(False)
        self.BTN_Save.setEnabled(False)
        self.BTN_Delete.setEnabled(False)
        self.BTN_Cancel.setEnabled(False)
        
        self.EDT_ICA.setReadOnly(True)
        self.EDT_ICA.setText("")

        self.EDT_Name.setReadOnly(True)
        self.EDT_Name.setText("")

        self.EDT_Frecuency.setReadOnly(True)
        self.EDT_Frecuency.setValue(0)
        

        self.EDT_Price.setReadOnly(True)
        self.EDT_Price.setValue(0)

        self.EDT_GracePeriod.setReadOnly(True)
        self.EDT_GracePeriod.setValue(0)

        self.EDT_LastApplication.setReadOnly(True)
        self.EDT_LastApplication.setDate(date.today())
        
        self.EDT_Dose.setEnabled(False)
        self.EDT_Dose.setValue(0)

        self.CBOX_ANIMAL.setEnabled(False)
        self.CBOX_ANIMAL.setCurrentIndex(INDEX_ANIMAL_TYPE_DICT[ANIMAL_TYPE.Bovino.name])

        self.TAB_ProductType.setCurrentIndex(0)
        self.TAB_ProductType.setTabEnabled(0, True)
        self.TAB_ProductType.setTabEnabled(1, True)
        self.TAB_ProductType.setTabEnabled(2, True)

        WIN_Product.state = WIN_Product.state.init
        

    def _setToNewProductState(self):

        self.tableView.setEnabled(False)

        self.BTN_New.setEnabled(False)
        self.BTN_Edit.setEnabled(False)
        self.BTN_Save.setEnabled(True)
        self.BTN_Delete.setEnabled(False)
        self.BTN_Cancel.setEnabled(True)

        
        self.EDT_ICA.setReadOnly(False)
        self.EDT_ICA.setText("")

        self.EDT_Name.setReadOnly(False)
        self.EDT_Name.setText("")

        self.EDT_Frecuency.setReadOnly(False)
        self.EDT_Frecuency.setValue(0)

        self.EDT_Price.setReadOnly(False)
        self.EDT_Price.setValue(0)

        self.EDT_GracePeriod.setReadOnly(False)
        self.EDT_GracePeriod.setValue(0)

        self.EDT_LastApplication.setReadOnly(False)
        self.EDT_LastApplication.setDate(date.today())

        self.EDT_Dose.setEnabled(True)
        self.EDT_Dose.setValue(0)

        self.CBOX_ANIMAL.setEnabled(True)
        self.CBOX_ANIMAL.setCurrentIndex(INDEX_ANIMAL_TYPE_DICT[ANIMAL_TYPE.Bovino.name])


        self.TAB_ProductType.setCurrentIndex(0)
        self.TAB_ProductType.setTabEnabled(0, True)
        self.TAB_ProductType.setTabEnabled(1, True)
        self.TAB_ProductType.setTabEnabled(2, True)
        

        self.EDT_ICA.setFocus()

        WIN_Product.state = WIN_Product.state.inCreation

    def _setToEditState(self):

        self.tableView.setEnabled(False)

        self.BTN_New.setEnabled(False)
        self.BTN_Edit.setEnabled(False)
        self.BTN_Save.setEnabled(True)
        self.BTN_Delete.setEnabled(False)
        self.BTN_Cancel.setEnabled(True)

        self.EDT_ICA.setReadOnly(False)
        self.EDT_ICA.setText(self.productSelected.ica)

        self.EDT_Name.setReadOnly(False)
        self.EDT_Name.setText(self.productSelected.name)

        self.EDT_Frecuency.setReadOnly(False)
        self.EDT_Frecuency.setValue(self.productSelected.frecuency)

        self.EDT_Price.setReadOnly(False)
        self.EDT_Price.setValue(self.productSelected.price)


        if self.productSelected.type == PRODUCT_TYPE.PlageControl:
            self.productSelected = cast(ProductPlagueControlModel, self.productSelected)
            self.TAB_ProductType.setCurrentIndex(0)
            self.TAB_ProductType.setTabEnabled(0, True)
            self.TAB_ProductType.setTabEnabled(1, False)
            self.TAB_ProductType.setTabEnabled(2, False)
            self.EDT_GracePeriod.setReadOnly(False)
            self.EDT_GracePeriod.setValue(self.productSelected.gracePeriod)
 

        if self.productSelected.type == PRODUCT_TYPE.FertilizerControl:
            self.productSelected = cast(ProductFertilizerControlModel, self.productSelected)
            self.TAB_ProductType.setCurrentIndex(1)
            self.TAB_ProductType.setTabEnabled(0, False)
            self.TAB_ProductType.setTabEnabled(1, True)
            self.TAB_ProductType.setTabEnabled(2, False)
            self.EDT_LastApplication.setReadOnly(False)
            self.EDT_LastApplication.setDate(self.productSelected.lastApplicationDate)

        if self.productSelected.type == PRODUCT_TYPE.Antibiotic:
            self.productSelected = cast(ProductAntibioticModel, self.productSelected)
            self.TAB_ProductType.setCurrentIndex(2)
            self.TAB_ProductType.setTabEnabled(1, False)
            self.TAB_ProductType.setTabEnabled(0, False)
            self.TAB_ProductType.setTabEnabled(2, True)
            self.EDT_Dose.setEnabled(True)
            self.EDT_Dose.setValue(self.productSelected.dose)
            self.CBOX_ANIMAL.setEnabled(True)
            self.CBOX_ANIMAL.setCurrentIndex(INDEX_ANIMAL_TYPE_DICT[self.productSelected.animalType.name])
        

        self.EDT_ICA.setFocus()

        WIN_Product.state = WIN_Product.state.inEdition
    
    def _setToSelectState(self):
        
        self.BTN_New.setEnabled(True)
        self.BTN_Edit.setEnabled(True)
        self.BTN_Save.setEnabled(False)
        self.BTN_Delete.setEnabled(True)
        self.BTN_Cancel.setEnabled(False)

        self.EDT_ICA.setReadOnly(True)
        self.EDT_ICA.setText(self.productSelected.ica)

        self.EDT_Name.setReadOnly(True)
        self.EDT_Name.setText(self.productSelected.name)

        self.EDT_Frecuency.setReadOnly(True)
        self.EDT_Frecuency.setValue(self.productSelected.frecuency)

        self.EDT_Price.setReadOnly(True)
        self.EDT_Price.setValue(self.productSelected.price)


        if self.productSelected.type == PRODUCT_TYPE.PlageControl:
            self.productSelected = cast(ProductPlagueControlModel, self.productSelected)
            self.TAB_ProductType.setCurrentIndex(0)
            self.TAB_ProductType.setTabEnabled(0, True)
            self.TAB_ProductType.setTabEnabled(1, False)
            self.TAB_ProductType.setTabEnabled(2, False)
            self.EDT_GracePeriod.setReadOnly(True)
            self.EDT_GracePeriod.setValue(self.productSelected.gracePeriod)

        if self.productSelected.type == PRODUCT_TYPE.FertilizerControl:
            self.productSelected = cast(ProductFertilizerControlModel, self.productSelected)
            self.TAB_ProductType.setCurrentIndex(1)
            self.TAB_ProductType.setTabEnabled(0, False)
            self.TAB_ProductType.setTabEnabled(1, True)
            self.TAB_ProductType.setTabEnabled(2, False)
            self.EDT_LastApplication.setReadOnly(True)
            self.EDT_LastApplication.setDate(self.productSelected.lastApplicationDate)

        if self.productSelected.type == PRODUCT_TYPE.Antibiotic:
            self.productSelected = cast(ProductAntibioticModel, self.productSelected)
            self.TAB_ProductType.setCurrentIndex(2)
            self.TAB_ProductType.setTabEnabled(1, False)
            self.TAB_ProductType.setTabEnabled(0, False)
            self.TAB_ProductType.setTabEnabled(2, True)
            self.EDT_Dose.setEnabled(False)
            self.EDT_Dose.setValue(self.productSelected.dose)
            self.CBOX_ANIMAL.setEnabled(False)
            self.CBOX_ANIMAL.setCurrentIndex(INDEX_ANIMAL_TYPE_DICT[self.productSelected.animalType.name])

        WIN_Product.state = WIN_Product.state.inSelection