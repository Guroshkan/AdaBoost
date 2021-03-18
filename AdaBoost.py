import numpy as np
import random
from sklearn.ensemble import AdaBoostClassifier
class AdaBoost:
    def __init__(self, x, y, defects, params, count=100):
        self.count_enumerators = count
        self.clf = {}
        self.X = x
        self.Xfiting = {}
        self.Xtesting = {}
        self.y = y
        self.yfiting = {}
        self.ytesting = {}
        self.clf = {}
        self.defects = defects
        self.params = params

    def fit(self, signals):
        if len(self.X) == 0:
            return
        signals.emit(0)
        for d in range(len(self.defects)):
            for i in range(len(self.y[self.defects[d]])):
                if np.isnan(self.y[self.defects[d]][i]):
                    self.y[self.defects[d]][i] = 0
            miny = min(self.y[self.defects[d]])
            maxy = max(self.y[self.defects[d]])
            y_crit = miny + 0.6*(maxy - miny)
            y_crit = 0
            for i in range(len(self.y[self.defects[d]])):
                y_crit += self.y[self.defects[d]][i]
            y_crit /= len(self.y[self.defects[d]])
            y_crit = y_crit/1
            for i in range(len(self.y[self.defects[d]])):
                if self.y[self.defects[d]][i] >= y_crit:
                    self.y[self.defects[d]][i] = 1
                else:
                    self.y[self.defects[d]][i] = 0
        for i in range(len(self.defects)):
            self.ytesting[list(self.y.keys())[i]] = []
            self.yfiting[list(self.y.keys())[i]] = []
            self.Xtesting[list(self.y.keys())[i]] = []
            self.Xfiting[list(self.y.keys())[i]] = []
            for a in range(len(self.X)):
                if random.random() <= 0.8:
                    self.Xfiting[self.defects[i]].append(self.X[a])
                    self.yfiting[self.defects[i]].append(self.y[self.defects[i]][a])
                else:
                    self.Xtesting[self.defects[i]].append(self.X[a])
                    self.ytesting[self.defects[i]].append(self.y[self.defects[i]][a])
            clf = AdaBoostClassifier(n_estimators=self.count_enumerators, learning_rate=1, random_state=0)
            clf.fit(self.Xfiting[self.defects[i]], self.yfiting[self.defects[i]])
            self.clf[self.defects[i]] = clf
            signals.emit(int((i+1)/len(self.defects)*100))
        #signals.emit(int(100))
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