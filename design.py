# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 726)
        MainWindow.setMinimumSize(QtCore.QSize(600, 726))
        MainWindow.setMaximumSize(QtCore.QSize(600, 726))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 611, 711))
        self.tabWidget.setMaximumSize(QtCore.QSize(1319, 739))
        self.tabWidget.setObjectName("tabWidget")
        self.tabAnalys_3 = QtWidgets.QWidget()
        self.tabAnalys_3.setObjectName("tabAnalys_3")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tabAnalys_3)
        self.textBrowser_3.setGeometry(QtCore.QRect(0, 0, 591, 111))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.frame_19 = QtWidgets.QFrame(self.tabAnalys_3)
        self.frame_19.setGeometry(QtCore.QRect(0, 110, 771, 569))
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.labelDefects_3 = QtWidgets.QLabel(self.frame_19)
        self.labelDefects_3.setGeometry(QtCore.QRect(10, 30, 55, 16))
        self.labelDefects_3.setObjectName("labelDefects_3")
        self.comboBoxDefects_3 = QtWidgets.QComboBox(self.frame_19)
        self.comboBoxDefects_3.setGeometry(QtCore.QRect(70, 30, 501, 22))
        self.comboBoxDefects_3.setObjectName("comboBoxDefects_3")
        self.labelOutput_5 = QtWidgets.QLabel(self.frame_19)
        self.labelOutput_5.setGeometry(QtCore.QRect(0, 90, 55, 16))
        self.labelOutput_5.setObjectName("labelOutput_5")
        self.frame_20 = QtWidgets.QFrame(self.frame_19)
        self.frame_20.setGeometry(QtCore.QRect(0, 120, 601, 191))
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.labelUnit1_3 = QtWidgets.QLabel(self.frame_20)
        self.labelUnit1_3.setGeometry(QtCore.QRect(490, 70, 55, 21))
        self.labelUnit1_3.setObjectName("labelUnit1_3")
        self.labelIntervalParam2_3 = QtWidgets.QLabel(self.frame_20)
        self.labelIntervalParam2_3.setGeometry(QtCore.QRect(360, 110, 91, 20))
        self.labelIntervalParam2_3.setObjectName("labelIntervalParam2_3")
        self.spinBoxParam1_3 = QtWidgets.QSpinBox(self.frame_20)
        self.spinBoxParam1_3.setGeometry(QtCore.QRect(270, 60, 61, 31))
        self.spinBoxParam1_3.setObjectName("spinBoxParam1_3")
        self.labelUnit2_3 = QtWidgets.QLabel(self.frame_20)
        self.labelUnit2_3.setGeometry(QtCore.QRect(490, 110, 55, 21))
        self.labelUnit2_3.setObjectName("labelUnit2_3")
        self.labelParam1_3 = QtWidgets.QLabel(self.frame_20)
        self.labelParam1_3.setGeometry(QtCore.QRect(10, 60, 251, 31))
        self.labelParam1_3.setObjectName("labelParam1_3")
        self.labelIntervalParam1_3 = QtWidgets.QLabel(self.frame_20)
        self.labelIntervalParam1_3.setGeometry(QtCore.QRect(360, 70, 91, 21))
        self.labelIntervalParam1_3.setObjectName("labelIntervalParam1_3")
        self.spinBoxParam2_3 = QtWidgets.QSpinBox(self.frame_20)
        self.spinBoxParam2_3.setGeometry(QtCore.QRect(270, 100, 61, 31))
        self.spinBoxParam2_3.setMinimum(0)
        self.spinBoxParam2_3.setObjectName("spinBoxParam2_3")
        self.labelParam2_3 = QtWidgets.QLabel(self.frame_20)
        self.labelParam2_3.setGeometry(QtCore.QRect(10, 95, 251, 41))
        self.labelParam2_3.setObjectName("labelParam2_3")
        self.comboBoxPairParams_3 = QtWidgets.QComboBox(self.frame_20)
        self.comboBoxPairParams_3.setGeometry(QtCore.QRect(70, 10, 361, 22))
        self.comboBoxPairParams_3.setObjectName("comboBoxPairParams_3")
        self.labelPairParams_3 = QtWidgets.QLabel(self.frame_20)
        self.labelPairParams_3.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.labelPairParams_3.setObjectName("labelPairParams_3")
        self.labelOutput_6 = QtWidgets.QLabel(self.frame_20)
        self.labelOutput_6.setGeometry(QtCore.QRect(0, 170, 111, 16))
        self.labelOutput_6.setObjectName("labelOutput_6")
        self.setParamsButton = QtWidgets.QPushButton(self.frame_20)
        self.setParamsButton.setGeometry(QtCore.QRect(470, 10, 93, 28))
        self.setParamsButton.setObjectName("setParamsButton")
        self.FitButton_3 = QtWidgets.QPushButton(self.frame_19)
        self.FitButton_3.setGeometry(QtCore.QRect(30, 340, 93, 28))
        self.FitButton_3.setObjectName("FitButton_3")
        self.label_31 = QtWidgets.QLabel(self.frame_19)
        self.label_31.setGeometry(QtCore.QRect(520, 510, 81, 20))
        self.label_31.setObjectName("label_31")
        self.LoadButton_3 = QtWidgets.QPushButton(self.frame_19)
        self.LoadButton_3.setGeometry(QtCore.QRect(30, 490, 93, 28))
        self.LoadButton_3.setObjectName("LoadButton_3")
        self.saveModelButton_3 = QtWidgets.QPushButton(self.frame_19)
        self.saveModelButton_3.setGeometry(QtCore.QRect(140, 490, 93, 28))
        self.saveModelButton_3.setObjectName("saveModelButton_3")
        self.Plot3d_3 = QtWidgets.QPushButton(self.frame_19)
        self.Plot3d_3.setGeometry(QtCore.QRect(30, 440, 93, 28))
        self.Plot3d_3.setObjectName("Plot3d_3")
        self.saveDataButton_3 = QtWidgets.QPushButton(self.frame_19)
        self.saveDataButton_3.setGeometry(QtCore.QRect(250, 490, 93, 28))
        self.saveDataButton_3.setObjectName("saveDataButton_3")
        self.predictButton_3 = QtWidgets.QPushButton(self.frame_19)
        self.predictButton_3.setGeometry(QtCore.QRect(30, 390, 93, 28))
        self.predictButton_3.setObjectName("predictButton_3")
        self.progressBar_3 = QtWidgets.QProgressBar(self.frame_19)
        self.progressBar_3.setGeometry(QtCore.QRect(30, 542, 541, 21))
        self.progressBar_3.setProperty("value", 24)
        self.progressBar_3.setObjectName("progressBar_3")
        self.frame_21 = QtWidgets.QFrame(self.frame_19)
        self.frame_21.setGeometry(QtCore.QRect(300, 320, 299, 131))
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.labelEnumerator_3 = QtWidgets.QLabel(self.frame_21)
        self.labelEnumerator_3.setGeometry(QtCore.QRect(120, 50, 121, 20))
        self.labelEnumerator_3.setObjectName("labelEnumerator_3")
        self.spinBoxEmumerator_3 = QtWidgets.QSpinBox(self.frame_21)
        self.spinBoxEmumerator_3.setGeometry(QtCore.QRect(240, 50, 51, 22))
        self.spinBoxEmumerator_3.setMinimum(10)
        self.spinBoxEmumerator_3.setMaximum(1000)
        self.spinBoxEmumerator_3.setObjectName("spinBoxEmumerator_3")
        self.labelSize_3 = QtWidgets.QLabel(self.frame_21)
        self.labelSize_3.setGeometry(QtCore.QRect(170, 10, 71, 16))
        self.labelSize_3.setObjectName("labelSize_3")
        self.spinBoxSize_3 = QtWidgets.QSpinBox(self.frame_21)
        self.spinBoxSize_3.setGeometry(QtCore.QRect(240, 10, 51, 22))
        self.spinBoxSize_3.setMinimum(4)
        self.spinBoxSize_3.setMaximum(100)
        self.spinBoxSize_3.setObjectName("spinBoxSize_3")
        self.lableEstimating_3 = QtWidgets.QLabel(self.frame_21)
        self.lableEstimating_3.setGeometry(QtCore.QRect(170, 90, 131, 16))
        self.lableEstimating_3.setObjectName("lableEstimating_3")
        self.testModelButton = QtWidgets.QPushButton(self.frame_19)
        self.testModelButton.setGeometry(QtCore.QRect(370, 490, 93, 28))
        self.testModelButton.setObjectName("testModelButton")
        self.loadModelButton_4 = QtWidgets.QPushButton(self.frame_19)
        self.loadModelButton_4.setGeometry(QtCore.QRect(140, 440, 93, 28))
        self.loadModelButton_4.setObjectName("loadModelButton_4")
        self.tabWidget.addTab(self.tabAnalys_3, "")
        self.tabSettings_3 = QtWidgets.QWidget()
        self.tabSettings_3.setObjectName("tabSettings_3")
        self.frame_25 = QtWidgets.QFrame(self.tabSettings_3)
        self.frame_25.setGeometry(QtCore.QRect(0, 380, 1111, 301))
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.lineEditUnitNameExcelPath_3 = QtWidgets.QLineEdit(self.frame_25)
        self.lineEditUnitNameExcelPath_3.setGeometry(QtCore.QRect(10, 190, 131, 31))
        self.lineEditUnitNameExcelPath_3.setObjectName("lineEditUnitNameExcelPath_3")
        self.lineEditDelaysExcelPath_3 = QtWidgets.QLineEdit(self.frame_25)
        self.lineEditDelaysExcelPath_3.setGeometry(QtCore.QRect(10, 130, 131, 31))
        self.lineEditDelaysExcelPath_3.setObjectName("lineEditDelaysExcelPath_3")
        self.label_40 = QtWidgets.QLabel(self.frame_25)
        self.label_40.setGeometry(QtCore.QRect(150, 130, 451, 31))
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.frame_25)
        self.label_41.setGeometry(QtCore.QRect(150, 190, 451, 31))
        self.label_41.setObjectName("label_41")
        self.lineEditRelationsPath = QtWidgets.QLineEdit(self.frame_25)
        self.lineEditRelationsPath.setGeometry(QtCore.QRect(10, 250, 131, 31))
        self.lineEditRelationsPath.setObjectName("lineEditRelationsPath")
        self.label_43 = QtWidgets.QLabel(self.frame_25)
        self.label_43.setGeometry(QtCore.QRect(150, 250, 451, 31))
        self.label_43.setObjectName("label_43")
        self.tabWidget.addTab(self.tabSettings_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSetParams = QtWidgets.QAction(MainWindow)
        self.actionSetParams.setObjectName("actionSetParams")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelDefects_3.setText(_translate("MainWindow", "Defects"))
        self.labelOutput_5.setText(_translate("MainWindow", "Output"))
        self.labelUnit1_3.setText(_translate("MainWindow", "Unit1"))
        self.labelIntervalParam2_3.setText(_translate("MainWindow", "IntervalParam2"))
        self.labelUnit2_3.setText(_translate("MainWindow", "Unit2"))
        self.labelParam1_3.setText(_translate("MainWindow", "Param1"))
        self.labelIntervalParam1_3.setText(_translate("MainWindow", "IntervalParam1"))
        self.labelParam2_3.setText(_translate("MainWindow", "Param2"))
        self.labelPairParams_3.setText(_translate("MainWindow", "Params"))
        self.labelOutput_6.setText(_translate("MainWindow", "Control Action"))
        self.setParamsButton.setText(_translate("MainWindow", "SetParams"))
        self.FitButton_3.setText(_translate("MainWindow", "Fit Model"))
        self.label_31.setText(_translate("MainWindow", "ControlPanel"))
        self.LoadButton_3.setText(_translate("MainWindow", "Load Data"))
        self.saveModelButton_3.setText(_translate("MainWindow", "Save Model"))
        self.Plot3d_3.setText(_translate("MainWindow", "Plot 3d"))
        self.saveDataButton_3.setText(_translate("MainWindow", "Save Data"))
        self.predictButton_3.setText(_translate("MainWindow", "Score"))
        self.labelEnumerator_3.setText(_translate("MainWindow", "countEnumerators"))
        self.labelSize_3.setText(_translate("MainWindow", "resolution"))
        self.lableEstimating_3.setText(_translate("MainWindow", "Estimating indicators"))
        self.testModelButton.setText(_translate("MainWindow", "Compare"))
        self.loadModelButton_4.setText(_translate("MainWindow", "Load Model"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAnalys_3), _translate("MainWindow", "Analys"))
        self.lineEditUnitNameExcelPath_3.setText(_translate("MainWindow", "UnitNameParams.ods"))
        self.lineEditDelaysExcelPath_3.setText(_translate("MainWindow", "delays.ods"))
        self.label_40.setText(_translate("MainWindow", "Путь к файлу с данными о запаздывании сигналов."))
        self.label_41.setText(_translate("MainWindow", "Путь к файлу с данными о наименовании параметров и ед.изм."))
        self.lineEditRelationsPath.setText(_translate("MainWindow", "relations.ods"))
        self.label_43.setText(_translate("MainWindow", "Путь к файлу с данными о зависимостях дефектов от параметров."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings_3), _translate("MainWindow", "Settings"))
        self.actionSetParams.setText(_translate("MainWindow", "SetParams"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())