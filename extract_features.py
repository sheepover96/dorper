# %%
from utils.setting import session
from models import RaceResultGrouped, RaceInfo

valid_race_result_list_18 = session.query(RaceInfo, RaceResultGrouped)\
    .filter(RaceInfo.race_num==RaceResultGrouped.race_num, RaceInfo.year==RaceResultGrouped.year,\
    RaceInfo.year==2018, RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1).all()
# valid_race_info_list_17 = session.query(RaceInfo, RaceResultGrouped)\
#     .filter(RaceInfo.year==2017, RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1).all()

# %%
from feature.race_result_ranks_one_hot import RaceResultRanksOneHot
race_result_ranks_one_hot = RaceResultRanksOneHot(valid_race_result_list_18, 2018)
# %%
race_result_ranks_one_hot.extract_feature()
race_result_ranks_one_hot.save('./feature_pkls/race_result_ranks_one_hot_2018_all.pkl')

# %%
from feature.racer_info_base import RacerInfoBase
race_result_ranks_one_hot = RaceResultRanksOneHot(valid_race_info_list_17, 2018)
race_result_ranks_one_hot.extract_feature()
race_result_ranks_one_hot.save('./feature_pkls/race_result_ranks_one_hot_2018_all.pkl')
