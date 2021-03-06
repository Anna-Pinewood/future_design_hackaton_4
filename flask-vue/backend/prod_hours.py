# -*- coding: utf-8 -*-
"""productive_hours.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zmS4_8ulpe-3RnHorrXrNf3ZtxBISPMU
"""
import random

import pandas as pd
import datetime
import warnings
from collections import namedtuple


warnings.filterwarnings('ignore')


def get_data(data):
    df = data
    df = df[['date', 'begin', 'end', 'isprod']]
    df['date'] = pd.to_datetime(df.date)
    return df


def delete_empty_activities(data):
    return data.loc[data.begin != data.end]


def add_empty_ranges(data):
    first = data.begin.shift(periods=1) - data.end > datetime.timedelta(0)
    second = data.begin - data.end.shift(periods=-1) > datetime.timedelta(0)
    df_1 = data.loc[first]
    k = pd.DataFrame(columns=['date', 'begin', 'end', 'isprod'])
    for i, row in df_1.iterrows():
        tmp = [data.loc[i - 1].date, row.end, data.loc[i - 1].begin, 2]
        k.loc[len(k)] = tmp
    data = pd.concat([data, k])
    return data


def split_weekdays(data):
    df_weekend = data[data.date.dt.dayofweek >= 5]
    df_weekday = data[data.date.dt.dayofweek < 5]
    return df_weekday, df_weekend


def distribute_ranges(data):
    data['begin'] = data.begin.map(lambda x: x.round(freq='5min'))
    data['end'] = data.end.map(lambda x: x.round(freq='5min'))
    data = delete_empty_activities(data)
    data['ranges'] = data[['begin', 'end']].agg(lambda x: pd.date_range(start=x[0], end=x[1], freq='5min'), axis=1)
    data['ranges'] = data.ranges.map(lambda x: list(zip(x[:-1:], x[1::])))
    data = data.explode('ranges', ignore_index=True)
    data = data.drop(columns=['begin', 'end'])
    return data


def predict_hours(data):
    df_full = add_empty_ranges(data)
    df_full = df_full.sort_values(by=['begin'])
    df_full_distributed = distribute_ranges(df_full)
    df_full_distributed = df_full_distributed.dropna()
    return df_full_distributed


def need_row(data, need_type):
    data['needed_range'] = data.isprod.apply(lambda x: (x == need_type))
    data['needed_range'] *= data.ranges
    data = data.groupby(['week', 'ranges_day'], as_index=False).agg({'needed_range': 'sum'})
    data['isprod'] = need_type
    return data


def group_ranges(data, type):
    data['week'] = data.date.apply(lambda x: x.isocalendar()[:2])
    data['ranges_day'] = data.ranges.apply(lambda x: ((x[0].hour, x[0].minute), (x[1].hour, x[1].minute)))
    df_group_day = data.groupby([data.week, data.ranges_day, data.isprod], as_index=False).agg({'ranges': 'count'})
    df_group_mean = need_row(df_group_day, type)
    return df_group_mean


def union_to_hour(data):
    data['ranges_day_hour'] = data.ranges_day.apply(lambda x: (x[0][0], x[0][0] + 1))
    return data


def get_score(data, type):
    res_weeekdays = union_to_hour(group_ranges(data, type)).groupby(['week', 'ranges_day_hour'], as_index=False).agg(
        {'needed_range': 'mean'})
    df_for_mean = res_weeekdays.groupby('ranges_day_hour', as_index=False).agg({'needed_range': lambda x: list(x)})
    df_for_mean['weights'] = df_for_mean.needed_range.apply(lambda x: pd.DataFrame(x).ewm(com=0.5).mean())
    df_for_mean['weights'] = df_for_mean.weights.apply(lambda x: x[0].tolist())
    products = []
    for index, row in df_for_mean.iterrows():
        list1 = row.needed_range
        list2 = row.needed_range
        p = sum([a * b for a, b in zip(list1, list2)]) / len(list1)
        products.append(p)
    df_for_mean['score'] = products
    return df_for_mean[['ranges_day_hour', 'score']]


def x_str(res):
    return '{}:00, {}:00'.format(*res)


def prepared_result(res, name):
    return list(x_str(i) for i in res.ranges_day_hour), list(res.score.apply(lambda x: round(x, 3))), name

def prepared_results_answers(scores, name):
    return [x_str((i, i + 1)) for i in range(0, 24)], scores, name


# DATA IS NONE
# CHANGE TYPE
def run(data=None, answers=None, type=1):
    Result = namedtuple('Plot', 'X Y name')
    if not data is None:
        df = get_data(data)
        df = predict_hours(df)
        df_weekday, df_weekend = split_weekdays(df)
        result1 = Result(*prepared_result(get_score(df_weekday, type=type), "???????????????????????? ???????? ?? ???????????? ??????"))
        result2 = Result(*prepared_result(get_score(df_weekend, type=type), "???????????????????????? ???????? ?? ???????????????? ??????"))
    else:
        result1 = Result(*prepared_results_answers([random.randint(0, 4) for i in range(24)], "???????????????????????? ???????? ?? ???????????? ??????"))
        result2 = Result(*prepared_results_answers([random.randint(0, 3) for i in range(24)], "???????????????????????? ???????? ?? ???????????????? ??????"))
    return result1, result2


"""???????????? run()"""

# data_init = pd.read_csv('../data/report_initial.csv')
#
# a = process.DataStorage(data=data_init)
#
# r = run(a.data_schedule)
# print(r)