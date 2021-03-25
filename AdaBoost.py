import numpy as np
import random
from sklearn.ensemble import AdaBoostClassifier


class AdaBoost:

    def __init__(self, x, y, defect, limits, count=100):
        self.count_enumerators = count
        self.clf = 0
        self.X = x
        self.Xfiting = []
        self.Xtesting = []
        self.y = []
        for el in y:
            self.y.append(el)
        self.yfiting = []
        self.ytesting = []
        self.defect = defect
        self.limits = limits

    def fit(self, signals):
        if len(self.X) == 0:
            return
        signals.emit(0)
        for i in range(len(self.y)):
            if np.isnan(self.y[i]):
                self.y[i] = 0
        y_crit = self.limits[self.defect][1]
        for i in range(len(self.y)):
            if self.y[i] >= y_crit:
                self.y[i] = 1
            else:
                self.y[i] = 0

        for a in range(len(self.X)):
            if random.random() <= 0.8:  # разделение выборок
                self.Xfiting.append(self.X[a])
                self.yfiting.append(self.y[a])
            else:
                self.Xtesting.append(self.X[a])
                self.ytesting.append(self.y[a])
        clf = AdaBoostClassifier(n_estimators=self.count_enumerators, learning_rate=1,
                                 random_state=int(random.random() * 4294967295))
        clf.fit(self.Xfiting, self.yfiting)
        self.clf = clf
        signals.emit(100)
        return

    def score(self, signals, signal_text):
        signals.emit(0)
        try:
            for i in range(len(self.clf)):
                result = self.clf[list(self.clf.keys())[i]].score(self.Xtesting[list(self.clf.keys())[i]]
                                                                  , self.ytesting[list(self.clf.keys())[i]])
                signal_text.emit('Score ' + str(list(self.clf.keys())[i]) + ' = ' + str(round(result, 5)))
                signals.emit(int((i + 1) / len(self.defects) * 100))
        except AttributeError:
            raise Exception('This model does not fit for this data.')
        return

    def setX(self, x):
        self.Xtesting = x

    def sety(self, y):
        self.ytesting = y
