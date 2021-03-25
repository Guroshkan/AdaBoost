import sqlite3



def db_reader(count):
    conn = sqlite3.connect('extcaland.db')
    cursor = conn.cursor()
    cursor.execute("SELECT IdParameter, ParameterCode ,IdParameterType FROM Parameters")
    par = cursor.fetchall()
    params = []
    for el in par:
        if el[1].split('.')[-1]!='predict':
            params.append(el)
    dict={}
    df = {}
    df['DateTime']=[]
    for el in params:
        cursor.execute("SELECT DateTime,Value FROM ParameterValues WHERE IdParameter ==%(value)s  LIMIT(%(count)s)"%{"value": str(el[0]), "count": count})
        results = cursor.fetchall()
        dict[el[1]]=results
        df[el[1]]=[]
        print (el[0])
    for el in dict[params[5][1]]:
        df['DateTime'].append(el[0])
    df_last={}
    for p in params:
        df_last[p[1]]=0

    for p in params:
        print("i = %(i)s" % {"i": str(p[0])})
        for i in range(len(df['DateTime'])):
            if df['DateTime'][i]==dict[p[1]][df_last[p[1]]][0]:
                df[p[1]].append(dict[p[1]][df_last[p[1]]][1])
                df_last[p[1]]+=1
            else:
                df[p[1]].append('nan')
    '''for p in params:
        for i in range(len(df['DateTime'])):
            print("i = %(i)s"%{"i":str(i)})
            df[p[1]].append('nan')
            for j in range(len(dict[p[1]]))[:i]:
                if df['DateTime'][i]==dict[p[1]][j][0]:
                    prevj=j
                    df[p[1]][i]=dict[p[1]][j][1]
                    break'''

    for el in list(df.keys())[1:]:
        df[el]=[round(float(x),4) for x in df[el]]
    conn.close()

    return df,params


def db_limits():
    conn = sqlite3.connect('extcaland.db')
    cursor = conn.cursor()
    cursor.execute("SELECT IdParameter, LowLimitValue, HighLimitValue FROM Limits")
    lim = cursor.fetchall()
    cursor.execute("SELECT IdParameter, ParameterCode FROM Parameters")
    param = cursor.fetchall()
    limits = {}
    params = []
    for el in param:
        if el[1].split('.')[-1] != 'predict':
            params.append(el)
    for i in range(len(params)):
        limits[param[i][1]] = (float(lim[i][1]), float(lim[i][2]))

    conn.close()
    return limits

def write_predict_db( time, predictValue):
    conn = sqlite3.connect('extcaland.db')
    cursor = conn.cursor()
    cursor.execute("SELECT max(IdParameterValue) FROM ParameterValues")
    maxIndex = cursor.fetchall()

    cursor.execute("SELECT IdParameter, ParameterCode ,IdParameterType FROM Parameters")
    par = cursor.fetchall()
    params = []
    for el in par:
        if el[1].split('.')[-1] == 'predict':
            params.append(el)
