from datetime import datetime, timedelta
from pandas as pd
import process


def advice(a, days=7):

    if(a.upload):
        data=a.data_schedule

    else:
        return "Вам стоит больше заботиться о себе"

    data.date = pd.to_datetime(data.date)

    last_data = data.iloc[-1, :].date
    last_data

    df2_fullfill0 = data[data['isfull'] == False].loc[:, ['date', 'act', 'minutes']]
    df2_fullfill1 = data[data['isfull'] == True].loc[:, ['date', 'act', 'minutes']]

    first_data = last_data - timedelta(days=days)

    df2_fullfill0 = df2_fullfill0[df2_fullfill0.date >= first_data]
    df2_fullfill1 = df2_fullfill1[df2_fullfill1.date >= first_data]

    minimum_fill1 = df2_fullfill1.groupby('act').sum().sort_values(by=['minutes'])
    maximum_fill0 = df2_fullfill0.groupby('act').sum().sort_values(by=['minutes'])

    res = "Увеличьте время на " + minimum_fill1.index[0] + " и " + minimum_fill1.index[1] + "\n"

    res += "Уменьшите время на " + maximum_fill0.index[-1] + " и " + maximum_fill0.index[-2]

    return res

