import numpy as np


class DataProcess:
    # создание матрицы данных для обучения
    def build_2D_list(self, params, defect, limit, df, y):
        arr = {}
        for i in range(len(params)):
            arr[params[i][0]] = np.array(df[params[i][0]])
        x = []
        for i in range(len(arr[params[0][0]])):
            xi = []
            for j in range(len(params)):
                value = arr[params[j][0]][i]
                if value < limit[params[j][0]][0]:
                    value = limit[params[j][0]][0]
                if value > limit[params[j][0]][1] :
                    value = limit[params[j][0]][1]
                xi.append(value)
            x.append(xi)

        for dfct in defect:
            for i in range(len(y)):
                if y[dfct][i] < limit[dfct][0]:
                    y[dfct][i] = limit[defect][0]
                if y[dfct][i] > limit[dfct][1]:
                    y[dfct][i] = limit[defect][1]
        return np.array(x), y

    # заполнение пропусков данных параметров предыдущими значениями
    def build_list(self, array):
        res = []
        for i in range(len(array)):
            if i > 3500:
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

            if mod =='F':
                precision = TP / max((TP + FP), 1)
                recall = TP / max((TP + FN), 1)
                try:
                    F = (betta**2+1)*(precision*recall)/(betta**2*precision+recall)
                    return F
                except:
                    return 0
            elif mod == 'KKM':
                try:
                    KKM = (TP*TN-FP*FN)/((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**0.5
                    return KKM
                except:
                    return 0
        else:
            return None
