from design import *
from DataProcess import *
from File import *
import pandas
from PyQt5.QtWidgets import QFileDialog
import numpy as np
import threading
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt


# запуск функции в отдельном потоке для корректной работы интерфейса
def thread(my_func):
    def wrapper(*args):
        my_thread = threading.Thread(target=my_func, args=args)
        my_thread.start()

    return wrapper


class MyWin(QtWidgets.QMainWindow):
    signal_progress_bar = QtCore.pyqtSignal(int, name='signal_progress_bar')  # сигнал для обновления progress bar
    signal_graph = QtCore.pyqtSignal(list, name='signal_graph')  # сигнал для отрисовки графика
    signal_text = QtCore.pyqtSignal(str, name='signal_text')  # сигнал для вывода текста

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.defects = []  # список дефектов
        self.params = []  # список входных параметров и управляющих воздействий
        self.name_unit = {}  # данные по названию и единицам измерения
        self.relations = {}  # данные по зависимости дефекта от воздействий
        self.excel_data_df = {}  # датафрейм из файла excel
        self.delay = {}  # данные по задержкам
        self.x = []  # данные, подготовленные для обучения модели
        self.y = {}  # качественные показатели по каждому из дефектов
        self.adaboost = 0  # сама модель адаптивного бустинга
        self.proc = DataProcess()  # класс для обработки данных
        self.file = File(self.ui)  # класс для работы с файлами

        # подключение кнопок и сигналов
        self.ui.LoadButton_3.clicked.connect(self.load_data)
        self.ui.FitButton_3.clicked.connect(lambda: self.fit_model(self.signal_progress_bar))
        self.ui.predictButton_3.clicked.connect(lambda: self.score(self.signal_progress_bar, self.signal_text))
        self.ui.Plot3d_3.clicked.connect(lambda: self.plot3d(self.signal_graph, self.signal_progress_bar))
        self.ui.saveModelButton_3.clicked.connect(self.save_model)
        self.ui.loadModelButton_4.clicked.connect(self.load_model)
        self.ui.testModelButton.clicked.connect(lambda: self.test_model(self.signal_progress_bar, self.signal_text))
        self.signal_progress_bar.connect(self.SignalHandlerUpdateProgBar, QtCore.Qt.QueuedConnection)
        self.signal_graph.connect(self.SignalHandlerUpdateGraph, QtCore.Qt.QueuedConnection)
        self.signal_text.connect(self.signalHandlerTextBrowserUpdate, QtCore.Qt.QueuedConnection)
        self.ui.setParamsButton.clicked.connect(self.set_parametrs)
        self.ui.saveDataButton_3.clicked.connect(self.save_data)
        self.ui.comboBoxDefects_3.currentTextChanged.connect(self.combo_box_changed_event)
        self.ui.spinBoxParam1_3.textChanged.connect(self.spin_box_changed_event)
        self.ui.spinBoxParam2_3.textChanged.connect(self.spin_box_changed_event)
        self.ui.lineEditRelationsPath.textChanged.connect(self.line_edit_relations_path)
        self.ui.lineEditUnitNameExcelPath_3.textChanged.connect(self.line_edit_unitname_path)
        self.ui.lineEditDelaysExcelPath_3.textChanged.connect(self.line_edit_delays_path)
        self.ui.progressBar_3.setValue(0)

        self.ui.labelParam1_3.setStyleSheet("background-color: lightblue")
        self.ui.labelParam2_3.setStyleSheet("background-color: lightyellow")
        self.ui.predictButton_3.setDisabled(True)
        self.ui.Plot3d_3.setDisabled(True)

    # сравнение моделей AdaBoost и CatBoost
    @thread
    def test_model(self, signal, signal_text):
        self.disabled(True)
        signal.emit(0)
        if self.adaboost == 0:
            self.ui.textBrowser_3.append('Сначала обучите модель.')
            self.disabled(False)
            return
        dfct = self.ui.comboBoxDefects_3.currentText()
        from catboost import CatBoostRegressor
        model = CatBoostRegressor(learning_rate=1, depth=2)
        yfit = list(map(int, self.adaboost.yfiting[dfct]))
        catboost = model.fit(self.adaboost.Xfiting[dfct], yfit)
        res = catboost.predict(self.adaboost.Xtesting[dfct])
        self.ui.textBrowser_3.append('Точность модели CatBoost для параметра' +
                                     self.ui.comboBoxDefects_3.currentText() +
                                     ' = ' + str(
            round(catboost.score(self.adaboost.Xtesting[dfct], self.adaboost.ytesting[dfct]) * 100, 2)) + '%')
        array = self.adaboost.getScore()
        index = self.defects.index(dfct)
        self.ui.textBrowser_3.append('Точность модели AdaBoost  для параметра ' +
                                     self.ui.comboBoxDefects_3.currentText() +
                                     ' = ' + str(round((array[index] * 100), 2)) + '%')
        signal.emit(100)
        self.disabled(False)

    # обучение модели AdaBoost
    @thread
    def fit_model(self, signal):
        self.disabled(True)
        if len(self.excel_data_df) == 0 or len(self.name_unit) == 0 or len(self.delay) == 0 or len(self.relations) == 0:
            self.ui.textBrowser_3.append('Загрузите данные для начала работы')
            self.disabled(False)
            return
        clf = AdaBoost(self.x, self.y, self.defects, self.params, self.ui.spinBoxEmumerator_3.value())
        clf.fit(signals=signal)
        self.ui.textBrowser_3.append('Модель обучена.')
        self.ui.predictButton_3.setDisabled(False)
        self.ui.Plot3d_3.setDisabled(False)
        self.disabled(False)
        self.adaboost = clf

    # данные о точности модели AdaBoost
    @thread
    def score(self, progressbar, text):
        self.disabled(True)
        progressbar.emit(0)
        if self.adaboost == 0 or len(self.excel_data_df) == 0 or len(self.name_unit) == 0 or \
                len(self.delay) == 0 or len(self.relations) == 0:
            text.emit('Fit model first')
            return
        try:
            ycalc = self.adaboost.getScore()
            for i in range(len(self.defects)):
                text.emit('Для дефекта' + self.defects[i] +
                          ' точность прогнозирования составляет ' +
                          str(round(ycalc[i] * 100, 2)) + '%')
            text.emit('Из них ошибок 2 рода:')
            ycalc = self.adaboost.getScore(mod='e2')
            for i in range(len(self.defects)):
                self.ui.textBrowser_3.append('Для дефекта' + self.defects[i] +
                                             ' ошибки второго рода составляют ' +
                                             str(round(ycalc[i][0] * 100, 2)) + '% количество: ' + str(ycalc[i][1]))

            text.emit('Прогнозирование завершено.')
        except:
            text.emit('Неверный формат выборок.')
        progressbar.emit(100)
        self.disabled(False)

    # загрузка задержек по пути, который хранится в lineEditDelaysExcelPath_3
    def line_edit_delays_path(self):
        try:
            self.set_delays(self.ui.lineEditDelaysExcelPath_3.text())
        except:
            self.ui.predictButton_3.setDisabled(True)
            self.ui.Plot3d_3.setDisabled(True)

    # загрузка данных о названии и единицах измерения по пути, который хранится в lineEditUnitNameExcelPath_3
    def line_edit_unitname_path(self):
        self.set_name_unit(self.ui.lineEditUnitNameExcelPath_3.text())

    # загрузка данных о зависимостях по пути lineEditRelationsPath
    def line_edit_relations_path(self):
        self.buildrelationmap()

    # блокировка/разблокировка элементов управления
    def disabled(self, mod):
        self.ui.frame_19.setDisabled(mod)

    # вывод параметров от которых зависит дефект
    def combo_box_changed_event(self):
        if len(self.relations) == 0:
            return
        dfct = str(self.ui.comboBoxDefects_3.currentText())
        self.ui.comboBoxPairParams_3.clear()
        for i in range(len(self.relations[dfct])):
            self.ui.comboBoxPairParams_3.addItem(
                str(self.relations[dfct][i][0] + ' ' + str(self.relations[dfct][i][1])))

    # вывод данных о названии параметров, единицах измерения и границ варьирования
    def spin_box_changed_event(self):
        if len(self.name_unit) == 0:
            self.ui.textBrowser_3.append("Единицы измерения еще не загружены.")
            return
        i = int(self.ui.spinBoxParam1_3.value())
        j = int(self.ui.spinBoxParam2_3.value())
        self.ui.labelParam1_3.setText(str(self.name_unit[self.params[i][0]][2]))
        self.ui.labelParam2_3.setText(str(self.name_unit[self.params[j][0]][2]))
        minx = min(self.excel_data_df[self.params[i][0]])
        minx = minx if minx >= 0 else 0.0
        maxx = max(self.excel_data_df[self.params[i][0]])
        miny = min(self.excel_data_df[self.params[j][0]])
        miny = miny if miny >= 0 else 0.0
        maxy = max(self.excel_data_df[self.params[j][0]])
        self.ui.labelIntervalParam1_3.setText(str('[ ' + str(round(minx, 2)) + ' ;' + str(round(maxx, 2)) + ']'))
        self.ui.labelIntervalParam2_3.setText(str('[ ' + str(round(miny, 2)) + ' ;' + str(round(maxy, 2)) + ']'))

        self.ui.labelUnit1_3.setText('[ ' + str(self.name_unit[self.params[i][0]][0]) + ']')
        self.ui.labelUnit2_3.setText('[ ' + str(self.name_unit[self.params[j][0]][0]) + ']')

    # сигнал для обновления progress bar
    def SignalHandlerUpdateProgBar(self, data):
        print(data)
        self.ui.progressBar_3.setValue(int(data))

    # сигнал для вывода текста
    def signalHandlerTextBrowserUpdate(self, data):
        if len(data) > 0:
            self.ui.textBrowser_3.append(data)

    # сигнал для вывода графика
    def SignalHandlerUpdateGraph(self, data):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim([data[7][0], data[7][1]])
        ax.set_ylim([data[7][2], data[7][3]])
        ax.scatter(data[0], data[1], 0, c='b', marker='o')
        ax.scatter(data[2], data[3], 1, c='r', marker='+')
        ax.set_xlabel(self.ui.labelParam1_3.text() + ', ' + str(self.ui.labelUnit1_3.text()))
        ax.set_ylabel(self.ui.labelParam2_3.text() + ', ' + str(self.ui.labelUnit2_3.text()))
        ax.set_zlabel(self.ui.comboBoxDefects_3.currentText())
        plt.show()

    # вывод зон показателя качества, зависящих от параметров управляющих воздействий
    @thread
    def plot3d(self, signal_graph, signals):
        self.disabled(True)
        signals.emit(0)
        i = int(self.ui.spinBoxParam1_3.value())
        j = int(self.ui.spinBoxParam2_3.value())

        if i == j or i >= len(self.params) or j >= len(self.params):
            self.ui.textBrowser_3.append('Incorrect parametr index.')
            self.disabled(False)
            return
        if j < i:
            i, j = j, i
        self.ui.spinBoxParam1_3.setValue(i)
        self.ui.spinBoxParam2_3.setValue(j)
        if self.adaboost == 0:
            self.ui.textBrowser_3.append('Fit model first')
            self.disabled(False)
            return
        dfct = self.defects.index(str(self.ui.comboBoxDefects_3.currentText()))
        size = self.ui.spinBoxSize_3.value()

        minx = min(self.excel_data_df[self.params[i][0]])
        minx = minx if minx >= 0 else 0.0
        maxx = max(self.excel_data_df[self.params[i][0]])
        miny = min(self.excel_data_df[self.params[j][0]])
        miny = miny if miny > 0 else 0.0
        maxy = max(self.excel_data_df[self.params[j][0]])
        if minx == maxx or miny == maxy:
            self.ui.textBrowser_3.append('Parameter constant.')
            self.disabled(False)
            return
        newx = np.linspace(minx, maxx, size)
        newy = np.linspace(miny, maxy, size)
        itter = 0
        x0 = []
        y0 = []
        x1 = []
        y1 = []
        xline0 = []
        xline1 = []
        yline = []
        avg = {}
        for i in range(len(self.params)):
            avg[self.params[i][0]] = float(sum(self.excel_data_df[self.params[i][0]])) / max(
                len(self.excel_data_df[self.params[i][0]]), 1)

        for s in range(len(newx)):
            itter += 1
            signals.emit(int(itter / len(newx) * 100))
            Q = self.x[s]
            for q in range(len(self.params)):
                Q[q] = avg[self.params[i][0]]
            Q[i] = newx[s]
            Q[j] = newy[0]
            yline.append(self.x[s][j])
            a = int(self.adaboost.clf[self.defects[dfct]].predict([Q]))
            if a == 1:
                xline1.append(newx[s])
            else:
                xline0.append(newx[s])
            for l in range(len(newy)):
                Q = self.x[s]
                Q[i] = newx[s]
                Q[j] = newy[l]
                a = int(self.adaboost.clf[self.defects[dfct]].predict([Q]))
                if a == 1:
                    x1.append(newx[s])
                    y1.append(newy[l])
                else:
                    x0.append(newx[s])
                    y0.append(newy[l])
        signal_graph.emit([x0, y0, x1, y1, xline0, xline1, yline, [minx, maxx, miny, maxy]])
        self.disabled(False)

    # заполнение списка временных задержек
    def set_delays(self, path):
        self.delay = {}
        self.delay = pandas.read_excel(path).to_dict()

    # заполнение данных о названии и единицах измерения параметров
    def set_name_unit(self, path):
        try:
            self.name_unit = {}
            self.name_unit = pandas.read_excel(path).to_dict()
            params = list(self.name_unit.keys())
            self.ui.comboBoxDefects_3.clear()
            for i in range(len(self.name_unit)):
                if params[i].split('.')[0] == 'Defects':
                    self.defects.append(params[i])
                    self.ui.comboBoxDefects_3.addItem(str(params[i]))
                else:
                    self.params.append((params[i], i))
        except:
            self.ui.predictButton_3.setDisabled(True)
            self.ui.Plot3d_3.setDisabled(True)

    # заполнение данных о зависимостях дефектов от параметров
    def build_relation_map(self):
        try:
            rl = pandas.read_excel(self.ui.lineEditRelationsPath.text())
            relation = {}
            for i in range(len(rl['Def'])):
                relation[rl['Def'][i]] = []
                for j in range(len(rl.columns)):
                    if rl[rl.columns[j]][i] == '*':
                        a = rl.columns[j]
                        b = rl[rl.columns[0]][i]
                        relation[b].append(a)
            self.relations = {}
            for i in range(len(relation)):
                par = list(relation.keys())[i]
                self.relations[par] = []
                if len(relation[par]) >= 2:
                    for j in range(len(relation[par])):
                        for k in range(j + 1, len(relation[par])):
                            self.relations[par].append((relation[par][j], relation[par][k]))
        except:
            self.ui.predictButton_3.setDisabled(True)
            self.ui.Plot3d_3.setDisabled(True)
            self.ui.textBrowser_3.append("Файл с зависимостей имеет неверный формат.")

    # заполнение полей исходя из выбора пользователя
    def set_parametrs(self):
        if len(self.ui.comboBoxPairParams_3.currentText()) <= 0:
            self.ui.textBrowser_3.append('Select parameters first')
            return
        par = str.split(self.ui.comboBoxPairParams_3.currentText(), ' ')
        for i in range(len(self.params)):
            if par[0] == self.params[i][0]:
                self.ui.spinBoxParam1_3.setValue(i)
            if par[1] == self.params[i][0]:
                self.ui.spinBoxParam2_3.setValue(i)

    # загрузка промышленных данных
    def load_data(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if len(fname) == 0:
            return
        try:
            df = self.file.load_data_from_dump(fname)
        except:
            try:
                df = pandas.read_excel(fname)
            except:
                self.ui.textBrowser_3.append("Неверный формат данных.")
                return
        self.set_name_unit(self.ui.lineEditUnitNameExcelPath_3.text())
        params = list(self.name_unit.keys())
        self.x = []
        self.y = {}
        self.defects = []
        self.params = []
        try:
            self.ui.comboBoxDefects_3.clear()
            for i in range(len(self.name_unit)):
                self.excel_data_df[params[i]] = df[params[i]]
                if params[i].split('.')[0] == 'Defects':
                    self.defects.append(params[i])
                    self.ui.comboBoxDefects_3.addItem(str(params[i]))
                else:
                    self.params.append((params[i], i))
            for i in range(len(self.params)):
                self.excel_data_df[self.params[i][0]] = self.proc.build_list(
                    self.excel_data_df[self.params[i][0]])
            for i in range(len(self.defects)):
                self.y[self.defects[i]] = np.array(
                    self.proc.delete_nan(list(self.excel_data_df[self.defects[i]])))
            self.set_delays(self.ui.lineEditDelaysExcelPath_3.text())
        except:
            self.ui.textBrowser_3.append("Неверное содержание файла с данными.")
            self.excel_data_df = {}
            return
        self.x, self.y = self.proc.build_2D_list(self.delay, self.params, self.defects, self.name_unit,
                                                 self.excel_data_df, self.y)
        self.build_relation_map()
        self.ui.spinBoxParam1_3.setMaximum(len(self.params) - 1)
        self.ui.spinBoxParam2_3.setMaximum(len(self.params) - 1)
        self.spin_box_changed_event()

        self.ui.progressBar_3.setValue(100)
        self.ui.textBrowser_3.append('Загрузка данных завершена.')

        if self.adaboost != 0:
            self.ui.predictButton_3.setDisabled(False)
            self.ui.Plot3d_3.setDisabled(False)
        return

    # загрузка обученной модели из файла
    def load_model(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if len(file_name) == 0:
            self.ui.textBrowser_3.append('Пустой путь к файлу.')
            return
        self.adaboost = self.file.load_model(file_name,len(self.excel_data_df))
        clf = AdaBoost([], [], [], [])
        if self.adaboost.__class__ != clf.__class__:
            self.adaboost = 0
            return
        self.ui.textBrowser_3.append("Модель загружена.")

    # сохранение обученной модели в файл
    def save_model(self):
        if self.adaboost == 0:
            self.ui.textBrowser_3.append('Обучите модель прежде, чем сохранять.')
            return
        file_name = QFileDialog.getSaveFileName(self, 'Create file', '/home')[0]
        if len(file_name) == 0:
            self.ui.textBrowser_3.append('Пустой путь к файлу.')
            return
        self.file.save_model(file_name)

    # сохранение промышленных данных в файл
    def save_data(self):
        if len(self.excel_data_df) == 0:
            self.ui.textBrowser_3.append("Нет данных для сохранения.")
            return
        file_name = QFileDialog.getOpenFileName(self, 'Create file', '/home')[0]
        if len(file_name) == 0:
            return
        self.file.save_data(file_name, self.excel_data_df)