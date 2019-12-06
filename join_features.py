# %%
from utils.setting import session
from models import RaceResultGrouped, RaceInfo
# %%
session.rollback()

# %%

valid_race_result_list_17 = session.query(RaceInfo, RaceResultGrouped)\
    .join(RaceInfo, RaceInfo.race_num==RaceResultGrouped.race_num)\
    .filter(RaceInfo.year==RaceResultGrouped.year, RaceInfo.year==2017,\
    RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1).all()

#%%
from feature.racer_win_rate_year import RacerInfoWinRateYear
from feature.racer_info_base import RacerInfoBase
from utils.pickle_helper import pickle_load
racer_info_base_2017 = RacerInfoBase()
racer_info_base_2017.load('feature_pkls/racer_win_rate_year_2017.pkl')
race_win_rate_year_2017 = RacerInfoWinRateYear()
race_win_rate_year_2017.load('feature_pkls/racer_win_rate_year_2017.pkl')

#%%
from feature.join import Join
race_id_list = [ race.RaceInfo.race_num for race in valid_race_result_list_17]

group_feature_dic_list = [racer_info_base_2017.get_feature(),\
                          race_win_rate_year_2017.get_feature()]
simple_feature_17 = Join(id_list=race_id_list,\
                         group_features_dic_list=group_feature_dic_list)
simple_feature_17.join_feature()
simple_feature_17.save('feature_pkls/simple_feature_17.pkl')


#%%
