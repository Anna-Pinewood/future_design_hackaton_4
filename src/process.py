import pandas as pd
import datetime
from typing import Any, Dict, Optional, List
from constants import Constants
from utils import generate_all
import numpy as np

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
        self.data_schedule = None
        self.answers = None

        if data is None:
            self.upload = False
            self.answers = answers
            ideal_score = int(answers['ideal'][0])
            procr_score = int(answers['procrastination'][0])
            work_status = Constants.questionnaire_act_mappings[answers['work'][0]]
            (self.isprod,
            self.nonprod,
            self.isful,
            self.nonful,
            self.sleep) = generate_all(work_status,
                                       ideal_score,
                                       procr_score)

        else:
            self.data_schedule = self._base_pipeline(data)
            self.sleep = self._sleep_from_schedule(self.data_schedule)
            self.isprod = self._set_productive_data()
            self.nonprod = self._set_nonproductive_data()
            self.isful = self._set_fulfill_data()
            self.nonful = self._set_devastated_data()


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
        data['isful'] = data.act.map(mappings_full).astype('category')
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


    @staticmethod
    def _sleep_from_schedule(data: pd.DataFrame) -> pd.DataFrame:
        """
        Get sleep time per day based on scheduled data.
        :param data: Base-preprocessed dataframe.
        :type data: pd.DataFrame
        :return: Table with two columns: date and sleep in minutes.
        :rtype: pd.DataFrame
        """
        data = data.groupby('date').sum()
        data['minutes'] = 24 * 60 - data.minutes

        return pd.DataFrame(data['minutes'])

    @property
    def _prod_from_schedule(self) -> pd.DataFrame:
        """Data with date, productive_label, num of minutes."""
        data = self.data_schedule.groupby(['date', 'isprod']).sum()['minutes'].reset_index('isprod').reset_index()
        return data

    def _set_productive_data(self) -> pd.DataFrame:
        isprod = self._prod_from_schedule[self._prod_from_schedule.isprod == 1]
        isprod.index = isprod.date
        isprod.drop(['date', 'isprod'], axis=1, inplace=True)
        return isprod

    def _set_nonproductive_data(self) -> pd.DataFrame:
        nonprod = self._prod_from_schedule[self._prod_from_schedule.isprod == 0]
        nonprod.index = nonprod.date
        nonprod.drop(['date', 'isprod'], axis=1, inplace=True)
        return nonprod

    @property
    def _fulfill_from_schedule(self) -> pd.DataFrame:
        """Data with date, fulfill label, num of minutes."""
        data = self.data_schedule.groupby(['date', 'isful']).sum()['minutes'].reset_index('isful').reset_index()
        return data

    def _set_fulfill_data(self) -> pd.DataFrame:
        isful = self._fulfill_from_schedule[self._fulfill_from_schedule.isful == 1]
        isful.index = isful.date
        isful.drop(['date', 'isful'], axis=1, inplace=True)
        return isful

    def _set_devastated_data(self) -> pd.DataFrame:
        nonful = self._fulfill_from_schedule[self._fulfill_from_schedule.isful == 0]
        nonful.index = nonful.date
        nonful.drop(['date', 'isful'], axis=1, inplace=True)
        return nonful

a = DataStorage(answers={'procrastination': ('1',), 'work': ('Учеба',), 'workdaysleep': ('1:00',), 'weekendsleep': ('3:00',), 'ideal': ('2',)})
#
