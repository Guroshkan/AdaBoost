# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: C:\Users\acer nitro 5\PycharmProjects\AdaBoostVisualDemo lib\AdaBoost.py
# Compiled at: 2021-05-10 06:11:37
# Size of source mod 2**32: 3836 bytes
import numpy as np, random
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression

class AdaBoost:

    def __init__(self, defect, limits, id_defect, count=100, clf=0):
        self.count_enumerators = count
        self.clf = clf
        self.id_defect = id_defect
        self.defect = defect
        self.limits = limits
        self.count_params = 5

    def fit(self, x_, y_, signal_pb):
        signal_pb.emit(0)
        coef = self.logistic_regression(x_, y_)
        x = self.cut_unimportant_x(coef, x_)
        y = np.array(y_)
        if len(x_) == 0:
            return
        signal_pb.emit(50)
        for i in range(len(y)):
            if np.isnan(y[i]):
                y[i] = 0
        else:
            y_crit = self.limits[self.defect][1]

        for i in range(len(y)):
            if y[i] >= y_crit:
                y[i] = 1
            else:
                y[i] = 0
        else:
            x_testing = list()
            x_fiting = list()
            y_testing = list()
            y_fiting = list()
            for i in range(len(y)):
                if random.random() <= 0.8:
                    x_fiting.append(x[i])
                    y_fiting.append(y[i])
                else:
                    x_testing.append(x[i])
                    y_testing.append(y[i])
            else:
                clf = AdaBoostClassifier(n_estimators=(self.count_enumerators), learning_rate=1, random_state=(int(random.random() * 4294967295)))
                clf.fit(x_fiting, y_fiting)
                self.clf = clf
                signal_pb.emit(100)
                return x_fiting, y_fiting, x_testing, y_testing

    def score(self, signals, signal_text):
        signals.emit(0)
        try:
            for i in range(len(self.clf)):
                result = self.clf[list(self.clf.keys())[i]].score(self.Xtesting[list(self.clf.keys())[i]], self.ytesting[list(self.clf.keys())[i]])
                signal_text.emit('Score ' + str(list(self.clf.keys())[i]) + ' = ' + str(round(result, 5)))
                signals.emit(int((i + 1) / len(self.defects) * 100))

        except AttributeError:
            raise Exception('This model does not fit for this data.')

    def setX(self, x):
        self.Xtesting = x

    def sety(self, y):
        self.ytesting = y

    def logistic_regression(self, x, y_):
        y = list()
        for el in y_:
            y.append(el)
        else:
            from sklearn import linear_model
            clf = linear_model.Lasso(alpha=0.8)
            clf.fit(x, y)
            a = clf.predict(x)
            b = clf.score(x, y)
            coef = clf.coef_
            return coef

    def cut_unimportant_x(self, coef, x_):
        self.indexes = self.find_indexes_important_x(coef)
        index_sort = sorted(self.indexes)
        x = list()
        for row in x_:
            curr_row = list()
            for el_index in index_sort:
                curr_row.append(row[el_index])
            else:
                x.append(np.array(curr_row))

        else:
            return np.array(x)

    def find_indexes_important_x(self, coef):
        coef = [abs(c) for c in coef]
        sort_coef = sorted(coef, reverse=True)
        indexes_list = list()
        for counter in range(self.count_params):
            indexes_list.append(coef.index(sort_coef[counter]))
            sort_coef.remove(sort_coef[counter])
        else:
            return indexes_list