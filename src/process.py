import pandas as pd
from typing import Any, Dict, Optional
from constants import Constants


class DataStorage:
    def __init__(self,
                 data: Optional[pd.DataFrame] = None,
                 answers: Optional[Dict[str, Any]] = None):
        """
        :param data: Raw dataframe if uploaded.
        :type data: Optional[pd.DataFrame], default=None
        :param answers: Users questionary answers to generate data.
        :type answers: Dict[str, Any], default=None
        """
        self.upload = True
        if data is None:
            self.upload = False
            self.answers = answers
        else:
            self.data_schedule = self._base_pipeline(data)

    @staticmethod
    def _naming_and_types(data: pd.DataFrame) -> pd.DataFrame:
        """
        Column names and type manipultions with raw data.
        :param data: Initial raw data.
        :type data: pd.DataFrame
        :return: Data with renamed columns and right types.
        :rtype: pd.DataFrame
        """
        data = data.rename(columns=Constants.init_data_col_name_mappings)
        data = data.drop('comment', axis=1)

        data['act'] = data.act.replace(Constants.init_data_act_mappings)

        data['begin'] = pd.to_datetime(data.begin)
        data['end'] = pd.to_datetime(data.end)

        data['dur'] = data['dur'] + ':00'
        data['dur'] = pd.to_timedelta(data.dur)
        data['dur'] = data['dur'] - pd.to_timedelta(data['dur'].dt.days, unit='d')

        data['minutes'] = data.dur.dt.total_seconds() / 60
        data['date'] = data.begin.dt.date

        data = data.drop('dur', axis=1)

        return data

    @staticmethod
    def _prod_fullfil_columns(data: pd.DataFrame,
                             mappings_prod: Dict[str, int],
                             mappings_full: Dict[str, int]) \
            -> pd.DataFrame:
        """
        Adding productive/inprod/neutral labels to activities.
        Adding fulfill/devastating labels to activities.
        :param data: Data with right column namings and types.
        :type data: pd.DataFrame.
        :param mappings_prod: Actions' mappings for productivity labels.
        :type mappings_prod: Dict[str, int]
        :param mappings_full: Actions' mappings for charging labels
        :type mappings_full: Dict[str, int]
        :return: Data with additional columns.
        :rtype: pd.DataFrame
        """
        data['isprod'] = data.act.map(mappings_prod).astype('category')
        data['isfull'] = data.act.map(mappings_full).astype('category')
        return data

    def _base_pipeline(self,
                       data: pd.DataFrame) \
            -> pd.DataFrame:
        """
        :param data: Raw time data.
        :type data: pd.DataFrame
        :return: Based preprocessed data.
        :rtype: pd.DataFrame
        """
        data = self._naming_and_types(data)
        data = self._prod_fullfil_columns(data,
                                          Constants.mappings_productive_acts_custom,
                                          Constants.mappings_fulfill_acts_custom)
        return data


data_init = pd.read_csv('D:/IT stuff/PY/Хакатон ИКТ 4/future_design_hackaton_4/data/report_initial.csv')

a = DataStorage(data=data_init)

print(0)