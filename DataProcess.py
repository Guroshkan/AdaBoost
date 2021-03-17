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
            if array[i] == '               ':
                res.append(np.float64('nan'))
            elif str(array[i]) == 'nan':
                continue
            else:
                res.append(np.float64(array[i]))
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
