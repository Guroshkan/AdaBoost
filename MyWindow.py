# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: C:\Users\acer nitro 5\PycharmProjects\AdaBoostVisualDemo lib\MyWindow.py
# Compiled at: 2021-05-10 06:48:18
# Size of source mod 2**32: 53409 bytes
import Language
from design import *
from DataProcess import *
import threading
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from AdaBoost import *
from DataReader import *
import datetime as dt
from catboost import CatBoostClassifier
from Language import *
from datetime import datetime
import calendarFormConnector


def thread(my_func):
    def wrapper(*args):
        my_thread = threading.Thread(target=my_func, args=args)
        my_thread.start()

    return wrapper


class MyWin(QtWidgets.QMainWindow):
    signal_progress_bar = QtCore.pyqtSignal(int, name='signal_progress_bar')
    signal_graph = QtCore.pyqtSignal(list, name='signal_graph')
    signal_text = QtCore.pyqtSignal(str, name='signal_text')
    signal_progress_bar_status = QtCore.pyqtSignal(str, name='signal_progress_bar_status')
    select_first_defect = QtCore.pyqtSignal(name='select_first_defect')
    select_first_defect_model = QtCore.pyqtSignal(name='select_first_defect_model')
    set_parametr = QtCore.pyqtSignal(name='set_parametr')

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.defects = []
        self.id_defects = {}
        self.params = []
        self.delay = {}
        self.x = []
        self.y = {}
        self.adaboost = 0
        self.proc = DataProcess()
        self.limits = {}
        self.nameUnit = {}
        self.currentLanguage = Language.Ru
        self.ui.changeParameterIndexRightButton.clicked.connect(self.changeParameterIndexRightButtonEvent)
        self.ui.changeParameterIndexLeftButton.clicked.connect(self.changeParameterIndexLeftButtonEvent)
        self.ui.saveModelButton.clicked.connect(self.save_model)
        self.ui.LoadButton.clicked.connect(
            lambda: self.load_data(self.signal_progress_bar, self.signal_progress_bar_status, self.signal_text,
                                   self.select_first_defect))
        self.ui.LoadButtonModel.clicked.connect(
            lambda: self.load_dataModel(self.signal_progress_bar, self.signal_progress_bar_status, self.signal_text,
                                        self.select_first_defect))
        self.ui.loadModelButton.clicked.connect(self.load_model)
        self.ui.languageButton.clicked.connect(self.change_language)
        self.ui.languageButtonModel.clicked.connect(self.change_language)
        self.ui.refreshModelButton.clicked.connect(self.refresh_model)
        self.ui.FitButton.clicked.connect(
            lambda: self.fit_model(self.signal_progress_bar, self.signal_progress_bar_status, self.signal_text,
                                   self.set_parametr))
        self.ui.predictButton.clicked.connect(lambda: self.score(self.signal_progress_bar))
        self.ui.ROCButton.clicked.connect(self.roc_curve)
        self.ui.trendButton.clicked.connect(self.trends)
        self.ui.testModelButton.clicked.connect(
            lambda: self.test_model(self.signal_progress_bar, self.signal_progress_bar_status))
        self.signal_progress_bar.connect(self.sh_update_prog_bar)
        self.signal_progress_bar_status.connect(self.sh_update_prog_bar_status)
        self.signal_graph.connect(self.sh_update_graph)
        self.signal_text.connect(self.sh_text_browser_update)
        self.select_first_defect.connect(self.sh_select_first_defect)
        self.select_first_defect_model.connect(self.sh_select_first_defect_model)
        self.set_parametr.connect(self.sh_param_index_set)
        self.ui.comboBoxDefectsModel.currentTextChanged.connect(self.change_comboBoxDefectsModel)
        self.ui.comboBoxTimeModel.currentTextChanged.connect(self.change_comboBoxTimeModel)
        self.current_value_param_spinbox_index = 0
        self.ui.calendarEditFromButton.clicked.connect(self.makeDateFrom)
        self.ui.calendarEditToButton.clicked.connect(self.makeDateTo)
        self.ui.calendarEditFromButtonModel.clicked.connect(self.makeDateFromModel)
        self.ui.calendarEditToButtonModel.clicked.connect(self.makeDateToModel)
        self.ui.progressBar.setValue(0)
        self.ui.progressBarModel.setValue(0)
        self.ui.predictButton.setDisabled(True)
        self.ui.ROCButton.setDisabled(True)
        self.ui.trendButton.setDisabled(True)
        self.ui.testModelButton.setDisabled(True)
        self.ui.FitButton.setDisabled(True)
        self.ui.saveModelButton.setDisabled(True)
        self.ui.changeParameterIndexLeftButton.setDisabled(True)
        self.ui.changeParameterIndexRightButton.setDisabled(True)
        self.ui.loadModelButton.setDisabled(True)
        self.ui.spinBoxEmumerator.setDisabled(True)
        self.limit_calendar()

    def makeDateFrom(self):
        self.win_calendar_from = calendarFormConnector.Ui_TimeManagerController(self, self.ui.dateEditFrom, 'min')
        self.win_calendar_from.show()

    def makeDateTo(self):
        self.win_calendar_to = calendarFormConnector.Ui_TimeManagerController(self, self.ui.dateEditTo, 'max')
        self.win_calendar_to.show()

    def makeDateFromModel(self):
        self.win_calendar_from_model = calendarFormConnector.Ui_TimeManagerController(self, self.ui.dateEditFromModel,
                                                                                      'min')
        self.win_calendar_from_model.show()

    def makeDateToModel(self):
        self.win_calendar_to_model = calendarFormConnector.Ui_TimeManagerController(self, self.ui.dateEditToModel,
                                                                                    'max')
        self.win_calendar_to_model.show()

    def limit_calendar(self):
        self.maxTime, self.minTime = findTimeRange()
        self.ui.dateEditFrom.setDateTime(datetime.strptime(self.minTime, '%Y-%m-%d %H:%M:%S'))
        self.ui.dateEditTo.setDateTime(datetime.strptime(self.maxTime, '%Y-%m-%d %H:%M:%S'))
        self.ui.dateEditFromModel.setDateTime(datetime.strptime(self.minTime, '%Y-%m-%d %H:%M:%S'))
        self.ui.dateEditToModel.setDateTime(datetime.strptime(self.maxTime, '%Y-%m-%d %H:%M:%S'))

    def change_language(self):
        self.ui.labelProgresBarStatus.clear()
        self.ui.labelProgresBarStatusModel.clear()

        if self.currentLanguage == Language.En:
            self.ui.LoadButton.setText('Загрузить данные')
            self.ui.LoadButtonModel.setText('Загрузить данные')
            self.ui.ROCButton.setText('ROC кривая')
            self.ui.trendButton.setText('Тренды')
            self.ui.testModelButton.setText('Сравнение модели')
            self.ui.predictButton.setText('Качество модели')
            self.ui.FitButton.setText('Обучить модель')
            self.ui.labelDefects.setText('Дефект')
            self.ui.labelEnumerator.setText('Количество оценщиков')
            self.ui.lableEstimating.setText('Показатели модели')
            self.ui.labelDefectsModel.setText('Дефект')
            self.ui.labelCountModel.setText('Количество оценщиков')
            self.ui.labelDateTimeFrom.setText('От')
            self.ui.labelDateTimeTo.setText('До')
            self.ui.labelDateTimeFromModel.setText('От')
            self.ui.labelDateTimeToModel.setText('До')
            self.ui.refreshModelButton.setText('Обновить')
            self.ui.loadModelButton.setText('Загрузить модель')
            self.ui.trendButton.setText('Тренды')
            self.ui.labelTimeModel.setText('Период времени')
            self.ui.tabWidget.setTabText(0, 'Обучение')
            self.ui.tabWidget.setTabText(1, 'Прогноз')
            if len(self.nameUnit) != 0:
                chosen_defect = self.find_defect(self.ui.comboBoxDefects.currentText())
                self.ui.comboBoxDefects.clear()
                for defect_code in self.defects:
                    if self.nameUnit[defect_code][1] != 'nan':
                        self.ui.comboBoxDefects.addItem(self.nameUnit[defect_code][0])
                    self.ui.comboBoxDefects.setCurrentText(self.nameUnit[chosen_defect][0])
                    if self.adaboost != 0:
                        self.ui.labelParam1.setText(self.nameUnit[self.params[
                            sorted(self.adaboost.indexes)[self.current_value_param_spinbox_index]][0]][
                                                        Language.Ru.value])

            else:
                self.ui.labelParam1.setText('Параметр')
                self.ui.labelUnit1.setText('Ед.изм.')
            self.ui.languageButton.setText('Ru')
            self.ui.languageButtonModel.setText('Ru')
            self.currentLanguage = Language.Ru
        else:
            if self.currentLanguage == Language.Ru:
                self.ui.LoadButton.setText('Load data')
                self.ui.LoadButtonModel.setText('Load data')
                self.ui.ROCButton.setText('ROC curvie')
                self.ui.trendButton.setText('Trends')
                self.ui.testModelButton.setText('Model comparison')
                self.ui.predictButton.setText('Model quality')
                self.ui.FitButton.setText('FitModel')
                self.ui.labelDefects.setText('Defect')
                self.ui.labelEnumerator.setText('Count estimators')
                self.ui.lableEstimating.setText('Estimating control')
                self.ui.labelDefectsModel.setText('Defect')
                self.ui.labelCountModel.setText('Count estimators')
                self.ui.labelDateTimeFrom.setText('From')
                self.ui.labelDateTimeTo.setText('To')
                self.ui.labelDateTimeFromModel.setText('From')
                self.ui.labelDateTimeToModel.setText('To')
                self.ui.refreshModelButton.setText('Refresh')
                self.ui.loadModelButton.setText('Load model')
                self.ui.trendButton.setText('Trends')
                self.ui.labelTimeModel.setText('Period of time')
                self.ui.tabWidget.setTabText(0, 'Learning')
                self.ui.tabWidget.setTabText(1, 'Predict')
                if len(self.nameUnit) != 0:
                    chosen_defect = self.find_defect()
                    self.ui.comboBoxDefects.clear()
                    for defect_code in self.defects:
                        if self.nameUnit[defect_code][1] != 'nan':
                            self.ui.comboBoxDefects.addItem(self.nameUnit[defect_code][1])
                        self.ui.comboBoxDefects.setCurrentText(self.nameUnit[chosen_defect][1])
                        if self.adaboost != 0:
                            self.ui.labelParam1.setText(self.nameUnit[self.params[
                                sorted(self.adaboost.indexes)[self.current_value_param_spinbox_index]][0]][
                                                            Language.En.value])

                else:
                    self.ui.labelParam1.setText('Parameter')
                    self.ui.labelUnit1.setText('Unit.')
                self.ui.languageButton.setText('En')
                self.ui.languageButtonModel.setText('En')
                self.currentLanguage = Language.En
        if self.adaboost != 0:
            self.set_parametr.emit()

    @thread
    def test_model(self, signal_pb, signal_pb_status):
        self.disabled(True)
        signal_pb.emit(0)
        defect = self.find_defect()

        if self.adaboost.defect != defect:
            if self.currentLanguage == Language.Ru:
                self.ui.textBrowser.append('Модель не обучена для этого параметра.')
            if self.currentLanguage == Language.En:
                self.ui.textBrowser.append("Model don't fitted for this parameter.")
            self.disabled(False)
            return None

        model = CatBoostClassifier(learning_rate=1, depth=2, random_state=(int(random.random() * 999999999)))
        if self.currentLanguage == Language.Ru:
            signal_pb_status.emit('Обучение модели CatBoost.')
        if self.currentLanguage == Language.En:
            signal_pb_status.emit('Learning CatBoost model.')
        catboost = model.fit(self.Xfiting, self.yfiting)

        ycat = catboost.predict(self.Xtesting)
        yada = self.adaboost.clf.predict(self.Xtesting)
        score_cat = self.proc.getScore((self.ytesting), ycat, mod='st') * 100
        score_ada = self.proc.getScore((self.ytesting), yada, mod='st') * 100
        score_cat_f = self.proc.getScore((self.ytesting), ycat, mod='F') * 100
        score_ada_f = self.proc.getScore((self.ytesting), yada, mod='F') * 100
        score_cat_kkm = self.proc.getScore((self.ytesting), ycat, mod='KKM') * 100
        score_ada_kkm = self.proc.getScore((self.ytesting), yada, mod='KKM') * 100
        if self.currentLanguage == Language.Ru:
            self.ui.textBrowser.append(
                f'Точность модели CatBoost для параметра {defect} = {round(score_cat, 2)} %')
            self.ui.textBrowser.append(
                f'Точность модели AdaBoost  для параметра {defect} = {round(score_ada, 2)}%')
            self.ui.textBrowser.append(
                f'F мера для модели CatBoost для дефекта {defect} = {round(score_cat_f, 2)}')
            self.ui.textBrowser.append(
                f'F мера для модели AdaBoost для дефекта {defect} = {round(score_ada_f, 2)}')
            self.ui.textBrowser.append(
                f'KKM мера для модели CatBoost для дефекта {defect} = {round(score_cat_kkm, 2)}')
            self.ui.textBrowser.append(
                f'KKM мера для модели AdaBoost для дефекта {defect} = {round(score_ada_kkm, 2)}')
        if self.currentLanguage == Language.En:
            self.ui.textBrowser.append(
                f'CatBoost model precision for parameter {defect} = {round(score_cat, 2)} %')
            self.ui.textBrowser.append(
                f'AdaBoost model precision for parameter {defect} = {round(score_ada, 2)}%')
            self.ui.textBrowser.append(
                f'F measure for the CatBoost model for the defect {defect} = {round(score_cat_f, 2)}')
            self.ui.textBrowser.append(
                f'F measure for the AdaBoost model for the defect {defect} = {round(score_ada_f, 2)}')
            self.ui.textBrowser.append(
                f'KKM measure for CatBoost model for defect {defect} = {round(score_cat_kkm, 2)}')
            self.ui.textBrowser.append(
                f'KKM measure for AdaBoost model for defect {defect} = {round(score_ada_kkm, 2)}')
        signal_pb.emit(100)
        signal_pb_status.emit('')
        self.disabled(False)

    @thread
    def fit_model(self, signal_pb, signal_pb_status, signal_text, signal_set_parametr):
        self.disabled(True)
        if len(self.x) == 0:
            if self.currentLanguage == Language.Ru:
                signal_text.emit('Загрузите данные для начала работы.')
            if self.currentLanguage == Language.En:
                signal_text.emit('Download data to get started.')
            self.disabled(False)
            return None
        if len(self.defects) == 0:
            if self.currentLanguage == Language.Ru:
                signal_text.emit('Данных недостаточно для прогнозирования.')
            if self.currentLanguage == Language.En:
                signal_text.emit('Not enough data to predict.')
            self.disabled(False)
            return None
        defect = self.find_defect()
        ada_boost_clf = AdaBoost(defect, self.limits, self.id_params[defect], self.ui.spinBoxEmumerator.value())
        if self.currentLanguage == Language.Ru:
            signal_pb_status.emit('Обучение алгоритма адаптивного бустига.')
        if self.currentLanguage == Language.En:
            signal_pb_status.emit('Learning the AdaBoost algorithm.')
        self.Xfiting, self.yfiting, self.Xtesting, self.ytesting = ada_boost_clf.fit((self.x), (self.y[defect]),
                                                                                     signal_pb=signal_pb)
        self.adaboost = ada_boost_clf
        if self.currentLanguage == Language.Ru:
            signal_text.emit(f"Модель для параметра {self.nameUnit[defect][self.currentLanguage.value]} обучена.")
        if self.currentLanguage == Language.En:
            signal_text.emit(f"Model for parameter {self.nameUnit[defect][self.currentLanguage.value]} trained.")
        signal_set_parametr.emit()
        self.ui.predictButton.setDisabled(False)
        self.ui.ROCButton.setDisabled(False)
        self.ui.trendButton.setDisabled(False)
        self.ui.testModelButton.setDisabled(False)
        self.disabled(False)
        self.ui.saveModelButton.setDisabled(False)
        self.ui.changeParameterIndexLeftButton.setDisabled(False)
        self.ui.changeParameterIndexRightButton.setDisabled(False)

    @thread
    def score(self, progressbar):
        self.disabled(True)
        progressbar.emit(0)
        defect = self.find_defect()
        if self.adaboost == 0:
            if self.currentLanguage == Language.Ru:
                self.ui.textBrowser.append('Сначала обучите модель.')
            if self.currentLanguage == Language.En:
                self.ui.textBrowser.append('Fit model first.')
            self.disabled(False)
            return None
        if self.adaboost.defect != defect:
            if self.currentLanguage == Language.Ru:
                self.ui.textBrowser.append('Модель не обучена для этого параметра.')
            if self.currentLanguage == Language.En:
                self.ui.textBrowser.append('The model is not trained for this parameter.')
            self.disabled(False)
            return None
        yada = self.adaboost.clf.predict(self.Xtesting)
        score = self.proc.getScore((self.ytesting), yada, mod='st') * 100
        score_f = self.proc.getScore((self.ytesting), yada, mod='F') * 100
        score_kkm = self.proc.getScore((self.ytesting), yada, mod='KKM') * 100
        if self.currentLanguage == Language.Ru:
            self.ui.textBrowser.append(
                'Точность модели AdaBoost  для параметра ' + defect + ' = ' + str(round(score, 2)) + '%')
            self.ui.textBrowser.append(
                'F мера для модели AdaBoost для дефекта' + defect + ' = ' + str(round(score_f, 2)))
            self.ui.textBrowser.append(
                'KKM мера для модели AdaBoost для дефекта' + defect + ' = ' + str(round(score_kkm, 2)))
        if self.currentLanguage == Language.En:
            self.ui.textBrowser.append(
                'The accuracy of the AdaBoost model for a parameter ' + defect + ' = ' + str(round(score, 2)) + '%')
            self.ui.textBrowser.append(
                'F measure for the AdaBoost model for a defect' + defect + ' = ' + str(round(score_f, 2)))
            self.ui.textBrowser.append(
                'KKM measure for AdaBoost model for defect' + defect + ' = ' + str(round(score_kkm, 2)))
        progressbar.emit(100)
        self.disabled(False)

    def disabled(self, mod):
        self.ui.centralwidget.setDisabled(mod)

    def sh_update_prog_bar(self, data):
        self.ui.progressBar.setValue(int(data))
        self.ui.progressBarModel.setValue(int(data))

    def sh_update_prog_bar_status(self, status):
        self.ui.labelProgresBarStatus.setText(status)
        self.ui.labelProgresBarStatusModel.setText(status)

    def sh_select_first_defect(self):
        if len(self.defects) != 0:
            self.ui.comboBoxDefects.setCurrentText(self.nameUnit[self.defects[0]][self.currentLanguage.value])

    def sh_param_index_set(self):
        if len(self.params) == 0:
            return
        self.ui.labelParam1.setText(
            struct_string(
                self.nameUnit[self.params[sorted(self.adaboost.indexes)[self.current_value_param_spinbox_index]][0]][
                    self.currentLanguage.value
                ]))
        self.ui.labelUnit1.setText(
            struct_string(
                self.nameUnit[self.params[sorted(self.adaboost.indexes)[self.current_value_param_spinbox_index]][0]][
                    3]))

    def sh_select_first_defect_model(self):
        if len(self.defects) != 0:
            self.ui.comboBoxDefectsModel.setCurrentText(self.defects[0])

    def sh_text_browser_update(self, data):
        if len(data) > 0:
            self.ui.textBrowser.append(data)
            self.ui.textBrowserModel.append(data)

    def sh_update_graph(self, data):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim([data[7][0], data[7][1]])
        ax.set_ylim([data[7][2], data[7][3]])
        ax.scatter((data[0]), (data[1]), 0, c='b', marker='o')
        ax.scatter((data[2]), (data[3]), 1, c='r', marker='+')
        ax.set_xlabel(self.ui.labelParam1.text() + ', ' + str(self.ui.labelUnit1.text()))
        ax.set_zlabel(self.ui.comboBoxDefects.currentText())
        plt.show()

    def roc_curve(self):
        if self.adaboost.defect != self.find_defect():
            if self.currentLanguage == Language.Ru:
                self.ui.textBrowser.append('Модель не обучена для этого параметра.')
            if self.currentLanguage == Language.En:
                self.ui.textBrowser.append('The model is not trained for this parameter.')
            self.disabled(False)
            return None

        res = self.adaboost.clf.predict_proba(self.Xtesting)
        y = self.ytesting
        res_pos_prob = []
        for i in range(len(res)):
            res_pos_prob.append((res[i][0], y[i]))
        res_pos_prob = sorted(res_pos_prob, key=lambda tup: tup[0])
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
        curvex.append(0)
        curvey.append(0)
        for i in range(len(res_pos_prob)):
            if res_pos_prob[i][1] == 1:
                ycoord += stepy
            else:
                xcoord += stepx
                s += ycoord * stepx
            xcoordline += xlinestep
            yline.append(xcoord)
            xline.append(xcoord)
            curvex.append(xcoord)
            curvey.append(ycoord)

        fig = plt.figure('ROC')
        ax = fig.gca()
        ax.plot(curvex, curvey, c='r')
        ax.plot(xline, yline, c='g')
        plt.show()
        if self.currentLanguage == Language.Ru:
            self.ui.textBrowser.append('Площадь под графиком ROC кривой равна ' + str(round(s, 4)))
        if self.currentLanguage == Language.En:
            self.ui.textBrowser.append('The area under the ROC curve is ' + str(round(s, 4)))

    def trends(self):
        self.disabled(True)
        trend_param = []
        trend_defect = []
        trend_predict = []
        time_list = []
        fig, (axParam, axExpertDef, axModelDef) = plt.subplots(3, 1)
        fig.canvas.set_window_title('Trends')
        if self.currentLanguage == Language.Ru:
            fig.suptitle('Тренды')
        if self.currentLanguage == Language.En:
            fig.suptitle('Trends')
        param = self.params[sorted(self.adaboost.indexes)[self.current_value_param_spinbox_index]][0]
        defect = list(self.nameUnit.keys())[(self.adaboost.id_defect - 1)]
        index_sort = sorted(self.adaboost.indexes)
        break_period_one_line = list()
        tmp_list = list()
        x = list()
        for row in self.x:
            curr_row = list()
            for el_index in index_sort:
                curr_row.append(row[el_index])
            x.append(np.array(curr_row))

        predict = self.adaboost.clf.predict(x)
        params = [par[0] for par in self.params]
        count = 0
        index_from, index_to = (-1, -1)
        first_in_row = True
        for i in range(len(self.time_list)):
            trend_param.append(self.x[i][params.index(param)])
            trend_defect.append(self.y[defect][i])
            trend_predict.append(predict[i])
            year_month_day = [int(x) for x in self.time_list[i].split(' ')[0].split('-')]
            hour_min_sec = [int(x) for x in self.time_list[i].split(' ')[1].split(':')]
            time_list.append(
                dt.datetime(year_month_day[0], year_month_day[1], year_month_day[2], hour_min_sec[0], hour_min_sec[1],
                            hour_min_sec[2]))
            if self.x[i][params.index(param)] == 0 or self.y[defect][i] == 0:
                break_period_one_line.append(2000)
                count += 1
                if first_in_row:
                    index_from = i
                    first_in_row = False
            else:
                first_in_row = True
                index_to = i
                break_period_one_line.append(0)
                if 0 < count < 1000:
                    for j in range(index_to)[index_from:index_to]:
                        break_period_one_line[j] = 0
                count = 0

        time_break_period = list(time_list)
        ind = 0
        break_periods = list()
        new_period = True
        if ind < len(break_period_one_line):
            if break_period_one_line[ind] == 0:
                del break_period_one_line[ind]
                del time_break_period[ind]
                new_period = True
            else:
                if new_period:
                    break_periods.append(list())
                    new_period = False
                break_periods[(-1)].append(break_period_one_line[ind])
                ind += 1

        bad_period_defect = list()
        time_bad_period_defect = list()
        good_period_defect = list()
        time_good_period_defect = list()
        is_first_good_element = True
        is_first_bad_element = True

        for ind_defect_value in range(len(trend_defect)):
            if trend_defect[ind_defect_value] >= self.limits[defect][1]:
                is_first_good_element = True
                time_bad_period_defect.append(time_list[ind_defect_value])
                if is_first_bad_element:
                    bad_period_defect.append(list())
                    bad_period_defect[(-1)].append(trend_defect[ind_defect_value])
                    is_first_bad_element = False
                else:
                    bad_period_defect[(-1)].append(trend_defect[ind_defect_value])
            else:
                is_first_bad_element = True
                time_good_period_defect.append(time_list[ind_defect_value])
                if is_first_good_element:
                    good_period_defect.append(list())
                    good_period_defect[(-1)].append(trend_defect[ind_defect_value])
                    is_first_good_element = False
                else:
                    good_period_defect[(-1)].append(trend_defect[ind_defect_value])

        max_value_param = max(trend_param)
        max_value_defect = max(trend_defect)
        time_index_start, time_index_final = (0, 0)
        for ind_good_defect_period in range(len(good_period_defect)):
            for ind_el in range(len(good_period_defect[ind_good_defect_period]))[:-1]:
                if good_period_defect[ind_good_defect_period][ind_el] != 0:
                    good_period_defect[ind_good_defect_period][ind_el + 1] = 0

            good_defect = [max_value_defect if value > 0 else 0 for value in good_period_defect[ind_good_defect_period]]
            good_param = [max_value_param if value > 0 else 0 for value in good_period_defect[ind_good_defect_period]]
            time_index_final = time_index_start + len(good_defect)
            good_pred = [1.1 if value > 0 else 0 for value in good_period_defect[ind_good_defect_period]]
            if time_index_start == 0:
                axParam.plot(time_good_period_defect[:time_index_final], good_param, '#90ee90')
                axExpertDef.plot(time_good_period_defect[:time_index_final], good_defect, '#90ee90')
                axModelDef.plot(time_good_period_defect[:time_index_final], good_pred, '#90ee90')
            else:
                if len(time_good_period_defect) == time_index_final:
                    axParam.plot(time_good_period_defect[time_index_start:], good_param, '#90ee90')
                    axExpertDef.plot(time_good_period_defect[time_index_start:], good_defect, '#90ee90')
                    axModelDef.plot(time_good_period_defect[time_index_start:], good_pred, '#90ee90')
                else:
                    axParam.plot(time_good_period_defect[time_index_start:time_index_final], good_param, '#90ee90')
                    axExpertDef.plot(time_good_period_defect[time_index_start:time_index_final], good_defect, '#90ee90')
                    axModelDef.plot(time_good_period_defect[time_index_start:time_index_final], good_pred, '#90ee90')
            time_index_start = time_index_final

        time_index_start, time_index_final = (0, 0)
        for ind_bad_defect_period in range(len(bad_period_defect)):
            for ind_el in range(len(bad_period_defect[ind_bad_defect_period]))[:-1]:
                if bad_period_defect[ind_bad_defect_period][ind_el] != 0:
                    bad_period_defect[ind_bad_defect_period][ind_el + 1] = 0

            bad_defect = [max_value_defect if value > 0 else 0 for value in bad_period_defect[ind_bad_defect_period]]
            bad_param = [max_value_param if value > 0 else 0 for value in bad_period_defect[ind_bad_defect_period]]
            time_index_final = time_index_start + len(bad_defect)
            good_pred = [1.1 if value > 0 else 0 for value in bad_period_defect[ind_bad_defect_period]]
            if time_index_start == 0:
                axParam.plot(time_bad_period_defect[:time_index_final], bad_param, '#FFC0CB')
                axExpertDef.plot(time_bad_period_defect[:time_index_final], bad_defect, '#FFC0CB')
                axModelDef.plot(time_bad_period_defect[:time_index_final], good_pred, '#FFC0CB')
            else:
                if len(time_bad_period_defect) == time_index_final:
                    axParam.plot(time_bad_period_defect[time_index_start:], bad_param, '#FFC0CB')
                    axExpertDef.plot(time_bad_period_defect[time_index_start:], bad_defect, '#FFC0CB')
                    axModelDef.plot(time_bad_period_defect[time_index_start:], good_pred, '#FFC0CB')
                else:
                    axParam.plot(time_bad_period_defect[time_index_start:time_index_final], bad_param, '#FFC0CB')
                    axExpertDef.plot(time_bad_period_defect[time_index_start:time_index_final], bad_defect, '#FFC0CB')
                    axModelDef.plot(time_bad_period_defect[time_index_start:time_index_final], good_pred, '#FFC0CB')
            time_index_start = time_index_final

        time_index_start, time_index_final = (0, 0)
        for ind_period in range(len(break_periods)):
            for ind_value in range(len(break_periods[ind_period]))[:-1]:
                if break_periods[ind_period][ind_value] != 0:
                    break_periods[ind_period][ind_value + 1] = 0
            else:
                break_period_param = [max_value_param if value > 0 else 0 for value in break_periods[ind_period]]
                break_period_defect = [max_value_defect if value > 0 else 0 for value in break_periods[ind_period]]
                break_period_pred = [1.1 if value > 0 else 0 for value in break_periods[ind_period]]
                time_index_final = time_index_start + len(break_period_param)
                if time_index_start == 0:
                    axParam.plot(time_break_period[:time_index_final], break_period_param, 'w')
                    axExpertDef.plot(time_break_period[:time_index_final], break_period_defect, 'w')
                    axModelDef.plot(time_break_period[:time_index_final], break_period_pred, 'w')
                else:
                    if len(time_break_period) == time_index_final:
                        axParam.plot(time_break_period[time_index_start:], break_period_param, 'w')
                        axExpertDef.plot(time_break_period[time_index_start:], break_period_defect, 'w')
                        axModelDef.plot(time_break_period[time_index_start:], break_period_pred, 'w')
                    else:
                        axParam.plot(time_break_period[time_index_start:time_index_final], break_period_param, 'w')
                        axExpertDef.plot(time_break_period[time_index_start:time_index_final], break_period_defect, 'w')
                        axModelDef.plot(time_break_period[time_index_start:time_index_final], break_period_pred, 'w')
                time_index_start = time_index_final

        limit = [self.limits[defect][1]] * len(trend_defect)
        axParam.plot(time_list, trend_param)
        axExpertDef.plot(time_list, trend_defect)
        axExpertDef.plot(time_list, limit)
        for index_predict in range(len(trend_predict))[:-1]:
            if trend_predict[index_predict] != 0:
                trend_predict[index_predict + 1] = 0
        axModelDef.plot(time_list, trend_predict)
        if self.currentLanguage == Language.Ru:
            axModelDef.set_ylabel('Прогнозируемое значение')
            axModelDef.set_xlabel('Время')
        if self.currentLanguage == Language.En:
            axModelDef.set_ylabel('predict')
            axModelDef.set_xlabel('date')
        axExpertDef.set_ylabel(struct_string(self.nameUnit[defect][self.currentLanguage.value], 30))
        axParam.set_ylabel(struct_string(self.nameUnit[param][self.currentLanguage.value], 30))
        plt.show()
        self.disabled(False)

    def changeParameterIndexRightButtonEvent(self):
        self.current_value_param_spinbox_index = min(self.current_value_param_spinbox_index + 1,
                                                     len(self.adaboost.indexes) - 1)
        param = self.params[sorted(self.adaboost.indexes)[self.current_value_param_spinbox_index]][0]

        self.ui.labelParam1.setText(struct_string(self.nameUnit[param][self.currentLanguage.value]))

        self.ui.labelUnit1.setText(self.nameUnit[param][3])

    def changeParameterIndexLeftButtonEvent(self):
        self.current_value_param_spinbox_index = max(self.current_value_param_spinbox_index - 1, 0)
        param = self.params[sorted(self.adaboost.indexes)[self.current_value_param_spinbox_index]][0]

        self.ui.labelParam1.setText(struct_string(self.nameUnit[param][self.currentLanguage.value]))

        self.ui.labelUnit1.setText(self.nameUnit[param][3])

    @thread
    def load_data(self, signal_pb, signal_pb_status, signal_text, signal_defect_combobox):
        self.disabled(True)
        self.nameUnit = read_names()
        self.limits = db_limits()
        time_from = self.ui.dateEditFrom.dateTime().toPyDateTime()
        time_to = self.ui.dateEditTo.dateTime().toPyDateTime()
        if time_to < time_from:
            if self.currentLanguage == Language.Ru:
                signal_text.emit('Неправильный интервал времени.')
            if self.currentLanguage == Language.En:
                signal_text.emit('Wrong time interval.')
            self.disabled(False)
            return

        if self.currentLanguage == Language.Ru:
            signal_pb_status.emit('Загрузка промышленных данных.')
        if self.currentLanguage == Language.En:
            signal_pb_status.emit('Download industrial data.')
        self.x, self.y, self.id_params, self.time_list = db_reader_from_to(str(time_from), str(time_to), signal_pb)
        try:
            self.ui.comboBoxDefects.clear()
            self.parameter = list(self.id_params.keys())
            self.defects = list(self.y.keys())
            for i in range(len(self.parameter)):
                if not self.parameter[i] in self.defects:
                    self.params.append((self.parameter[i], i))
            self.delete_const()
            signal_defect_combobox.emit()
            for defect in self.defects:
                if self.nameUnit[defect][self.currentLanguage.value] != 'nan':
                    self.ui.comboBoxDefects.addItem(
                        self.nameUnit[defect][self.currentLanguage.value]
                    )

        except:
            if self.currentLanguage == Language.Ru:
                signal_text.emit('Неверное содержание файла с данными.')
            if self.currentLanguage == Language.En:
                signal_text.emit('Invalid data file content.')

        signal_pb.emit(100)
        if self.currentLanguage == Language.Ru:
            signal_text.emit('Загрузка данных завершена.')
        if self.currentLanguage == Language.En:
            signal_text.emit('Data download is complete.')
        if self.adaboost != 0:
            self.ui.changeParameterIndexRightButton.setDisabled(False)
            self.ui.changeParameterIndexLeftButton.setDisabled(False)
            self.ui.trendButton.setDisabled(False)
        signal_defect_combobox.emit()
        self.ui.FitButton.setDisabled(False)
        self.ui.spinBoxEmumerator.setDisabled(False)
        self.disabled(False)

    @thread
    def load_dataModel(self, signal_pb, signal_pb_status, signal_text, signal_defect_combobox):
        self.disabled(True)
        self.nameUnit = read_names()
        self.limits = db_limits()
        time_from = self.ui.dateEditFromModel.dateTime().toPyDateTime()
        time_to = self.ui.dateEditToModel.dateTime().toPyDateTime()
        if time_to < time_from:
            if self.currentLanguage == Language.Ru:
                signal_text.emit('Неправильный интервал времени.')
            if self.currentLanguage == Language.En:
                signal_text.emit('Wrong time interval.')
            self.disabled(False)
            return

        if self.currentLanguage == Language.Ru:
            signal_pb_status.emit('Загрузка промышленных данных.')
        if self.currentLanguage == Language.En:
            signal_pb_status.emit('Download industrial data.')
        self.x, self.y, self.id_params, self.time_list = db_reader_from_to(str(time_from), str(time_to), signal_pb)
        try:
            self.ui.comboBoxDefects.clear()
            self.parameter = list(self.id_params.keys())
            self.defects = list(self.y.keys())
            for i in range(len(self.parameter)):
                if not self.parameter[i] in self.defects:
                    self.params.append((self.parameter[i], i))
            self.delete_const()
            signal_defect_combobox.emit()
            for defect in self.defects:
                if self.nameUnit[defect][self.currentLanguage.value] != 'nan':
                    self.ui.comboBoxDefects.addItem(
                        self.nameUnit[defect][self.currentLanguage.value]
                    )
        except:
            if self.currentLanguage == Language.Ru:
                signal_text.emit('Неверное содержание файла с данными.')
            if self.currentLanguage == Language.En:
                signal_text.emit('Invalid data file content.')
        signal_pb.emit(100)
        if self.currentLanguage == Language.Ru:
            signal_text.emit('Загрузка данных завершена.')
        if self.currentLanguage == Language.En:
            signal_text.emit('Data download is complete.')
        if self.adaboost != 0:
            self.ui.changeParameterIndexRightButton.setDisabled(False)
            self.ui.changeParameterIndexLeftButton.setDisabled(False)
            self.ui.trendButton.setDisabled(False)
        signal_defect_combobox.emit()
        self.disabled(False)

    def delete_const(self):
        defect = self.defects
        i = 0
        while i < len(self.defects):
            maxd = max(self.y[self.defects[i]])
            mind = min(self.y[self.defects[i]])
            if maxd == mind:
                defect.remove(self.defects[i])
            else:
                i += 1
        self.defects = defect
        # min_list = [float('inf')] * len(self.params)
        # max_list = [0] * len(self.params)
        # for row_ind in range(len(self.x)):
        #     for col_ind in range(len(self.x[row_ind])):
        #         min_list[col_ind] = min(min_list[col_ind], self.x[row_ind][col_ind])
        #         max_list[col_ind] = max(max_list[col_ind], self.x[row_ind][col_ind])
        # par_ind = 0
        # while par_ind < len(self.params):
        #     if max_list[par_ind] == max_list[par_ind]:
        #         self.params.remove(self.params[par_ind])
        #     else:
        #         par_ind += 1

    def save_model(self):
        write_model_db(self.adaboost, self.adaboost.count_enumerators, self.adaboost.id_defect,
                       self.ui.dateEditFrom.dateTime().toPyDateTime(), self.ui.dateEditTo.dateTime().toPyDateTime())
        if self.currentLanguage == Language.Ru:
            self.ui.textBrowser.append('Модель успешно сохранена.')
        if self.currentLanguage == Language.En:
            self.ui.textBrowser.append('Model saved.')

    def find_defect(self, current_defect=None):
        if current_defect is None:
            current_defect = self.ui.comboBoxDefects.currentText()
        defect = current_defect
        for row in range(len(self.nameUnit)):
            row_defect = list(self.nameUnit.keys())[row]
            if current_defect == self.nameUnit[row_defect][self.currentLanguage.value]:
                return row_defect
        return None

    def refresh_model(self):
        self.ui.comboBoxDefectsModel.clear()
        self.nameUnit = read_names()
        defect_model = read_params_model()
        id_params = read_params()
        params = dict()
        for x in id_params:
            params[x[0]] = x[1]

        for defect_id in defect_model.keys():
            self.ui.comboBoxDefectsModel.addItem(self.nameUnit[params[defect_id]][self.currentLanguage.value])
        self.ui.loadModelButton.setDisabled(False)

    def change_comboBoxDefectsModel(self):
        self.ui.comboBoxTimeModel.clear()
        defect_model = read_params_model()
        id_params = read_params()
        params = dict()
        for x in id_params:
            params[x[1]] = x[0]

        defect = self.find_defect(self.ui.comboBoxDefectsModel.currentText())
        if not defect or len(defect) == 0:
            return
        index = params[defect]
        if len(defect) > 0:
            for count in defect_model[index]:
                self.ui.comboBoxTimeModel.addItem(str(count))

    def change_comboBoxTimeModel(self):
        self.ui.comboBoxCountModel.clear()
        defect_model = read_params_model()
        id_params = read_params()
        params = dict()
        for x in id_params:
            params[x[1]] = x[0]
        else:
            defect = self.find_defect(self.ui.comboBoxDefectsModel.currentText())
            if not defect or len(defect) == 0:
                return
            index = params[defect]
            time_from_to = self.ui.comboBoxTimeModel.currentText()
            if len(time_from_to) > 0:
                if len(defect) > 0:
                    for count in defect_model[index][time_from_to]:
                        self.ui.comboBoxCountModel.addItem(str(count))

    def load_model(self):
        defect = self.find_defect(self.ui.comboBoxDefectsModel.currentText())
        defect_id = list(self.nameUnit.keys()).index(defect) + 1
        count_est = self.ui.comboBoxCountModel.currentText()
        time_list = self.ui.comboBoxTimeModel.currentText().split(' ')
        time_from = datetime.strptime(f"{time_list[0]} {time_list[1]}", '%Y-%m-%d %H:%M:%S')
        time_to = datetime.strptime(f"{time_list[2]} {time_list[3]}", '%Y-%m-%d %H:%M:%S')
        model = read_model(defect_id, count_est, time_from, time_to)
        from bitstring import BitArray
        b = BitArray(model[0])
        byte = b.tobytes()
        import pickle
        if model:
            self.adaboost = pickle.loads(byte)
        if len(self.x) != 0:
            self.ui.trendButton.setDisabled(False)
            self.ui.changeParameterIndexRightButton.setDisabled(False)
            self.ui.changeParameterIndexLeftButton.setDisabled(False)

        if self.currentLanguage == Language.Ru:
            self.signal_text.emit('Модель успешно загружена.')
        if self.currentLanguage == Language.En:
            self.signal_text.emit('The model has been loaded successfully.')
