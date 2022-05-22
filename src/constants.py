from typing import Dict
import pandas as pd


def make_ranges_weekday_prod() -> pd.DataFrame:
    ranges_weekday_prod = pd.DataFrame({
        'cat': ['sc', 'w', 'sc_w', 'non'],
        'prod_low': [5, 7, 8, 4],
        'prod_high': [8, 8.5, 10, 6],
        'neu_low': [5, 5, 4, 4],
        'neu_high': [6, 6, 5, 5],
        'unprod_low': [2, 2, 2, 4],
        'unprod_high': [4, 3.5, 3, 6]
    })

    ranges_weekday_prod.index = ranges_weekday_prod['cat'].astype('category')
    ranges_weekday_prod = ranges_weekday_prod.drop('cat', axis=1)
    ranges_weekday_prod = (ranges_weekday_prod * 60).astype(int)
    return ranges_weekday_prod


def make_ranges_weekend_prod() -> pd.DataFrame:
    ranges_weekend_prod = pd.DataFrame({
        'cat': ['sc', 'w', 'sc_w', 'non'],
        'prod_low': [2, 2, 4, 4],
        'prod_high': [5, 3, 10, 5],
        'neu_low': [3, 3, 4, 4],
        'neu_high': [4, 5, 5, 5],
        'unprod_low': [3, 6, 4, 4],
        'unprod_high': [6, 8, 5, 6]
    })

    ranges_weekend_prod.index = ranges_weekend_prod['cat'].astype('category')
    ranges_weekend_prod = ranges_weekend_prod.drop('cat', axis=1)
    ranges_weekend_prod = (ranges_weekend_prod * 60).astype(int)

    return ranges_weekend_prod


class Constants:
    init_data_col_name_mappings: Dict[str, str] = \
        {'Тип': 'act',
         'Продолжительность': 'dur',
         'Начало': 'begin',
         'Конец': 'end',
         'Комментарий': 'comment'}
    init_data_act_mappings: Dict[str, str] = \
        {'Events': 'socio',
         'Социализация': 'socio',
         'Учеба': 'study',
         'Еда': 'eat',
         'Пары': 'school',
         'Транспорт': 'transport',
         'Сборы...': 'transport',
         'Душ. Beauty': 'chores',
         'Планирование': 'study',
         'Рома': 'socio',
         'Leisure': 'leisure',
         'Хобби / Осознанность': 'hobby',
         'Магазин': 'chores',
         'PwC': 'work',
         'Спорт': 'sport',
         'Работа Maximum': 'work',
         'Вынужденное (больница)': 'leisure',
         'Сон': 'sleep',
         'Мафия': 'hobby',
         'Уборка / Дом': 'chores',
         'Учёба. Пары': 'study'}
    mappings_productive_acts_custom: Dict[str, int] \
        = {'chores': 2,
           'eat': 2,
           'hobby': 1,
           'leisure': 0,
           'school': 1,
           'sleep': 0,
           'socio': 0,
           'sport': 1,
           'study': 1,
           'transport': 2,
           'work': 1}
    mappings_fulfill_acts_custom: Dict[str, int] = \
        {'chores': 0,
         'eat': 1,
         'hobby': 1,
         'leisure': 1,
         'school': 0,
         'sleep': 1,
         'socio': 1,
         'sport': 1,
         'study': 0,
         'transport': 0,
         'work': 0}

    ranges_weekday_prod = make_ranges_weekday_prod()
    ranges_weekend_prod = make_ranges_weekend_prod()

    fulfill_coefs_based_cat = pd.Series(
        dict(zip(['sc', 'w', 'sc_w', 'non'],
                 [1.05, 1, 1, 1.1]))
    )

    questionnaire_act_mappings: Dict[str, str] = {
        'Работа': 'w',
        'Учеба': 'sc',
        'Оба': 'sc_w',
        'Ничего': 'non'
    }

