# %%
from sqlalchemy.sql import text

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import xgboost as xgb

import numpy as np

from models import RaceResult, RacerInfo, RaceInfo
from setting import session
from utils.data import load_data

# %%
session.rollback()

# %%
# load train data
input_feature_list, target_list, odds_list = load_data(2016, data_num=1600)

# %%
from sklearn.ensemble import RandomForestRegressor
# train model
kfold = KFold(n_splits=4)
for train_idxs, val_idxs in kfold.split(input_feature_list):
    train_feature = [input_feature_list[train_idx] for train_idx in train_idxs]
    train_feature_np = np.array(train_feature)
    print(train_feature_np.shape)
    train_target = [target_list[train_idx] for train_idx in train_idxs]
    train_target_np = np.array(train_target)
    print(train_target_np.shape)

    val_feature = [input_feature_list[val_idx] for val_idx in val_idxs]
    val_feature_np = np.array(val_feature)
    val_target = [target_list[val_idx] for val_idx in val_idxs]
    val_target_np = np.array(val_target)

    model = RandomForestRegressor()
    model.fit(train_feature_np, train_target_np)

    pred_res = model.predict(val_feature_np)

    print(metrics.mean_squared_error(pred_res, val_target_np))

#%%

# load val data
val_feature_list, val_target_list, val_odds_list = load_data(2017, data_num=100)
# load test data
test_feature_list, test_target_list, test_odds_list = load_data(2018, data_num=100)

#%%
from utils.util import onehot2rank
from utils import earning_metrics as em

# validation
val_feature_np, val_target_np  = np.array(val_feature_list), np.array(val_target_list)
val_pred_list = model.predict(val_feature_np)
pred_rank_list = [onehot2rank(pred) for pred in val_pred_list]
target_rank_list = [onehot2rank(target) for target in val_target_list]

payment_sum = 0
revenue_sum = 0

for (val_pred, val_odds) in zip(val_pred_list, val_odds_list):
    sanrentan_comb_dic = {(val_odds.rank1_lane-1, val_odds.rank2_lane-1,
                            val_odds.rank3_lane-1): val_odds.sanrentan}
    payment, revenue = em.earning_sanrentan(val_pred, sanrentan_comb_dic, 0.05)
    payment_sum += payment
    revenue_sum += revenue

print(payment_sum, revenue_sum)


#%%
from utils.util import onehot2rank
from utils import earning_metrics as em

# earning test

