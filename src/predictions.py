import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import ks_2samp
from statistics import mean
#from fbprophet import Prophet
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from process import DataStorage

# df2_by_days0 = pd.read_csv("df2_by_days.csv")
# df2_full = pd.read_csv("df2_full.csv")
# df2_prod = pd.read_csv("df2_prod.csv")

def findanomalyboxplot(data):

    Q1 = data['minutes'].quantile(0.25)
    Q3 = data['minutes'].quantile(0.75)
    IQR = Q3 - Q1
    data_anomaly= data[(data['minutes'] < Q1-1.5*IQR ) | (data['minutes'] > Q3+1.5*IQR)==True]
    return data_anomaly

def findanomalyzindex(data):
  return data[(np.abs(stats.zscore(data['minutes']))) > 3]


# def getnightsleeptime(data):
#     date = data.date.unique()
#     data_sleep_night = pd.DataFrame(columns=['date', 'minutes'])
#     data_sleep_night.date = date
#     for day in date:
#         night_sleep_time = 24 * 60 - data[data.date == day].minutes.sum()
#         data_sleep_night['minutes'][data_sleep_night.date == day] = night_sleep_time
#
#     return data_sleep_night

def minimumsleep(data):
    Q1 = data['minutes'].quantile(0.25)
    Q3 = data['minutes'].quantile(0.75)
    IQR = Q3 - Q1
    data_anomaly= data[(data['minutes'] < Q1-1.5*IQR )==True]
    return data_anomaly

def maximumsleep(data):
    # sns.boxplot(data['minutes'])
    Q1 = data['minutes'].quantile(0.25)
    Q3 = data['minutes'].quantile(0.75)
    IQR = Q3 - Q1
    data_anomaly= data[(data['minutes'] > Q3+1.5*IQR )==True]
    return data_anomaly

def get_df2_full0(data):
  df2_full0 = data[data.isfull==False]
  df2_full0.head()
  df2_full0.drop('isfull',axis=1,inplace=True)
  return df2_full0

def get_df2_full1(data):
  df2_full1 = data[data.isfull==True]
  df2_full1.head()
  df2_full1.drop('isfull',axis=1,inplace=True)
  return df2_full1




# def get_df2_by_days_sleep(data):
#   df2_by_days_sleep=data[data.act=='sleep'].loc[:,['date','minutes']]
#   return df2_by_days_sleep




def get_last_anomalies(df2_prod0, df2_prod1, df2_ful1, df2_ful0, df2_sleep_night):

    # df2_sleep_night = getnightsleeptime(df2_by_days)

    # df2_days_sleep = get_df2_by_days_sleep(df2_by_days)

    # Минимальные часы сна
    # Максимальные часы сна
    df2_by_days_sleep_night_maximum = maximumsleep(df2_sleep_night)

    # Избыток непродуктивных часов
    df2_prod0_anomaly = findanomalyboxplot(df2_prod0)

    # Избыток notfullfill  часов
    df2_full0_anomaly = findanomalyboxplot(df2_ful0)

    # Переизбыток продуктивных часов
    df2_prod1_anomaly = findanomalyzindex(df2_prod1)

    # Аномальный дневной сон
   # df2_by_days_sleep_anomaly = maximumsleep(df2_days_sleep)

    # Получаем даты выгораний
    # Избыток непродуктивных часов - выгорание
    df2_anomalies = df2_prod0_anomaly.loc[:, ['date']]

    #  Избыток дневного сна - выгорание
  #  df2_anomalies = df2_anomalies.append(df2_by_days_sleep_anomaly.loc[:, ['date']], ignore_index=True)

    # Избыток ночного сна - выгорание
    df2_anomalies = df2_anomalies.append(df2_by_days_sleep_night_maximum.loc[:, ['date']], ignore_index=True)

    # Переделаем из строки дату
    df2_anomalies['date'] = pd.to_datetime(df2_anomalies['date'])

    df2_anomalies = df2_anomalies.sort_values(by='date')

    df2_anomalies.drop_duplicates(inplace=True)
    df2_anomalies = df2_anomalies.reset_index(drop=True)

    for i in range(len(df2_anomalies) - 1):

        if (df2_anomalies.iloc[i + 1, :] - df2_anomalies.iloc[i, :]).date.days <= 2:
            df2_anomalies.iloc[i + 1, :] = df2_anomalies.iloc[i, :]

    df2_anomalies.drop_duplicates(inplace=True)
    df2_anomalies = df2_anomalies.reset_index(drop=True)

    # print(df2_anomalies)
    return df2_anomalies

def first_window(windowlength, day_anomaly, df2_prod0):

  data_first_window=pd.DataFrame(columns=['date','minutes'])
  for day in df2_prod0.date:
    if((day_anomaly - pd.to_datetime(day)).days<=windowlength and (day_anomaly - pd.to_datetime(day)).days>0):
      data_first_window=data_first_window.append(df2_prod0[df2_prod0.date==day])
  return data_first_window


def second_window(windowlength, day_anomaly, df2_prod0):

  data_second_window=pd.DataFrame(columns=['date','minutes'])
  for day in df2_prod0.date:
    if((day_anomaly - pd.to_datetime(day)).days<=windowlength*2 and (day_anomaly - pd.to_datetime(day)).days>windowlength):
      data_second_window=data_second_window.append(df2_prod0[df2_prod0.date==day])
  return data_second_window


def get_length_window(day,df2_prod0):
  for i in range(2,8):
    windowl=i
    data_first_window = first_window(windowl,day,df2_prod0)
    data_second_window = second_window(windowl,day,df2_prod0)
    p_value = ks_2samp(np.array(data_first_window.minutes) , np.array(data_second_window.minutes)).pvalue
    if (p_value>0.05):
      break
  return windowl


def get_opt_window(df2_anomalies, df2_prod0):
    window_l = []

    df2_anomalies.date = pd.to_datetime(df2_anomalies.date)
    for day in df2_anomalies.date:
        wl = get_length_window(day, df2_prod0)
        window_l.append(wl)

    return window_l[len(window_l) // 2]


def get_df_burnout(df_anom, df2_prod, df2_full, df2_sleep_night,df2_days_sleep):
    df2_burnout = df_anom
    optlength = get_opt_window(df_anom, df2_prod)
    # Переизбыток продуктивных часов - признак приближающегося выгорания (добавить день +wl)
    # Переизбыток продуктивных часов
    df2_prod1_anomaly = findanomalyzindex(get_df2_prod0(df2_prod))
    df2_prod1_anomaly_plus2 = df2_prod1_anomaly.loc[:, ['date']]
    df2_prod1_anomaly_plus2['date'] = pd.to_datetime(df2_prod1_anomaly_plus2['date']) + pd.DateOffset(days=optlength)
    df2_burnout = df2_burnout.append(df2_prod1_anomaly_plus2.loc[:, ['date']], ignore_index=True)

    # Минимальные часы сна
    df2_by_days_sleep_night_minimum = minimumsleep(df2_sleep_night)
    df2_by_days_sleep_night_minimum_plus2 = df2_by_days_sleep_night_minimum.loc[:, ['date']]
    df2_by_days_sleep_night_minimum_plus2['date'] = pd.to_datetime(
        df2_by_days_sleep_night_minimum_plus2['date']) + pd.DateOffset(days=optlength)
    df2_burnout = df2_burnout.append(df2_by_days_sleep_night_minimum_plus2.loc[:, ['date']], ignore_index=True)

    # Переизбыток unfullfill часов - признак приближающегося выгорания (добавить день +2)
    # Избыток notfullfill  часов
    df2_full0_anomaly = findanomalyboxplot(get_df2_full0(df2_full))
    df2_full0_anomaly_plus2 = df2_full0_anomaly.loc[:, ['date']]
    df2_full0_anomaly_plus2['date'] = pd.to_datetime(df2_full0_anomaly_plus2['date']) + pd.DateOffset(days=optlength)
    df2_burnout = df2_burnout.append(df2_full0_anomaly_plus2.loc[:, ['date']], ignore_index=True)

    df2_burnout = df2_burnout.sort_values(by='date')

    df2_burnout.drop_duplicates(inplace=True)
    df2_burnout = df2_burnout.reset_index(drop=True)

    for i in range(len(df2_burnout) - 1):

        if (df2_burnout.iloc[i + 1, :] - df2_burnout.iloc[i, :]).date.days <= 2:
            df2_burnout.iloc[i + 1, :] = df2_burnout.iloc[i, :]

    df2_burnout.drop_duplicates(inplace=True)
    df2_burnout = df2_burnout.reset_index(drop=True)


def make_train_test(df2_prod0):
    df2_prod0_new = df2_prod0.copy()
    # df2_prod0_new.date = pd.to_datetime(df2_prod0_new['date'])
    # df2_prod0_new.index = pd.to_datetime(df2_prod0_new.date)

    df2_test = df2_prod0_new.tail(14)
    df2_train = df2_prod0_new.iloc[:df2_prod0_new.shape[0]-14, :]

    # Transform train data
    data = df2_train
    data.index = data.index.to_pydatetime()
    data["day"] = data.index.day
    data["weekday"] = data.index.weekday
    data["month"] = data.index.month
    data = data.dropna()
    data = data.reset_index(drop=True)
    data_train = data

    # Transform test data
    data_test = df2_test
    data_test.index = data_test.index.to_pydatetime()
    data_test["day"] = data_test.index.day
    data_test["weekday"] = data_test.index.weekday
    data_test["month"] = data_test.index.month
    data_test = data_test.dropna()
    data_test = data_test.reset_index(drop=True)

    X_train = data_train.loc[:, ['day', 'weekday', 'month']]
    y_train = data_train.iloc[:, [0]]

    X_test = data_test.loc[:, ['day', 'weekday', 'month']]
    y_test = data_test.iloc[:, [0]]

    return X_train, X_test, y_train, y_test


# Построили модель
def create_model(df2_prod0, model = None):
  # df2_prod0 - nonprod
  if model is not None:
    return model

  X_train,X_test,y_train,y_test = make_train_test(df2_prod0)
  random_forest = RandomForestRegressor()
  tuned_parameters  = {'n_estimators':[5,10,15,20],'max_depth':[2,4,6,8,10],'min_samples_split':np.arange(1,10)}
  clf1 = GridSearchCV(random_forest,tuned_parameters)
  clf1.fit(X_train,y_train)
  random_forest = RandomForestRegressor(**clf1.best_params_)

  random_forest.fit(X_train,y_train)

  y_pred = random_forest.predict(X_test)

  return random_forest


def prediction_burnout(model, data):
  y_pred = model.predict(data)
  return y_pred


def plot_pred_past(df2_prod0, model=None):
    model_ = create_model(df2_prod0, model)
    data_past = df2_prod0.tail(14)/60
    data_past.reset_index(inplace=True)
    data_past = data_past.rename(columns={'index': 'date'})
    today = pd.to_datetime('today').normalize().date()
    date_range_ = pd.date_range(start=today, periods=14)
    data_pred = pd.DataFrame(columns=['date'])
    data_pred.date = date_range_

    data_pred['minutes'] = None

    data_res = data_past.append(data_pred)
    data_res.date = pd.to_datetime(data_res.date)
    x_dates = [d.strftime('%Y-%m-%d') for d in data_res.date]
    y_past = data_res.minutes
    data = data_pred
    data.index = data_pred.date
    data.index = data.index.to_pydatetime()
    data["day"] = data.index.day
    data["weekday"] = data.index.weekday
    data["month"] = data.index.month
    x_pred = data.loc[:, ['day', 'weekday', 'month']]

    x_pred = x_pred.reset_index(drop=True)
    y_pred1 = [None] * 14 + prediction_burnout(model_, x_pred).tolist()

    return (x_dates, y_past.values.tolist(), "Past"), (x_dates, y_pred1, "Pred")

# a = DataStorage(answers={'procrastination': ('1',), 'work': ('Учеба',), 'workdaysleep': ('1:00',), 'weekendsleep': ('3:00',), 'ideal': ('2',)})
#
# print(plot_pred_past(a.nonprod))

