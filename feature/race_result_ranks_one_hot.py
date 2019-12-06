import sys
import numpy as np

from .base import BaseFeature
from models import RacerInfo, RaceOdds, RaceInfo, RaceResultGrouped

#parent directory
sys.path.append('..')
from utils.setting import session

class RaceResultRanksOneHot(BaseFeature):
    feature_name = 'race_result_ranks_one_hot'
    feature_type = 'group'

    def __init__(self, race_info_list=None, year=None, *args, **kwargs):
        super().__init__()
        self.race_info_list = race_info_list
        self.year = year
        self.data_dic = {}

    def extract_feature(self):
        self.data_dic = {}
        for race_info_grouped in self.race_info_list:
            target_np_list = []

            target = np.zeros(6)
            target[race_info_grouped.RaceResultGrouped.lane1_result_rank-1] = 1
            target_np_list.append(target)

            target = np.zeros(6)
            target[race_info_grouped.RaceResultGrouped.lane2_result_rank-1] = 1
            target_np_list.append(target)

            target = np.zeros(6)
            target[race_info_grouped.RaceResultGrouped.lane3_result_rank-1] = 1
            target_np_list.append(target)

            target = np.zeros(6)
            target[race_info_grouped.RaceResultGrouped.lane4_result_rank-1] = 1
            target_np_list.append(target)

            target = np.zeros(6)
            target[race_info_grouped.RaceResultGrouped.lane5_result_rank-1] = 1
            target_np_list.append(target)

            target = np.zeros(6)
            target[race_info_grouped.RaceResultGrouped.lane6_result_rank-1] = 1
            target_np_list.append(target)

            target_all = np.concatenate(target_np_list)
            self.data_dic[race_info_grouped.RaceResultGrouped.race_num] = target_all

    def get_feature(self):
        return self.data_dic
