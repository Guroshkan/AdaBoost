import datetime, math, sqlite3, time
import logging

par_name = 1
PATH = 'extcalandAda.db'

def db_reader(count):
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT IdParameter, ParameterCode ,IdParameterType FROM Parameters')
    par = cursor.fetchall()
    params = []
    for el in par:
        if el[1].split('.')[(-1)] != 'predict':
            params.append(el)
        dict = {}
        df = {}
        df['DateTime'] = []

    for el in params:
        cursor.execute('SELECT DateTime,Value FROM ParameterValues WHERE IdParameter ==%(value)s  LIMIT(%(count)s)' % {'value':str(el[0]), 
         'count':count})
        results = cursor.fetchall()
        dict[el[1]] = results
        df[el[1]] = []
    else:
        for el in dict[params[5][1]]:
            df['DateTime'].append(el[0])
        else:
            df_last = {}
            for p in params:
                df_last[p[1]] = 0
            else:
                for p in params:
                    for i in range(len(df['DateTime'])):
                        if df['DateTime'][i] == dict[p[1]][df_last[p[1]]][0]:
                            df[p[1]].append(dict[p[1]][df_last[p[1]]][1])
                            df_last[p[1]] += 1
                        else:
                            df[p[1]].append('nan')
                    else:
                        for el in list(df.keys())[1:]:
                            df[el] = [round(float(x), 4) for x in df[el]]
                        else:
                            conn.close()
                            return (
                             df, params)


def db_reader_from_to(timeFrom, timeTo, signal_pb):
    params_row = read_params()
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    size = int(cursor.execute(f"select count(DISTINCT DateTime) from ParameterValues where DateTime > '{timeFrom}' and DateTime < '{timeTo}'").fetchall()[0][0])
    step_update = int(size / 100)
    id_params = dict()
    params = list()
    defects = list()
    y = dict()
    x = list()
    for row_id in range(len(params_row)):
        params.append(params_row[row_id][1])
        id_params[params_row[row_id][1]] = params_row[row_id][0]
        if params_row[row_id][1].split('.')[0] == 'Defects':
            defects.append(params_row[row_id][1])
            y[params_row[row_id][1]] = list()
    cursor.execute(f""
                   f"select "
                   f"pv.DateTime,group_concat(p.ParameterCode || ': ' || pv.Value, ',') "
                   f"from "
                   f"ParameterValues as pv "
                   f"left join "
                   f"Parameters as p on p.idParameter = pv.idParameter "
                   f"where "
                   f"DateTime between '{timeFrom}' and '{timeTo}' "
                   f"and p.IdParameterType == 2  or "
                   f"DateTime between '{timeFrom}' and '{timeTo}' "
                   f"and p.IdParameterType == 3 "
                   f"group by pv.DateTime ")
    time_list = list()
    iter = 0
    avg_list = [0] * len(params)
    count_values = [0] * len(params)
    while True:
        iter += 1
        if iter % step_update == 0:
            signal_pb.emit(int(iter / size * 100))
        row = cursor.fetchone()

        if row:
            row_time = row[0]
            parameters_list = row[1].split(',')
            row_values = [float('nan')] * len(params)
            for element in parameters_list:
                dict_element = element.split(':')
                ind = params.index(dict_element[0])
                row_values[ind] = round(float(dict_element[1]), 4)

            for i in range(len(row_values)):
                if not math.isnan(row_values[i]):
                    avg_list[i] += row_values[i]
                    count_values[i] += 1

            if not if_nan_in_list(row_values):
                time_list.append(row_time)
                x.append(list())
                for j in range(len(params)):
                    if params[j] in defects:
                        y[params[j]].append(avg_list[j] / max(1, count_values[j]))
                    else:
                        x[(-1)].append(avg_list[j] / max(1, count_values[j]))
                count_values = [0] * len(params)
                avg_list = [0] * len(params)

        else:
            break

    return (x, y, id_params, time_list)


def db_limits():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT IdParameter, LowLimitValue, HighLimitValue FROM Limits order by IdParameter ')
    lim = cursor.fetchall()
    cursor.execute('SELECT IdParameter, ParameterCode FROM Parameters')
    param = cursor.fetchall()
    limits = {}
    params = []
    for el in param:
        if el[1].split('.')[(-1)] != 'predict':
            params.append(el)
        for i in range(len(params)):
            min = float('nan') if lim[i][1] is None else float(lim[i][1])
            max = float('nan') if lim[i][2] is None else float(lim[i][2])
            limits[param[i][1]] = (min, max)
        else:
            conn.close()
    return limits


def read_names():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT \n                        p.ParameterCode, \n                        p.ParameterNameRu, \n                        p.ParameterNameEng, \n                        p.Symbol, \n                        u.Sign \n                    FROM \n                        Parameters as p\n                    JOIN\n                        Units as u\n                    WHERE p.IdUnit == u.IdUnit ')
    names = cursor.fetchall()
    namesUnit = {}
    for parameter in names:
        namesUnit[parameter[0]] = [
         parameter[1], parameter[2], parameter[3], parameter[4]]
    else:
        conn.close()
        return namesUnit


def write_predict_db(time, predictValue):
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT max(IdParameterValue) FROM ParameterValues')
    maxIndex = cursor.fetchall()
    cursor.execute('SELECT IdParameter, ParameterCode ,IdParameterType FROM Parameters')
    par = cursor.fetchall()
    params = []
    for el in par:
        if el[1].split('.')[(-1)] == 'predict':
            params.append(el)


def findTimeRange():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT max(DateTime) FROM ParameterValues where LENGTH(DateTime) = LENGTH ('yyyy-mm-dd hh:mm:ss')")
    maxDate = cursor.fetchall()
    cursor.execute("SELECT min(DateTime) FROM ParameterValues where LENGTH(DateTime) = LENGTH ('yyyy-mm-dd hh:mm:ss')")
    minDate = cursor.fetchall()
    max = str(maxDate[0][0])
    min = str(minDate[0][0])
    return (max, min)


def write_model_db(clf, count, id_parameter, timeFrom, timeTo):
    import pickle
    b = pickle.dumps(clf)
    from bitstring import BitArray
    a = BitArray(bytes=b)
    str1 = '0x' + ''.join([bit for bit in a.hex])
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT IdModel FROM ParameterModel WHERE IdParameter = {id_parameter} AND CountEst = {count} and TimeFrom = '{timeFrom}' and TimeTo = '{timeTo}'")
    id_model = cursor.fetchall()
    if len(id_model) > 0:
        c = f"DELETE FROM ParameterModel WHERE IdModel = {id_model[0][0]}"
        cursor.execute(f"DELETE FROM ParameterModel WHERE IdModel = {id_model[0][0]}")
    else:
        conn.commit()
        if len(id_model) > 0:
            cursor.execute(f"INSERT INTO ParameterModel (IdModel,IdParameter,CountEst,Model,TimeFrom, TimeTo) Values ({id_model[0][0]},{id_parameter},{count},'{str1}','{timeFrom}','{timeTo}')")
        else:
            cursor.execute(f"INSERT INTO ParameterModel (IdParameter,CountEst,Model,TimeFrom, TimeTo) Values ({id_parameter},{count},'{str1}','{timeFrom}','{timeTo}')")
    conn.commit()
    conn.close()


def read_params_model():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    id_par, time_from, time_to, count_est = (0, 1, 2, 3)
    cursor.execute('SELECT IdParameter, TimeFrom, TimeTo, CountEst from ParameterModel')
    params = cursor.fetchall()
    parameter_dict_count = dict()
    a = str(params[0][time_from])
    for parameter in params:
        if parameter_dict_count.get(parameter[id_par], None):
            if parameter_dict_count[parameter[id_par]].get(f"{parameter[time_from]} {parameter[time_to]}", None):
                parameter_dict_count[parameter[id_par]][f"{parameter[time_from]} {parameter[time_to]}"].append(parameter[count_est])
            else:
                parameter_dict_count[parameter[id_par]][f"{parameter[time_from]} {parameter[time_to]}"] = list()
                parameter_dict_count[parameter[id_par]][f"{parameter[time_from]} {parameter[time_to]}"].append(parameter[count_est])
        else:
            parameter_dict_count[parameter[id_par]] = dict()
            if parameter_dict_count[parameter[id_par]].get(f"{parameter[time_from]} {parameter[time_to]}", None):
                parameter_dict_count[parameter[id_par]][f"{parameter[time_from]} {parameter[time_to]}"].append(parameter[count_est])
            else:
                parameter_dict_count[parameter[id_par]][f"{parameter[time_from]} {parameter[time_to]}"] = list()
                parameter_dict_count[parameter[id_par]][f"{parameter[time_from]} {parameter[time_to]}"].append(parameter[count_est])
    else:
        return parameter_dict_count


def read_params():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT IdParameter, ParameterCode FROM Parameters WHERE IdParameterType == 2 or IdParameterType == 3')
    params_row = cursor.fetchall()
    cursor.close()
    conn.close()
    return params_row


def read_defects():
    id_defects = dict()
    params_row = read_params()
    for row in params_row:
        if row[1].split('.')[0] == 'Defects':
            id_defects[row[1]] = row[0]
        return id_defects


def read_model(id_param, count_est, time_from, time_to):
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT Model FROM ParameterModel WHERE IdParameter = {id_param} AND CountEst = {count_est} AND TimeFrom = '{time_from}' AND TimeTo = '{time_to}'")
    model = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(model) > 0:
        return model[0]


def if_nan_in_list(array):
    for el in array:
        if el != el:
            return True
    return False
