from design import *
from DataProcess import *
from File import *
import threading
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from AdaBoost import *
from DataReader import *
import datetime as dt
from catboost import CatBoostRegressor


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
        self.excel_data_df = {}  # датафрейм из файла excel
        self.delay = {}  # данные по задержкам
        self.x = []  # данные, подготовленные для обучения модели
        self.y = {}  # качественные показатели по каждому из дефектов
        self.adaboost = 0  # сама модель адаптивного бустинга
        self.proc = DataProcess()  # класс для обработки данных
        self.file = File(self.ui)  # класс для работы с файлами
        self.limits = {}  # критические значени

        # подключение кнопок и сигналов
        self.ui.LoadButton.clicked.connect(self.load_data)
        self.ui.FitButton.clicked.connect(lambda: self.fit_model(self.signal_progress_bar))
        self.ui.predictButton.clicked.connect(lambda: self.score(self.signal_progress_bar))
        self.ui.Plot3d.clicked.connect(lambda: self.plot3d(self.signal_graph, self.signal_progress_bar))
        self.ui.ROCButton.clicked.connect(self.roc_curve)
        self.ui.trendButton.clicked.connect(self.trends)
        self.ui.testModelButton.clicked.connect(lambda: self.test_model(self.signal_progress_bar))
        self.signal_progress_bar.connect(self.sh_update_prog_bar)
        self.signal_graph.connect(self.sh_update_graph)
        self.signal_text.connect(self.sh_text_browser_update)
        self.ui.setParamsButton.clicked.connect(self.set_parametrs)
        self.ui.spinBoxParam1.textChanged.connect(self.spin_box_changed_event)
        self.ui.spinBoxParam2.textChanged.connect(self.spin_box_changed_event)

        self.ui.progressBar.setValue(0)
        self.ui.labelParam1.setStyleSheet("background-color: lightblue")
        self.ui.labelParam2.setStyleSheet("background-color: lightyellow")
        self.ui.predictButton.setDisabled(True)
        self.ui.Plot3d.setDisabled(True)
        self.ui.ROCButton.setDisabled(True)
        self.ui.trendButton.setDisabled(True)
        self.ui.testModelButton.setDisabled(True)
        self.ui.FitButton.setDisabled(True)

    # сравнение моделей AdaBoost и CatBoost
    @thread
    def test_model(self, signal):
        self.disabled(True)
        signal.emit(0)
        defect = self.ui.comboBoxDefects.currentText()
        if self.adaboost == 0:
            self.ui.textBrowser.append('Сначала обучите модель.')
            self.disabled(False)
            return
        if self.adaboost.defect != defect:
            self.ui.textBrowser.append('Модель не обучена для этого параметра.')
            self.disabled(False)
            return

        model = CatBoostRegressor(learning_rate=1, depth=2, random_state=int(random.random() * 999999999))
        yfit = list(map(int, self.adaboost.yfiting))
        catboost = model.fit(self.adaboost.Xfiting, yfit)
        print(len(self.adaboost.Xfiting))
        print(len(self.adaboost.yfiting))
        print(len(self.adaboost.Xtesting))
        print(len(self.adaboost.ytesting))
        ycat = catboost.predict(self.adaboost.Xtesting)
        ycat = [round(x) for x in ycat]
        yada = self.adaboost.clf.predict(self.adaboost.Xtesting)
        score_cat = self.proc.getScore(self.adaboost.ytesting, ycat, mod='st') * 100
        score_ada = self.proc.getScore(self.adaboost.ytesting, yada, mod='st') * 100
        score_cat_f = self.proc.getScore(self.adaboost.ytesting, ycat, mod='F') * 100
        score_ada_f = self.proc.getScore(self.adaboost.ytesting, yada, mod='F') * 100
        score_cat_kkm = self.proc.getScore(self.adaboost.ytesting, ycat, mod='KKM') * 100
        score_ada_kkm = self.proc.getScore(self.adaboost.ytesting, yada, mod='KKM') * 100
        self.ui.textBrowser.append('Точность модели CatBoost для параметра' +
                                   defect + ' = ' + str(round(score_cat, 2)) + '%')
        self.ui.textBrowser.append('Точность модели AdaBoost  для параметра ' +
                                   defect + ' = ' + str(round(score_cat_f, 2)) + '%')
        self.ui.textBrowser.append('F мера для модели CatBoost для дефекта' +
                                   defect + ' = ' + str(round(score_cat_kkm, 2)))

        self.ui.textBrowser.append('F мера для модели AdaBoost для дефекта' +
                                   defect + ' = ' + str(round(score_ada, 2)))
        self.ui.textBrowser.append('KKM мера для модели CatBoost для дефекта' +
                                   defect + ' = ' + str(round(score_ada_f, 2)))
        self.ui.textBrowser.append('KKM мера для модели AdaBoost для дефекта' +
                                   defect + ' = ' + str(round(score_ada_kkm, 2)))

        signal.emit(100)
        self.disabled(False)

    # обучение модели AdaBoost
    @thread
    def fit_model(self, signal):
        self.disabled(True)
        if len(self.excel_data_df) == 0:
            self.ui.textBrowser.append('Загрузите данные для начала работы.')
            self.disabled(False)
            return
        if len(self.defects) == 0:
            self.ui.textBrowser.append("Данных недостаточно для прогнозирования.")
            self.disabled(False)
            return
        defect = self.ui.comboBoxDefects.currentText()
        clf = AdaBoost(self.x, self.y[defect], defect, self.limits, self.ui.spinBoxEmumerator.value())
        clf.fit(signals=signal)
        self.ui.textBrowser.append('Модель для параметра %(defect)s обучена.' % {"defect": defect})
        self.ui.predictButton.setDisabled(False)
        self.ui.Plot3d.setDisabled(False)
        self.ui.ROCButton.setDisabled(False)
        self.ui.trendButton.setDisabled(False)
        self.ui.testModelButton.setDisabled(False)
        self.disabled(False)
        self.adaboost = clf

    # данные о точности модели AdaBoost
    @thread
    def score(self, progressbar):
        self.disabled(True)
        progressbar.emit(0)
        defect = self.ui.comboBoxDefects.currentText()
        if self.adaboost == 0:
            self.ui.textBrowser.append('Сначала обучите модель.')
            self.disabled(False)
            return
        if self.adaboost.defect != defect:
            self.ui.textBrowser.append('Модель не обучена для этого параметра.')
            self.disabled(False)
            return

        yada = self.adaboost.clf.predict(self.adaboost.Xtesting)
        score = self.proc.getScore(self.adaboost.ytesting, yada, mod='st') * 100
        score_f = self.proc.getScore(self.adaboost.ytesting, yada, mod='F') * 100
        score_kkm = self.proc.getScore(self.adaboost.ytesting, yada, mod='KKM') * 100
        self.ui.textBrowser.append('Точность модели AdaBoost  для параметра ' +
                                   defect + ' = ' + str(round(score, 2)) + '%')
        self.ui.textBrowser.append('F мера для модели AdaBoost для дефекта' +
                                   defect + ' = ' + str(round(score_f, 2)))
        self.ui.textBrowser.append('KKM мера для модели AdaBoost для дефекта' +
                                   defect + ' = ' + str(round(score_kkm, 2)))
        progressbar.emit(100)
        self.disabled(False)

    # блокировка/разблокировка элементов управления
    def disabled(self, mod):
        self.ui.frame_19.setDisabled(mod)

    # вывод данных о названии параметров, единицах измерения и границ варьирования
    def spin_box_changed_event(self):
        i = int(self.ui.spinBoxParam1.value())
        j = int(self.ui.spinBoxParam2.value())
        self.ui.labelParam1.setText(str(self.params[i][0]))
        self.ui.labelParam2.setText(str(self.params[j][0]))
        mini = self.limits[self.params[i][0]][0]
        mini = mini if mini >= 0 else 0.0
        maxi = self.limits[self.params[i][0]][1]
        minj = self.limits[self.params[j][0]][0]
        minj = minj if minj >= 0 else 0.0
        maxj = self.limits[self.params[j][0]][1]
        self.ui.labelIntervalParam1.setText(str('[ ' + str(round(mini, 2)) + ' ;' + str(round(maxi, 2)) + ']'))
        self.ui.labelIntervalParam2.setText(str('[ ' + str(round(minj, 2)) + ' ;' + str(round(maxj, 2)) + ']'))

        self.ui.labelUnit1.setText('[ ' + str(self.params[i][0]) + ']')
        self.ui.labelUnit2.setText('[ ' + str(self.params[j][0]) + ']')

    # сигнал для обновления progress bar
    def sh_update_prog_bar(self, data):
        self.ui.progressBar.setValue(int(data))

    # сигнал для вывода текста
    def sh_text_browser_update(self, data):
        if len(data) > 0:
            self.ui.textBrowser.append(data)

    # сигнал для вывода графика
    def sh_update_graph(self, data):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim([data[7][0], data[7][1]])
        ax.set_ylim([data[7][2], data[7][3]])
        ax.scatter(data[0], data[1], 0, c='b', marker='o')
        ax.scatter(data[2], data[3], 1, c='r', marker='+')
        ax.set_xlabel(self.ui.labelParam1.text() + ', ' + str(self.ui.labelUnit1.text()))
        ax.set_ylabel(self.ui.labelParam2.text() + ', ' + str(self.ui.labelUnit2.text()))
        ax.set_zlabel(self.ui.comboBoxDefects.currentText())
        plt.show()

    # вывод зон показателя качества, зависящих от параметров управляющих воздействий
    @thread
    def plot3d(self, signal_graph, signals):
        self.disabled(True)
        signals.emit(0)
        i = int(self.ui.spinBoxParam1.value())
        j = int(self.ui.spinBoxParam2.value())

        if i == j or i >= len(self.params) or j >= len(self.params):
            self.ui.textBrowser.append('Incorrect parametr index.')
            self.disabled(False)
            return
        if j < i:
            i, j = j, i
        self.ui.spinBoxParam1.setValue(i)
        self.ui.spinBoxParam2.setValue(j)
        if self.adaboost == 0:
            self.ui.textBrowser.append('Обучите модель для начала.')
            self.disabled(False)
            return

        dfct = self.ui.comboBoxDefects.currentText()
        if self.adaboost.defect != dfct:
            self.ui.textBrowser.append('Модель не обучена для этого дефекта.')
            self.disabled(False)
            return
        size = self.ui.spinBoxSize.value()

        minx = min(self.excel_data_df[self.params[i][0]])
        minx = minx if minx >= 0 else 0.0
        maxx = max(self.excel_data_df[self.params[i][0]])
        miny = min(self.excel_data_df[self.params[j][0]])
        miny = miny if miny > 0 else 0.0
        maxy = max(self.excel_data_df[self.params[j][0]])
        if minx == maxx or miny == maxy:
            self.ui.textBrowser.append('Parameter constant.')
            self.disabled(False)
            return

        minx = self.limits[self.params[i][0]][0]
        maxx = self.limits[self.params[i][0]][1]
        miny = self.limits[self.params[j][0]][0]
        maxy = self.limits[self.params[j][0]][1]

        if minx == maxx or miny == maxy:
            self.ui.textBrowser.append('Совпадение границ параметра.')
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
                len(self.excel_data_df[self.params[i][0]]), 1)  # берем среднее значение по каждому из параметров

        for s in range(len(newx)):
            itter += 1
            signals.emit(int(itter / len(newx) * 100))
            curr = self.x[s]
            for q in range(len(self.params)):
                curr[q] = avg[self.params[i][0]]
            curr[i] = newx[s]

            yline.append(self.x[s][j])
            curr[j] = newy[0]
            a = int(self.adaboost.clf.predict([curr]))
            if a == 1:
                xline1.append(newx[s])
            else:
                xline0.append(newx[s])
            for l in range(len(newy)):
                curr = self.x[s]
                curr[i] = newx[s]
                curr[j] = newy[l]
                a = int(self.adaboost.clf.predict([curr]))
                if a == 1:
                    x1.append(newx[s])
                    y1.append(newy[l])
                else:
                    x0.append(newx[s])
                    y0.append(newy[l])
        signal_graph.emit([x0, y0, x1, y1, xline0, xline1, yline, [minx, maxx, miny, maxy]])
        self.disabled(False)

    # построение roc кривой
    def roc_curve(self):
        res = self.adaboost.clf.predict_proba(self.adaboost.Xtesting)
        y = self.adaboost.ytesting
        res_pos_prob = []
        for i in range(len(res)):
            res_pos_prob.append((res[i][1], y[i]))
        res_pos_prob = sorted(res_pos_prob, key=lambda tup: tup[0], reverse=True)
        count_of_pos = 0
        count_of_neg = len(res_pos_prob)
        for i in range(len(res_pos_prob)):
            if res_pos_prob[i][1] == 1:
                count_of_pos += 1
        count_of_neg -= count_of_pos
        stepy = 1 / max(count_of_pos, 1)
        stepx = 1 / max(count_of_neg, 1)
        yline = []
        xline = []
        xcoordline = 0
        xlinestep = 1 / len(res_pos_prob)
        ycoord = 0
        xcoord = 0
        curvex = []
        curvey = []
        s = 0
        for i in range(len(res_pos_prob)):
            if res_pos_prob[i][1] == 1:
                ycoord += stepy  # учет позитивного прогноза
            else:
                xcoord += stepx  # учет негативного прогноза
                s += ycoord * stepx  # расчет площади
            xcoordline += xlinestep
            yline.append(xcoord)
            xline.append(xcoord)
            curvex.append(xcoord)
            curvey.append(ycoord)

        fig = plt.figure()
        ax = fig.gca()
        ax.plot(curvex, curvey, 'o-', c='r')
        ax.plot(xline, yline, c='g')
        plt.show()
        self.ui.textBrowser.append("Площадь под графиком ROC кривой равна " + str(round(s, 4)))

    # построение трендов
    def trends(self):
        trend_param = []
        trend_defect = []
        trend_predict = []
        time = []
        fig, (axParam, axExpertDef, axModelDef) = plt.subplots(3, 1)
        fig.suptitle('Trends')
        param = self.params[self.ui.spinBoxParam1.value()][0]
        defect = self.ui.comboBoxDefects.currentText()
        predict = self.adaboost.clf.predict(self.x)

        for i in range(len(self.excel_data_df['DateTime'])):
            trend_param.append(self.excel_data_df[param][i])
            trend_defect.append(self.excel_data_df[defect][i])
            trend_predict.append(predict[i])
            year_month_day = [int(x) for x in self.excel_data_df['DateTime'][i].split(' ')[0].split('-')]
            hour_min_sec = [int(x) for x in self.excel_data_df['DateTime'][i].split(' ')[1].split(':')]
            time.append(dt.datetime(year_month_day[0], year_month_day[1], year_month_day[2],
                                    hour_min_sec[0], hour_min_sec[1], hour_min_sec[2]))  # заполнение массива времени по оси x

        axParam.plot(time, trend_param)
        axParam.set_ylabel(param)
        axExpertDef.plot(time, trend_defect)
        axExpertDef.set_ylabel(defect)
        axModelDef.plot(time, trend_predict)
        axModelDef.set_ylabel('predict')
        axModelDef.set_xlabel('date')

        plt.show()

    # заполнение полей исходя из выбора пользователя
    def set_parametrs(self):
        if len(self.ui.comboBoxPairParams.currentText()) <= 0:
            self.ui.textBrowser.append('Select parameters first')
            return
        par = str.split(self.ui.comboBoxPairParams.currentText(), ' ')
        for i in range(len(self.params)):
            if par[0] == self.params[i][0]:
                self.ui.spinBoxParam1.setValue(i)
            if par[1] == self.params[i][0]:
                self.ui.spinBoxParam2.setValue(i)

    # загрузка промышленных данных
    def load_data(self):
        self.excel_data_df, params = db_reader(self.ui.spinBoxCallDBSize.value())
        self.limits = db_limits()
        print(params)
        self.x = []
        self.y = {}
        self.defects = []
        self.params = []
        try:
            self.ui.comboBoxDefects.clear()
            for i in range(len(params)):
                try:
                    if params[i][1].split('.')[0] == 'Defects':
                        self.defects.append(params[i][1])
                    else:
                        self.params.append((params[i][1], i))
                except:
                    self.params.append((params[i][1], i))

            for i in range(len(self.params)):
                self.excel_data_df[self.params[i][0]] = self.proc.build_list(
                    self.excel_data_df[self.params[i][0]])
            for i in range(len(self.defects)):
                self.y[self.defects[i]] = self.proc.build_list(
                    self.excel_data_df[self.defects[i]])
        except:
            self.ui.textBrowser.append("Неверное содержание файла с данными.")
            self.excel_data_df = {}
            return
        defect = self.defects
        i = 0
        while i < len(self.defects):
            maxd = max(self.excel_data_df[self.defects[i]])
            mind = min(self.excel_data_df[self.defects[i]])
            if maxd == mind:
                defect.remove(self.defects[i])  # удаление неизменяющихся значений дефектов
            else:
                i += 1
        self.defects = defect
        while i < len(self.params):
            maxd = max(self.excel_data_df[self.params[i][0]])
            mind = min(self.excel_data_df[self.params[i][0]])
            if maxd == mind:
                self.params.remove(self.params[i])  # удаление неизменяющихся параметров
            else:
                i += 1

        for el in defect:
            self.ui.comboBoxDefects.addItem(el)
        self.x, self.y = self.proc.build_2D_list(self.params, self.defects, self.limits, self.excel_data_df, self.y)
        self.ui.spinBoxParam1.setMaximum(len(self.params) - 1)
        self.ui.spinBoxParam2.setMinimum(1)
        self.ui.spinBoxParam2.setMaximum(len(self.params) - 1)
        self.spin_box_changed_event()

        self.ui.progressBar.setValue(100)
        self.ui.textBrowser.append('Загрузка данных завершена.')

        if self.adaboost != 0:
            self.ui.predictButton.setDisabled(False)
            self.ui.Plot3d.setDisabled(False)
        self.ui.FitButton.setDisabled(False)