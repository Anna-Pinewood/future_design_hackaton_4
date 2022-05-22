import pandas as pd
import datetime
from typing import Any, Dict, Optional, Tuple, List
from constants import Constants
import numpy as np


def _generate_day_prod_standard(date: datetime.date,
                                cat: str,
                                weekday: bool = True):
    """
    :param cat: Person category.
    :type cat: str
    :param weekday: Whether weekday or weekend
    :type weekday: bool, default True.
    :return:
    :rtype:
    """
    if weekday:
        range_dict = Constants.ranges_weekday_prod.loc[cat]
    else:
        range_dict = Constants.ranges_weekend_prod.loc[cat]
    productive_minutes = np.random.randint(range_dict['prod_low'], range_dict['prod_high'])
    neutral_minutes = np.random.randint(range_dict['neu_low'], range_dict['neu_high'])
    leisure_minutes = np.random.randint(range_dict['unprod_low'], range_dict['unprod_high'])
    one_day_df = pd.DataFrame({
        'date': [date] * 3,
        'isprod': [1, 0, 2],
        'minutes': [productive_minutes, neutral_minutes, leisure_minutes]
    })
    one_day_df['date'] = pd.to_datetime(one_day_df['date'])
    return one_day_df


def sleep_for_outliers(data: pd.DataFrame):

      data = data.groupby('date').sum()
      data['minutes'] = 24*60 - data.minutes

      return pd.DataFrame(data['minutes'])

def _generate_fulfill_on_prod_df(data: pd.DataFrame, cat: str) -> pd.DataFrame:
    """
    Generating fulfilling hours based on productive hours of 1 day data.
    :param data: One-day productivity data, generated previously.
    :type pd.DataFrame:
    :param cat: Category of person for generating.
    :type cat: str
    :return:
    :rtype:
    """
    data = data.rename(columns={'isprod': 'isful'})
    idx_0 = data[data.isful == 0].index
    idx_2 = data[data.isful == 2].index
    data.loc[idx_0, 'minutes'] += data.loc[idx_2, 'minutes'].values
    data = data.drop(idx_2)

    total = data.minutes.sum()
    idx = data[data.isful == 1].index
    data.loc[idx, 'minutes'] *= Constants.fulfill_coefs_based_cat[cat]

    idx_0 = data[data.isful == 0].index
    data.loc[idx_0, 'minutes'] = total - data.loc[idx, 'minutes'].values
    return data


def generate_prod_and_full(cat) -> Tuple[pd.DataFrame, pd.DataFrame]:
    today = pd.to_datetime('today').normalize()
    prod_data = pd.DataFrame()
    full_data = pd.DataFrame()
    date_range_ = pd.date_range(end=today, periods=6 * 30)
    for date in date_range_:
        weekday = date.dayofweek < 5
        prod = _generate_day_prod_standard(date, cat, weekday)
        full = _generate_fulfill_on_prod_df(prod, cat)
        prod_data = prod_data.append(prod)
        full_data = full_data.append(full)
    prod_data = prod_data.reset_index(drop=True)
    full_data = full_data.reset_index(drop=True)
    return prod_data, full_data


def count_burnout_nums(perfect_score: int, sad_score: int):
    score = (perfect_score + sad_score * 1.5) / 2
    num = round(score * 2)
    return num


def get_burnout_indexes(date_range: pd.DatetimeIndex, num: int) -> List[str]:
    num_ = round(len(date_range) / num)
    dates = notprod.index[::num_]
    random_component = pd.to_timedelta(np.random.randint(0, 3, size=len(dates)))
    new_dates = [d.strftime('%Y-%m-%d') for d in (dates + random_component).date]
    return new_dates


def add_burnouts(notprod: pd.DataFrame,
                 isprod: pd.DataFrame,
                 sleep: pd.DataFrame,
                 mean_nprod: float,
                 std_nprod: float,
                 mean_sleep: float,
                 std_sleep: float,
                 dates: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # allowed_value
    available_h = (notprod.loc[dates, 'minutes'] + sleep.loc[dates, 'minutes'] + isprod.loc[dates, 'minutes'])
    burnout_values_nonprod = np.random.randint(0, 40, size=len(dates)) + (mean_nprod + std_nprod) * 1.5
    burnout_values_sleep = np.random.randint(0, 40, size=len(dates)) + (std_sleep + mean_sleep)
    burnout_values_prod = available_h * 60 - (burnout_values_sleep + burnout_values_nonprod)
    if (burnout_values_prod < 0).any:
        burnout_values_nonprod = np.random.randint(9 * 60, 11 * 60, size=len(dates))
        burnout_values_sleep = np.random.randint(10 * 60, 11 * 60, size=len(dates))
        burnout_values_prod = 24 * 60 - burnout_values_sleep - burnout_values_nonprod - 2

    notprod.loc[dates, 'minutes'] = burnout_values_nonprod
    isprod.loc[dates, 'minutes'] = burnout_values_prod
    sleep.loc[dates, 'minutes'] = burnout_values_sleep

    return notprod, isprod, sleep


def add_before_burn(isprod: pd.DataFrame,
                    notprod: pd.DataFrame,
                    sleep: pd.DataFrame,
                    mean_prod: float,
                    std_prod: float,
                    mean_sleep: float,
                    std_sleep: float,
                    dates: List[str],
                    window: int = 4):
    dates = [d.strftime('%Y-%m-%d') for d in (pd.to_datetime(dates) - pd.to_timedelta(window))]
    try:
        isprod.loc[dates]
    except KeyError:
        dates = dates[1:]
    burnout_values_sleep = np.random.randint(0, 40, size=len(dates)) + (std_sleep + mean_sleep) / 1.5
    burnout_values_prod = np.random.randint(0, 40, size=len(dates)) + (mean_prod + std_prod) * 1.2

    if (burnout_values_sleep + burnout_values_prod > 24 * 60).any:
        burnout_values_sleep = np.random.randint(0, 5 * 60, size=len(dates))
        burnout_values_nonprod = np.random.randint(6 * 60, 14 * 60, size=len(dates))

    isprod.loc[dates, 'minutes'] = burnout_values_prod
    sleep.loc[dates, 'minutes'] = burnout_values_sleep

    fulfil = notprod * Constants.fulfill_coefs_based_cat[cat]

    return isprod, sleep, fulfil


def generate_all(cat: str, score: int):
    prod_data, full_data = generate_prod_and_full(cat)

    isprod = prod_data[prod_data.isprod == 1]
    isprod.index = isprod.date
    isprod.drop(['date', 'isprod'], axis=1, inplace=True)

    notprod = prod_data[prod_data.isprod == 0]
    notprod.index = notprod.date
    notprod.drop(['date', 'isprod'], axis=1, inplace=True)

    nfull = full_data[full_dat.isful == 0]
    nfull.index = nfull.date
    nfull.drop(['date', 'isful'], axis=1, inplace=True)

    sleep = sleep_for_outliers(prod_data)

generate_all('w', 1)