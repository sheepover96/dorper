#%%
import numpy as np
import pandas as pd

from models import Base, RaceResult, RacerInfo, RaceOdds, RaceInfo

from setting import session
from utils.data import get_target_race_nums, get_feature_race_nums, load_training_data
import utils.income_metrics as icmtr

import matplotlib.pyplot as plt

#%%

target_race_num_list_feature = get_feature_race_nums()
target_race_num_list_target = get_target_race_nums()
target_race_num_list = list(set(target_race_num_list_feature) & set(target_race_num_list_target))
input_features, target_labels = load_training_data(target_race_num_list)

null_idx_arr = pd.isnull(input_features)
null_idx = [True in i for i in null_idx_arr]
notnull_dx = [not i for i in null_idx]
print(input_features.shape)
print(target_labels.shape)
input_features = input_features[notnull_dx]
target_labels = target_labels[notnull_dx]

#%%
from sklearn import linear_model
linear = linear_model.LinearRegression()
linear.fit(input_features, target_labels)
#%%
race_numbers, test_input_features, test_target_label, odds_rank_top3s, odds_dir = load_test_data()
#%%
T_ctr = 0
TOP_N = 1
income_list = []
correct_prob_list = []
incorrect_prob_list = []

payment_sum = 0; revenue_sum = 0

for race_num, feature, label, odds_rank_top3, odds in zip(race_numbers, test_input_features, test_target_label, odds_rank_top3s, odds_dir["sanrentan"]):
    feature = np.reshape(feature, (-1,24))
    predicted = linear.predict(feature)
    pred_cliped = np.clip(predicted[0], 0, 1)
    target_comb_dic = {(odds_rank_top3[0]-1, odds_rank_top3[1]-1, odds_rank_top3[2]-1): odds}

    if race_num == 68:
        print(odds_rank_top3)
        print(target_comb_dic)
    payment, revenue = income_sanrentan(race_num, pred_cliped, target_comb_dic, method='ntop', ntop=1)
    if revenue != 0:
        print(race_num, odds_rank_top3)
    payment_sum += payment
    revenue_sum += revenue

print(payment_sum)
print(revenue_sum)


#%%

from itertools import permutations, combinations

def get_lane_win_prob(racer_win_prob, lane, rank):
    return racer_win_prob[lane*6+rank]

def income_sanrentan(race_num, racer_win_prob, target_comb_dic, method='ntop', threshold=0.1, ntop=5):
    sanrentan_problist = problist_sanrentan(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(sanrentan_problist.items(), key=lambda x:x[1], reverse=True)
    if method == 'threshold':
        for comb, prob in prob_sorted:
            if prob < threshold: break
            payment += 100
            if comb in target_comb_dic:
                revenue += target_comb_dic[comb]
    elif method == 'ntop':
        for comb, prob in prob_sorted[:ntop]:
            if race_num == 68:
                print(comb)
            payment += 100
            if comb in target_comb_dic:
                revenue += target_comb_dic[comb]
    return payment, revenue

def problist_sanrentan(racer_win_prob):
    sanrentan_comb = list(permutations(range(6), 3))
    problist = {}
    for comb in sanrentan_comb:
        problist[comb] = get_lane_win_prob(racer_win_prob, comb[0], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[1], 1) *\
                        get_lane_win_prob(racer_win_prob, comb[2], 2)
    return problist

#%%
