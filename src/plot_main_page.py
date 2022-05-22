import pandas as pd
import datetime
from process import DataStorage
from typing import Any, Dict, Optional, Tuple, List
from constants import Constants
import numpy as np

def get_data_main_plot(isprod: pd.DataFrame,
                       nonprod:  pd.DataFrame,
                       isful:  pd.DataFrame,
                       nonful:  pd.DataFrame,
                       sleep: pd.DataFrame):
    result = []
    result.append((plot_data_curve(isprod)[0], plot_data_curve(isprod)[1], 'Productive time'))
    result.append((plot_data_curve(nonprod),plot_data_curve(isprod)[1], 'Unproductive time'))
    result.append((plot_data_curve(isful),plot_data_curve(isprod)[1], 'Fulfilling time'))
    result.append((plot_data_curve(nonful),plot_data_curve(isprod)[1], 'Devastating time'))
    result.append((plot_data_curve(sleep), plot_data_curve(isprod)[1],'Sleep time'))
    return result
def plot_data_curve(data: pd.DataFrame) -> Tuple[List[str], List[float]]:
    end = (data.index[-1]).strftime('%Y-%m-%d')
    begin = (data.index[-1] - datetime.timedelta(days=21)).strftime('%Y-%m-%d')
    data_where = data.loc[begin:end]
    x = [d.strftime('%Y-%m-%d') for d in data.loc[begin:end].index]
    y = list((data.loc[begin:end].minutes.values/60).round(2))
    return x,y


# a = DataStorage(answers={'procrastination': ('1',), 'work': ('Учеба',), 'workdaysleep': ('1:00',), 'weekendsleep': ('3:00',), 'ideal': ('2',)})
#
# print(get_data_main_plot(a.isprod, a.nonprod, a.isful, a.nonful, a.sleep))