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
# valid_race_info_list_17 = session.query(RaceInfo, RaceResultGrouped)\
#     .filter(RaceInfo.year==2017, RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1).all()

# %%
from feature.race_result_ranks_one_hot import RaceResultRanksOneHot
race_result_ranks_one_hot = RaceResultRanksOneHot(race_info_list=valid_race_result_list_17, year=2017)
# %%
race_result_ranks_one_hot.extract_feature()
race_result_ranks_one_hot.save('./feature_pkls/race_result_ranks_one_hot_2017_all.pkl')

# %%
from feature.racer_info_base import RacerInfoBase
racer_info_base = RacerInfoBase(race_info_list=valid_race_result_list_17, year=2017)
racer_info_base.extract_feature()
racer_info_base.save('./feature_pkls/racer_info_base_2017_all.pkl')

#%%
from feature.racer_win_rate_year import RacerInfoWinRateYear
racer_win_rate_period = RacerInfoWinRateYear(race_info_list=valid_race_result_list_17, year=2017)
racer_win_rate_period.extract_feature()
racer_win_rate_period.save('./feature_pkls/racer_win_rate_year_2017.pkl')

