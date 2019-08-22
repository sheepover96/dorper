# %%
from sqlalchemy.sql import text

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import xgboost as xgb

import numpy as np

from models import RaceResult, RacerInfo, RaceInfo
from setting import session

rank_dic = {1:150, 2:100, 3:50, 4:0}


def load_train_data(year, data_num=1000000000):
    # for training
    race_result_list17 = session.query(RaceResult).filter(RaceResult.year==year)
    race_info_list17 = session.query(RaceInfo).filter(RaceInfo.year==year)
    racer_info_list16 = session.query(RacerInfo).filter(RacerInfo.year==(year-1))
    # for test
    #race_result_list2018 = session.query(RaceResult).filter(RaceResult.year==2018).all()
    #racer_info_list2018 = session.query(RacerInfo).filter(RacerInfo.year==2018).all()
    #race_id_list = racer_info_list17.filter(RaceResult.race_num).distinct(RaceResult.race_num).all()
    #race_result17_ordered = race_result_list17.order_by(RaceResult.race_num, RaceResult.pitout_lane).limit(data_num)
    #race_result17_ordered = session.execute('select * from race_result where year={} order by race_num, pitout_lane limit {};'.format(year, data_num*6))
    race_result_thisyear_ordered = session.execute('select * from race_result inner join race_info on\
                    race_result.race_num = race_info.race_num and race_result.year=race_info.year\
                    where race_result. year={} and is_race_no_flying=1 and is_race_times_record_valid=1 order by race_num, pitout_lane limit {};'.format(year, data_num*6))

    input_feature_list = []
    target_list = []                                                      
    feature_vec = []
    target_vec = []
    target_vec_part = [0 for i in range(6)]

    # create training data
    print('start')
    for idx, race_data in enumerate(race_result_thisyear_ordered):
        #print(idx)
        #race_info = race_info_list17.filter(RaceInfo.race_num==race_data.race_num).first()
        #race_info = session.execute('select * from race_info where race_num={} and year={};'.format(race_data.race_num, year)).first()
        ri = racer_info_list16.filter(RacerInfo.racer_id==race_data.racer_id).first()
        #ri = session.execute('select * from racer_info where racer_id={} and year={};'.format(race_data.racer_id, year-1)).first()
        if ri is not None:
            feature_vec_part = [ri.racer_sex, ri.racer_age, ri.racer_height, ri.racer_weight, ri.racer_win_rate, ri.racer_double_win_rate,\
                            ri.racer_first_arrival_times, ri.racer_second_arrival_times, ri.winner_race_start_times,\
                            ri.number_of_win, ri.average_start_timing, ri.previous_period_rank_int, ri.previous_second_period_rank_int,\
                            ri.previous_third_period_rank_int, ri.previous_period_capability_index, ri.this_period_capability_index]
            if len(feature_vec_part) != 16:
                print('flen', len(feature_vec_part))
            feature_vec += feature_vec_part

            target_vec_part[race_data.rank-1] = 1
            target_vec += target_vec_part
            target_vec_part[race_data.rank-1] = 0
        if race_data.pitout_lane == 6:
            print('idx', idx, race_data.race_num)
            if not (len(feature_vec) == 96 and len(target_vec) == 36):
                print('len', len(feature_vec), len(target_vec))
                print('no')
            if len(feature_vec) == 96:
                input_feature_list.append(feature_vec)
                target_list.append(target_vec)
            feature_vec = []
            target_vec = []
    return input_feature_list, target_list


# %%
session.rollback()
# %%
input_feature_list, target_list = load_train_data(2017, data_num=700)
    
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

# load test data 
test_feature_list, test_target_list = load_train_data(2018, data_num=100)

#%%
def onehot2rank_old(onehot_rank):
    rank_list = []
    for i in range(6):
        rank = np.argmax(onehot_rank[i*6:(i+1)*6])
        rank_list.append(rank+1)
    return rank_list

def onehot2rank(onehot_rank):
    racer_rank = np.array([-1 for i in range(6)])
    ranked_racer_list = []
    for i in range(6):
        rank_prob_list = []
        for j in range(6):
            rank_prob_list.append(onehot_rank[i+j*6])
        racer_rank_arg = np.argsort(rank_prob_list)[::-1]
        for k in range(6):
            if not racer_rank_arg[k] in ranked_racer_list:
                ranked_racer_list.append(racer_rank_arg[k])
                racer_rank[racer_rank_arg[k]] = i + 1
                break
    return racer_rank.tolist()

#%%
from utils.metrics import accuracy_tanshou, accuracy_fukushou, accuracy_nirentan, accuracy_nirenfuku, accuracy_sanrentan, accuracy_sanrenfuku
test_feature_np, test_target_np  = np.array(test_feature_list), np.array(test_target_list)
test_pred_res = model.predict(test_feature_np)
for idx, (pred, target) in enumerate(zip(test_pred_res, test_target_np)):
    print(idx)
    print(len(pred), len(target))
    print(onehot2rank(pred))
    print(onehot2rank(target))
pred_rank_list = [onehot2rank(pred) for pred in test_pred_res.tolist()]
target_rank_list = [onehot2rank(target) for target in test_target_list]
print('tanshou accuracy', accuracy_tanshou(pred_rank_list, target_rank_list))
print('fukushou accuracy', accuracy_fukushou(pred_rank_list, target_rank_list))
print('nirentan accuracy', accuracy_nirentan(pred_rank_list, target_rank_list))
print('nirenfuku accuracy', accuracy_nirenfuku(pred_rank_list, target_rank_list))
print('sanrentan accuracy', accuracy_sanrentan(pred_rank_list, target_rank_list))
print('sanrenfuku accuracy', accuracy_sanrenfuku(pred_rank_list, target_rank_list))

#%%
import utils.metrics as metrics


#%%
