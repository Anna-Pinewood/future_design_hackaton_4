from typing import Any, Dict


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
         'eat': 0,
         'hobby': 1,
         'leisure': 0,
         'school': 1,
         'sleep': 1,
         'socio': 0,
         'sport': 0,
         'study': 1,
         'transport': 0,
         'work': 1}


print(Constants.init_data_col_name_mappings)
