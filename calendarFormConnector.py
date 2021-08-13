from datetime import datetime
from PyQt5 import QtCore, QtWidgets
import second

def __init__form(self, form, parent=None):
    self.form = form


second.Ui_TimeManager.__init__ = __init__form

def set_limit_calendar(self, mod):
    if mod == 'min':
        self.calendarWidget.setMinimumDate(datetime.strptime(self.form.minTime, '%Y-%m-%d %H:%M:%S'))
        self.calendarWidget.setMaximumDate(datetime.strptime(self.form.maxTime, '%Y-%m-%d %H:%M:%S'))
        self.calendarWidget.setSelectedDate(datetime.strptime(self.form.minTime, '%Y-%m-%d %H:%M:%S'))
        self.timeEdit.setTime(datetime.strptime(self.form.minTime, '%Y-%m-%d %H:%M:%S').time())
    if mod == 'max':
        self.calendarWidget.setMinimumDate(datetime.strptime(self.form.minTime, '%Y-%m-%d %H:%M:%S'))
        self.calendarWidget.setMaximumDate(datetime.strptime(self.form.maxTime, '%Y-%m-%d %H:%M:%S'))
        self.calendarWidget.setSelectedDate(datetime.strptime(self.form.maxTime, '%Y-%m-%d %H:%M:%S'))
        self.timeEdit.setTime(datetime.strptime(self.form.maxTime, '%Y-%m-%d %H:%M:%S').time())


second.Ui_TimeManager.set_limit_calendar = set_limit_calendar

class Ui_TimeManagerController(QtWidgets.QWidget):

    def closeEvent(self, event):
        self.dateEdit.setDateTime(datetime.strptime(f"{str(self.ui.calendarWidget.selectedDate().toPyDate()).split(' ')[0]} {str(self.ui.timeEdit.time().toPyTime())}", '%Y-%m-%d %H:%M:%S'))

    def __init__(self, form, dateEdit, mod, parent=None):
        self.dateEdit = dateEdit
        QtWidgets.QCalendarWidget.__init__(self, parent)
        self.ui = second.Ui_TimeManager(form)
        self.ui.setupUi(self)
        self.ui.set_limit_calendar(mod)
