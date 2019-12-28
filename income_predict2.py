# %%
from sqlalchemy.sql import text

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import numpy as np

from models import RaceResult, RacerInfo, RaceResultGrouped, RaceInfo
from utils.setting import session
from utils.data import load_data

# %%
session.rollback()

# %%
import lightgbm as lgb

from feature.join import Join
from feature.race_result_ranks_one_hot import RaceResultRanksOneHot
from feature.race_odds_year_validated import RaceOddsYearValidated

# %%
# data loaading
simple_feature17_obj = Join()
simple_feature17_obj.load('feature_pkls/simple_feature_17.pkl')
simple_feature17 = simple_feature17_obj.get_feature_list()

race_result_ranks_one_hot_17_all = RaceResultRanksOneHot()
race_result_ranks_one_hot_17_all.load('feature_pkls/race_result_ranks_one_hot_2017_all.pkl')
label17 = race_result_ranks_one_hot_17_all.get_feature()
label_list17 = [label17[key] for key in label17.keys()]

simple_feature18_obj = Join()
simple_feature18_obj.load('feature_pkls/simple_feature_18.pkl')
simple_feature18 = simple_feature18_obj.get_feature_list()

race_result_ranks_one_hot_18_all = RaceResultRanksOneHot()
race_result_ranks_one_hot_18_all.load('feature_pkls/race_result_ranks_one_hot_2018_all.pkl')
label18 = race_result_ranks_one_hot_18_all.get_feature()
label_list18 = [label18[key] for key in label18.keys()]

race_odds_year_validated18 = RaceOddsYearValidated()
race_odds_year_validated18.load('feature_pkls/race_odds_year_validated_2018.pkl')
race_odds_year_validated18_dic = race_odds_year_validated18.get_feature()

# %%
from sklearn.ensemble import RandomForestRegressor
from utils.util import onehot2rank

# train

# lgb_train = lgb.Dataset(np.array(simple_feature17), np.ones(len(label17)))
# lgbm_params = {
#     'objective': 'regression'
# }

# model = lgb.train(lgbm_params, lgb_train)
model = RandomForestRegressor()
model.fit(simple_feature17, label_list17)
predicted_res = model.predict(simple_feature18)
predicted_res_onehot = [onehot2rank(predicted_res[idx]) for idx in range(len(predicted_res))]

# %%
from utils.purchase_pattern import get_sanrentan_nagashi_222_pattern
valid_race_result_list_18 = session.query(RaceInfo, RaceResultGrouped)\
    .join(RaceInfo, RaceInfo.race_num==RaceResultGrouped.race_num)\
    .filter(RaceInfo.year==RaceResultGrouped.year, RaceInfo.year==2018,\
    RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1).all()

payment = 0
revenue = 0
hit = 0
for idx, (predicted_res, label, key) in enumerate(zip(predicted_res_onehot, label_list18, race_odds_year_validated18_dic.keys())):
    rank_label = onehot2rank(label)
    label_top3_lane = [rank_label.index(1)+1, rank_label.index(2)+1, rank_label.index(3)+1]
    sanrentan_pattern = get_sanrentan_nagashi_222_pattern(predicted_res)
    sanrentan_odds = race_odds_year_validated18_dic[key]['sanrentan']
    if sanrentan_odds:
        if label_top3_lane in sanrentan_pattern:
            revenue += sanrentan_odds
            hit += 1
        payment += len(sanrentan_pattern) * 100



# %%
