import sys
import numpy as np

from .base import BaseFeature
from models import RacerInfo, RaceOdds, RaceInfo, RaceResultGrouped

#parent directory
sys.path.append('..')
from utils.setting import session

class RacerInfoBase(BaseFeature):
    feature_name = 'racer_info_base'
    feature_type = 'group'

    def ___init__(self, race_info_list, year):
        super().__init__()
        self.race_info_list = race_info_list
        self.year = year
        self.data_dic = {}

    def extract_feature(self):
        self.data_dic = {}
        for race_info_grouped in self.race_info_list:
            features = [None for i in range(6)]

            racer_id_lane1 = race_info_grouped.lane1_racer_id
            racer_info_lane1 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane1,\
                RacerInfo.year==self.year, RacerInfo.period==2).first()
            if (not racer_info_lane1):
                racer_info_lane1 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane1,\
                    RacerInfo.year==self.year, RacerInfo.period==1).first()

            if racer_info_lane1:
                features[0] = [racer_info_lane1.racer_win_rate,racer_info_lane1.racer_double_win_rate]
            else:
                continue

            racer_id_lane2 = race_info_grouped.lane2_racer_id
            racer_info_lane2 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane2,\
                RacerInfo.year==self.year, RacerInfo.period==2).first()
            if (not racer_info_lane2):
                racer_info_lane2 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane2,\
                    RacerInfo.year==self.year, RacerInfo.period==1).first()

            if racer_info_lane2:
                features[0] = [racer_info_lane2.racer_win_rate,racer_info_lane2.racer_double_win_rate]
            else:
                continue

            racer_id_lane3 = race_info_grouped.lane3_racer_id
            racer_info_lane3 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane3,\
                RacerInfo.year==self.year, RacerInfo.period==2).first()
            if (not racer_info_lane3):
                racer_info_lane3 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane3,\
                    RacerInfo.year==self.year, RacerInfo.period==1).first()

            if racer_info_lane3:
                features[0] = [racer_info_lane3.racer_win_rate,racer_info_lane3.racer_double_win_rate]
            else:
                continue

            racer_id_lane4 = race_info_grouped.lane4_racer_id
            racer_info_lane4 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane4,\
                RacerInfo.year==self.year, RacerInfo.period==2).first()
            if (not racer_info_lane4):
                racer_info_lane4 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane4,\
                    RacerInfo.year==self.year, RacerInfo.period==1).first()

            if racer_info_lane4:
                features[0] = [racer_info_lane4.racer_win_rate,racer_info_lane4.racer_double_win_rate]
            else:
                continue

            racer_id_lane5 = race_info_grouped.lane5_racer_id
            racer_info_lane5 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane5,\
                RacerInfo.year==self.year, RacerInfo.period==2).first()
            if (not racer_info_lane5):
                racer_info_lane5 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane5,\
                    RacerInfo.year==self.year, RacerInfo.period==1).first()

            if racer_info_lane5:
                features[0] = [racer_info_lane5.racer_win_rate,racer_info_lane5.racer_double_win_rate]
            else:
                continue

            racer_id_lane6 = race_info_grouped.lane6_racer_id
            racer_info_lane6 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane6,\
                RacerInfo.year==self.year, RacerInfo.period==2).first()
            if (not racer_info_lane6):
                racer_info_lane6 = session.query(RacerInfo).filter(RacerInfo.racer_id==racer_id_lane6,\
                    RacerInfo.year==self.year, RacerInfo.period==1).first()

            if racer_info_lane6:
                features[0] = [racer_info_lane6.racer_win_rate,racer_info_lane6.racer_double_win_rate]
            else:
                continue

            if None in features:
                self.data_dic[race_info_grouped.race_num] = features

    def get_feature(self):
        return self.data_dic

