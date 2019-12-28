import sys
import numpy as np

from .base import BaseFeature
from models import RaceOdds, RaceInfo

#parent directory
sys.path.append('..')
from utils.setting import session

class RaceOddsYearValidated(BaseFeature):

    def __init__(self, race_info_list=None, year=None, *args, **kwargs):
        super().__init__()
        self.race_info_list = race_info_list
        self.year = year
        self.data_dic = {}

    def extract_feature(self):
        self.data_dic = {}
        for race_info_grouped in self.race_info_list:
            race_odds = session.query(RaceOdds).filter(RaceOdds.year==self.year,\
                        RaceOdds.race_num==race_info_grouped.RaceResultGrouped.race_num).first()
            if race_odds:
                data = {'result':[race_odds.rank1_lane, race_odds.rank2_lane, race_odds.rank3_lane],\
                        'tanshou': race_odds.tanshou, 'sanrentan': race_odds.sanrentan}
                self.data_dic[race_info_grouped.RaceResultGrouped.race_num] = data

    def get_feature(self):
        return self.data_dic
