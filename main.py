from MyWindow import *
from DataReader import *
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec())
