import pickle
from AdaBoost import *


class File:
    def __init__(self, ui):
        self.ui = ui

    # выгрузка данных в файл
    def dump_data(self, path, data, mod='wb'):
        with open(path, mod)as f:
            pickle.dump(data, f)

    # загрузка данных из файла
    def load_data_from_dump(self, path, mod='rb'):
        with open(path, mod) as f:
            return pickle.load(f)

    # сохранение промышленных данных в файл
    def save_data(self, file_name, df):
        self.dump_data(file_name, df)

    # сохранение обученной модели в файл
    def save_model(self, file_name):
        self.dump_data(file_name, self.adaboost)

    # загрузка обученной модели из файла
    def load_model(self, file_name, df_size):
        try:
            self.adaboost = self.load_data_from_dump(file_name)
            if df_size > 0:
                self.ui.predictButton_3.setDisabled(False)
                self.ui.Plot3d_3.setDisabled(False)
            return self.adaboost
        except:
            self.ui.textBrowser_3.append('Неверный формат данных.')
