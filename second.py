# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: C:\Users\acer nitro 5\PycharmProjects\AdaBoostVisualDemo lib\second.py
# Compiled at: 2021-05-10 01:41:02
# Size of source mod 2**32: 1396 bytes
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TimeManager(object):

    def setupUi(self, TimeManager):
        TimeManager.setObjectName('TimeManager')
        TimeManager.resize(470, 371)
        self.calendarWidget = QtWidgets.QCalendarWidget(TimeManager)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 471, 371))
        self.calendarWidget.setObjectName('calendarWidget')
        self.timeEdit = QtWidgets.QTimeEdit(TimeManager)
        self.timeEdit.setGeometry(QtCore.QRect(0, 40, 61, 22))
        self.timeEdit.setObjectName('timeEdit')
        self.retranslateUi(TimeManager)
        QtCore.QMetaObject.connectSlotsByName(TimeManager)

    def retranslateUi(self, TimeManager):
        _translate = QtCore.QCoreApplication.translate
        TimeManager.setWindowTitle(_translate('TimeManager', 'TimeManager'))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TimeManager = QtWidgets.QWidget()
    ui = Ui_TimeManager()
    ui.setupUi(TimeManager)
    TimeManager.show()
    sys.exit(app.exec_())