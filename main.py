# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: C:\Users\acer nitro 5\PycharmProjects\AdaBoostVisualDemo lib\main.py
# Compiled at: 2021-03-24 20:09:18
# Size of source mod 2**32: 205 bytes
from MyWindow import *
from DataReader import *
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec())