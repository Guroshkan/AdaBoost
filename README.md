# AdaBoost

Описание файлов с данными

data.ods,data2000.ods - excel файлы с промышленными данными. data2000 - имеет первые 2000 записей файла data.

delays.ods - excel файл с данными о временных задержках параметров.

relations.ods - excel файл с данными о зависимостях. На пересечении строки-дефекта и столбца-параметра выставляется "*", если данный дефект зависит от данного параметра

UnitNameParams.ods - excel файл с названиями и единицами измерения параметров.

AdaBoost.txt - сохраненная модель adaboost

data.txt - dataframe - производственные данные.

Руководство по использованию с комментариями.

1.После открытия необходимо загрузить данные. Для этого нужно нажать кнопку Load Data и выбрать файл data.ods, data1 2000.ods, data2000.ods,excel_data_df.txt(см. п.5.) или аналогичный, содержащий производственные данные. Во время загрузки программа может подвиснуть, так как загрузка производится в том же потоке, в котором запущен графический интерфейс(исправится в следующих версиях программы).

2.Программа будет использовать для обработки данные из файлов по умолчанию: delays.ods (данные о задержках), relations.ods(данные о зависимостях дефектов от определенных параметров), UnitNameParams(таблица с названиями параметров и их единицами измерения). Можно заменить эти файлы во вкладке Settings. После изменения - программа сразу попробует загрузить из них данные.
После загрузки данных - необходимо обучить м.м. программы. Для этого нужно нажать на кнопку FitModel. Изменить количество базовых классификаторов можно в поле countEnumerators.
После обучения можно проверить точность модели(кнопка Score). Будут представленны данные о точности прогнозирования, а так же о количестве ошибок 2го рода.

3.Можно построить график зон качества, от параметров процесса. Для этого необходимо выбрать два параметра, не равные друг другу, и нажать кнопку Plot 3d. Можно увеличить количество точек в графике. Для этого необходимо изменить параметр resolution. Выбрать дефект для которого будет строится график в поле  Defects из списка предложенных.

4.Чтобы сохранить/загрузить обученную модель - необходимо нажать кнопку Save Model/Load Model. Модель сохраняется при помощи функции Dump(чтобы ускорить загрузку данные в программу).

5.Сохранить загруженные данные можно так же при помощи функции Dump при нажатии на кнопку Save Data.(Загрузить его можно при нажатии на Load Data). Уже есть сохраненные в "Dump" формате данные из файла data.ods.

6.Сравнить модель адаптивного бустинга можно с моделью градиентного бустинга из библиотеки CatBoost по нажатии на кнопку Compare.


Стандартная проверка работы:

- Нажать Load Data и загрузить excel_data_df.txt (или data.ods - это одно и то же, просто ods открывается в 100 раз дольше);

- Обучить модель, нажав кнопку Fit Model;

- Проверить точность нажав кнопку Score;

- Построить области качества, нажав кнопку Plot3d;

- Сравнить точность нажав кнопку Compare.


