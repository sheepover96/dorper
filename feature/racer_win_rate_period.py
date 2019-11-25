import sys
import numpy as np

from .Base import BaseFeature
from models import RacerInfo, RaceOdds, RaceInfo, RaceResultGrouped, RaceResult

#parent directory
sys.path.append('..')
from utils.setting import session

class RacerInfoWinRatePeriod(BaseFeature):
    feature_name = 'racer_info_win_rate_period'
    feature_type = 'group'
    feature_description = 'group'

    def ___init__(self, race_info_list, year):
        super().__init__()
        self.race_info_list = race_info_list
        self.year = year
        self.data_dic = {}

    def _calc_win_rate(self, racer_id, lane):
        nrace = session.query(RaceResult).filter(RaceResult.racer_id==racer_id,\
            RaceResult.year==self.year, RaceResult.period==2, RaceResult.pitout_lane==lane).count()

        nwon_race_on_lane = session.query(RaceResult).filter(RaceResult.racer_id==racer_id,\
            RaceResult.year==self.year, RaceResult.period==2, RaceResult.pitout_lane==lane,\
            RaceResult.rank==1).count()

        return nrace / nwon_race_on_lane

    def extract_feature(self):
        self.data_dic = {}
        for race_info_grouped in self.race_info_list:
            features = [None for i in range(6)]

            features[0] = self._calc_win_rate(race_info_grouped.lane1_racer_id, 1)
            features[1] = self._calc_win_rate(race_info_grouped.lane2_racer_id, 2)
            features[2] = self._calc_win_rate(race_info_grouped.lane3_racer_id, 3)
            features[3] = self._calc_win_rate(race_info_grouped.lane4_racer_id, 4)
            features[4] = self._calc_win_rate(race_info_grouped.lane5_racer_id, 5)
            features[5] = self._calc_win_rate(race_info_grouped.lane6_racer_id, 6)

            if None in features:
                self.data_dic[race_info_grouped.race_num] = features

    def get_feature(self):
        return self.data_dic
