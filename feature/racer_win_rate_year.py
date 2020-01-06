import sys
import numpy as np

from .base import BaseFeature
from models import RacerInfo, RaceOdds, RaceInfo, RaceResultGrouped, RaceResult

#parent directory
sys.path.append('..')
from utils.setting import session

class RacerInfoWinRateYear(BaseFeature):
    feature_name = 'racer_info_win_rate_year'
    feature_type = 'group'
    feature_description = 'group'

    def __init__(self, race_info_list=None, year=None):
        super().__init__()
        self.race_info_list = race_info_list
        self.year = year
        self.data_dic = {}

    def _calc_win_rate(self, racer_id, lane):
        race_result_tmp = session.query(RaceResult).filter(RaceResult.racer_id==racer_id,\
            RaceResult.year==self.year-1, RaceResult.pitout_lane==lane)

        nrace = race_result_tmp.count()
        nwon_race_on_lane = race_result_tmp.filter(RaceResult.rank==1).count()

        if nrace != 0:
            return nwon_race_on_lane / nrace
        else:
            return None

    def extract_feature(self):
        self.data_dic = {}
        for race_info_grouped in self.race_info_list:
            features = [None for i in range(6)]

            features[0] = self._calc_win_rate(race_info_grouped.RaceResultGrouped.lane1_racer_id, 1)
            features[1] = self._calc_win_rate(race_info_grouped.RaceResultGrouped.lane2_racer_id, 2)
            features[2] = self._calc_win_rate(race_info_grouped.RaceResultGrouped.lane3_racer_id, 3)
            features[3] = self._calc_win_rate(race_info_grouped.RaceResultGrouped.lane4_racer_id, 4)
            features[4] = self._calc_win_rate(race_info_grouped.RaceResultGrouped.lane5_racer_id, 5)
            features[5] = self._calc_win_rate(race_info_grouped.RaceResultGrouped.lane6_racer_id, 6)

            if not None in features:
                self.data_dic[race_info_grouped.RaceResultGrouped.race_num] = features

    def get_feature(self):
        return self.data_dic
