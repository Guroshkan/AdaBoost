import numpy as np

class DataProcess:

    def normilize_y(self, limit, y):
        defect = list(y.keys())
        for dfct in defect:
            y[dfct] = np.array(y[dfct])
            for i in range(len(y)):
                if y[dfct][i] < limit[dfct][0]:
                    y[dfct][i] = limit[defect][0]
            else:
                return y

    def build_list(self, array):
        res = []
        for i in range(len(array)):
            if array[i] == '               ' or str(array[i]) == 'nan' or array[i] == float('nan'):
                res.append(np.float64('nan'))
            else:
                res.append(np.float64(str(array[i]).replace(',', '.')))
        else:
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
                else:
                    return res

    def getScore(self, expert, model, mod='F', betta=1):
        if mod == 'st':
            count = 0
            for i in range(len(expert)):
                if model[i] == expert[i]:
                    count += 1
            return count / len(expert)
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

            if mod == 'F':
                precision = TP / max((TP + FP), 1)
                recall = TP / max((TP + FN), 1)
                try:
                    F = (betta ** 2 + 1) * (precision * recall) / (betta ** 2 * precision + recall)
                    return abs(F)
                except:
                    return 0
            elif mod == 'KKM':
                try:
                    KKM = (TP * TN - FP * FN) / ((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)) ** 0.5
                    return abs(KKM)
                except:
                    return 0
        else:
            return None

def struct_string( string, lenth = 50):
    if len(string) <= lenth:
        return string
    list_strings = string.split(' ')
    row_string = str()
    result_string = str()
    for word in list_strings:
        if len(row_string) + len(word) <= lenth:
            row_string += f' {word}'
        else:
            result_string += f' {row_string} \n'
            row_string = word
    result_string += f' {row_string} \n'
    return result_string
