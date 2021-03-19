import math
import numpy as np


class DataProcess:
    # удаление nan значений из списка
    def delete_nan(self, array):
        return [x for x in array if str(x) != 'nan']

    # синхронизация данных по времени
    def synchronization(self, delay, params, defects, df, y):
        arr = {}
        delay_step = 10
        max_delay = 0
        min_delay = float('inf')
        for el in delay.values():
            if el[0] > max_delay:
                max_delay = el[0]
            if el[0] < min_delay:
                min_delay = el[0]

        max_delay = math.ceil(max_delay / delay_step)
        for i in range(len(params)):
            q = math.ceil(delay[params[i][0]][0] / delay_step)
            arr[params[i][0]] = np.array(df[params[i][0]][max_delay - q:-q - min_delay - 1])
        for i in range(len(defects)):
            y[defects[i]] = np.array(y[defects[i]][max_delay:-min_delay - 1])

            #size = min(len(arr[0]),len(y[0]))
            #arr = arr[:size]
            #y = y[:size]
        return arr, y

    # создание матрицы данных для обучения
    def build_2D_list(self, delay, params, defect, name_unit, df, y):
        arr, y = self.synchronization(delay, params, defect, df, y)
        x = []
        for i in range(len(arr[params[0][0]])):
            xi = []
            for j in range(len(params)):
                xi.append(max(arr[params[j][0]][i], name_unit[params[j][0]][3]))
            x.append(xi)
        return np.array(x), y

    # заполнение пропусков данных параметров предыдущими значениями
    def build_list(self, array):
        res = []
        for i in range(len(array)):
            if i>3500:
                q = array[i]
            if array[i] == '               ' or str(array[i]) == 'nan' or array[i] == float('nan'):
                res.append(np.float64('nan'))
            else:

                res.append(np.float64(str(array[i]).replace(',', '.')))
        res = np.array(res)
        value = 0
        for i in range(len(res)):
            if ~np.isnan(res[i]):
                value = res[i]
                break
        for i in range(len(res)):
            if np.isnan(res[i]):
                res[i] = value
            else:
                value = res[i]
        return res

    def getScore(self, expert, model, mod='F', betta=1):

        if mod == 'st':
            count = 0
            for i in range(len(expert)):
                if model[i] == expert[i]:
                    count += 1
            return count/len(expert)
        elif mod == 'e1':
            count = 0
            for i in range(len(expert)):
                if model[i] == 1 and expert[i] == 0:
                    count += 1
            return count / len(expert), count
        elif mod == 'e2':
            count = 0
            for i in range(len(expert)):
                if model[i] == 0 and expert[i] == 1:
                    count += 1
            return count / len(expert), count
        elif mod == 'F' or mod == 'KKM':
            TP = TN = FP = FN = 0
            for i in range(len(expert)):
                if model[i] == 0 and expert[i] == 0:
                    TN += 1
                if model[i] == 0 and expert[i] == 1:
                    FN += 1
                if model[i] == 1 and expert[i] == 0:
                    FP += 1
                if model[i] == 1 and expert[i] == 1:
                    TP += 1
            precision = TP / (TP+FP)
            recall = TP / (TP+FN)
            if mod =='F':
                F = (betta**2+1)*(precision*recall)/(precision+recall)
                return F
            elif mod == 'KKM':
                KKM = (TP*TN-FP*FN)/((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**0.5
                return KKM
        else:
            return None
