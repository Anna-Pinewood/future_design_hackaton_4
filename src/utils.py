import pandas as pd
import datetime
from typing import Tuple, List
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
#    one_day_df['date'] = pd.to_datetime(one_day_df['date'])
    return one_day_df


def sleep_for_outliers(data: pd.DataFrame):
    data = data.groupby('date').sum()
    data['minutes'] = 24 * 60 - data.minutes

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


def generate_prod_and_full(cat: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generating productive dataset and fulfillment dataset
    per category in minutes per days.
    :param cat: Category - 'w' / 'sc' / 'sc_w' / 'non'
    :type cat: str
    :return: productivity df, fulfillment df
    :rtype: Tuple[pd.DataFrame, pd.DataFrame]
    """
    today = pd.to_datetime('today').normalize().date()
    prod_data = pd.DataFrame()
    full_data = pd.DataFrame()
    date_range_ = pd.date_range(end=today, periods=6 * 30)
    for date in date_range_:
        weekday = date.dayofweek < 5
        date = date.date()
        prod = _generate_day_prod_standard(date, cat, weekday)
        full = _generate_fulfill_on_prod_df(prod, cat)
        prod_data = prod_data.append(prod)
        full_data = full_data.append(full)
    prod_data = prod_data.reset_index(drop=True)
    full_data = full_data.reset_index(drop=True)
    return prod_data, full_data


def count_burnout_nums(perfect_score: int, sad_score: int) -> int:
    """
    Count, how many times will burnout happen, based on questionarrie.
    :param perfect_score: Score of perfectionism from quest.
    :type perfect_score: int
    :param sad_score: Score of procrastination from quest.
    :type sad_score: int
    :return: Number of burnouts.
    :rtype: int
    """
    score = (perfect_score + sad_score * 1.5) / 2
    num = round(score * 2)
    return num

def get_burnout_indexes(date_range: pd.DatetimeIndex,
                        notprod: pd.DataFrame,
                        num: int) -> List[str]:
    """
    Getting list of dates when burnout will happen.
    :param date_range: range of dates available.
    :type date_range: pd.DatetimeIndex
    :param notprod: Non-productive data.
    :type notprod: pd.DataFrame
    :param num: Number on burnouts counted.
    :type num: int
    :return: List of burnout dates.
    :rtype: List[str]
    """
    num_ = round(len(date_range) / num)
    dates = notprod.index[::num_]
    random_component = pd.to_timedelta(np.random.randint(0, 3, size=len(dates)))
    new_dates = dates + random_component
    return new_dates


def add_burnouts(isprod: pd.DataFrame,
                 notprod: pd.DataFrame,
                 sleep: pd.DataFrame,
                 mean_nprod: float,
                 std_nprod: float,
                 mean_sleep: float,
                 std_sleep: float,
                 dates: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Gets notprod, isprod, sleep data with burnouts.
    :type isprod: pd.DataFrame
    :type notprod: pd.DataFrame
    :type sleep: pd.DataFrame
    :type mean_nprod: float
    :type std_nprod: float
    :type mean_sleep: float
    :type std_sleep: float
    :param dates: Dates of burnouts
    :type dates: List[str]
    :return:
    :rtype:
    """
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
                    sleep_: pd.DataFrame,
                    mean_prod: float,
                    std_prod: float,
                    mean_sleep: float,
                    std_sleep: float,
                    dates: List[str],
                    cat: str,
                    window: int = 4):
    """Adding burnout window."""
    dates = [d.date() for d in (pd.to_datetime(dates) - pd.to_timedelta(window))]
    try:
        isprod.loc[dates]
    except KeyError:
        dates = dates[1:]
    burnout_values_sleep = np.random.randint(0, 40, size=len(dates)) + (std_sleep + mean_sleep) / 1.5
    burnout_values_prod = np.random.randint(0, 40, size=len(dates)) + (mean_prod + std_prod) * 1.2

    if (burnout_values_sleep + burnout_values_prod > 24 * 60).any:
        burnout_values_sleep = np.random.randint(0, 5 * 60, size=len(dates))
        burnout_values_prod = np.random.randint(6 * 60, 14 * 60, size=len(dates))


    isprod.loc[dates, 'minutes'] = burnout_values_prod
    sleep_.loc[dates, 'minutes'] = burnout_values_sleep

    fulfil = notprod * Constants.fulfill_coefs_based_cat[cat]

    return isprod, sleep_, fulfil


def generate_all(cat: str, perfect_score: int, sadness_score: int):
    prod_data, ful_data = generate_prod_and_full(cat)

    isprod = prod_data[prod_data.isprod == 1]
    isprod.index = [d.date() for d in pd.to_datetime(isprod.date)]
    #isprod.index = isprod.date
    isprod.drop(['date', 'isprod'], axis=1, inplace=True)

    notprod = prod_data[prod_data.isprod == 0]
    notprod.index = [d.date() for d in pd.to_datetime(notprod.date)]
    notprod.drop(['date', 'isprod'], axis=1, inplace=True)

    nfull = ful_data[ful_data.isful == 0]
    nfull.index = nfull.date
    nfull.drop(['date', 'isful'], axis=1, inplace=True)

    sleep = sleep_for_outliers(prod_data)

    num = count_burnout_nums(perfect_score, sadness_score)
    idx = sleep.index
    dates = get_burnout_indexes(date_range=idx, notprod=notprod, num=num)

    mean_nprod = np.mean(notprod['minutes'])
    std_nprod = np.std(notprod['minutes'])
    mean_prod = np.mean(isprod['minutes'])
    std_prod = np.std(isprod['minutes'])
    mean_sleep = np.mean(sleep['minutes'])
    std_sleep = np.std(sleep['minutes'])

    notprod, isprod, sleep = add_burnouts(isprod, notprod, sleep, mean_nprod, std_nprod, mean_sleep, std_sleep, dates)
    isprod, sleep, isful = add_before_burn(isprod, notprod, sleep, mean_prod, std_prod, mean_sleep, std_sleep, dates, cat)
    notful = 24*60-isful
    for data in  [isprod, notprod,isful,notful, sleep]:
        data.index = pd.to_datetime(data.index)
    return (
        isprod,
        notprod,
        isful,
        notful,
        sleep
    )