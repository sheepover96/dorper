import sys
import numpy as np

from .base import BaseFeature
from models import RacerInfo, RaceOdds, RaceInfo, RaceResultGrouped

#parent directory
sys.path.append('..')
from utils.setting import session

class RaceResultWinOrNot(BaseFeature):
    feature_name = 'race_result_win_or_not'
    feature_type = 'group'

    def __init__(self, race_info_list=None, year=None, win_threshold=3, *args, **kwargs):
        super().__init__()
        self.race_info_list = race_info_list
        self.year = year
        self.win_threshold = win_threshold
        self.data_dic = {}

    def extract_feature(self):
        self.data_dic = {}
        for race_info_grouped in self.race_info_list:
            target = [0 for i in range(6)]

            if race_info_grouped.RaceResultGrouped.lane1_result_rank\
                <= self.win_threshold:
                target[0] = 1

            if race_info_grouped.RaceResultGrouped.lane2_result_rank\
                <= self.win_threshold:
                target[1] = 1

            if race_info_grouped.RaceResultGrouped.lane3_result_rank\
                <= self.win_threshold:
                target[2] = 1

            if race_info_grouped.RaceResultGrouped.lane4_result_rank\
                <= self.win_threshold:
                target[3] = 1

            if race_info_grouped.RaceResultGrouped.lane5_result_rank\
                <= self.win_threshold:
                target[4] = 1

            if race_info_grouped.RaceResultGrouped.lane6_result_rank\
                <= self.win_threshold:
                target[5] = 1

            self.data_dic[race_info_grouped.RaceResultGrouped.race_num] = target

    def get_feature(self):
        return self.data_dic
