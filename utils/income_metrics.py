from itertools import permutations, combinations

# 各選手のレーンごとの予想勝率を元に収益を計算
def get_lane_win_prob(racer_win_prob, lane, rank):
    return racer_win_prob[lane*6+rank]

def income_tanshou(racer_win_prob, target_comb_dic, method='ntop', threshold=0.1, ntop=5):
    tanshou_prolist = problist_tanshou(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(tanshou_prolist.items(), key=lambda x:x[1], reverse=True)
    if method == 'threshold':
        for comb, prob in prob_sorted:
            if prob < threshold: break
            payment += 100
            if comb in target_comb_dic:
                revenue += target_comb_dic[comb]
    elif method == 'ntop':
        for comb, prob in prob_sorted[:ntop]:
            payment += 100
            if comb in target_comb_dic:
                revenue += target_comb_dic[comb]
    return payment, revenue

def problist_tanshou(racer_win_prob):
    tanshou_combs = list(permutations(range(6), 1))
    problist = {}
    for comb in tanshou_combs:
        problist[comb] = get_lane_win_prob(racer_win_prob, comb[0], 0)
    return problist

def income_fukushou(racer_win_prob, target_comb_dic, method='ntop', threshold=0.1, ntop=5):
    fukushou_prolist = problist_fukushou(racer_win_prob)
    revenue = 0
    payment = 0
    sorted_key_target_comb_dic = {}
    for (key, val) in target_comb_dic.items():
        sorted_key = tuple(sorted(key))
        sorted_key_target_comb_dic[sorted_key] = val
    prob_sorted = sorted(fukushou_prolist.items(), key=lambda x:x[1], reverse=True)
    if method == 'threshold':
        for comb, prob in prob_sorted:
            if prob < threshold: break
            payment += 100
            if comb in sorted_key_target_comb_dic:
                revenue += sorted_key_target_comb_dic[comb]
    elif method == 'ntop':
        for comb, prob in prob_sorted[:ntop]:
            payment += 100
            if comb in sorted_key_target_comb_dic:
                revenue += sorted_key_target_comb_dic[comb]
    return payment, revenue

def problist_fukushou(racer_win_prob):
    fukushou_comb = list(combinations(range(6), 1))
    problist = {}
    for comb in fukushou_comb:
        problist[comb] = get_lane_win_prob(racer_win_prob, comb[0], 0) +\
                        get_lane_win_prob(racer_win_prob, comb[0], 1)
    return problist

def income_nirentan(racer_win_prob, target_comb_dic, method='ntop', threshold=0.1, ntop=5):
    nirentan_prolist = problist_nirentan(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(nirentan_prolist.items(), key=lambda x:x[1], reverse=True)
    if method == 'threshold':
        for comb, prob in prob_sorted:
            if prob < threshold: break
            payment += 100
            if comb in target_comb_dic:
                revenue += target_comb_dic[comb]
    elif method == 'ntop':
        for comb, prob in prob_sorted[:ntop]:
            payment += 100
            if comb in target_comb_dic:
                revenue += target_comb_dic[comb]
    return payment, revenue

def problist_nirentan(racer_win_prob):
    nirentan_comb = list(permutations(range(6), 2))
    problist = {}
    for comb in nirentan_comb:
        problist[comb] = get_lane_win_prob(racer_win_prob, comb[0], 0)\
                        * get_lane_win_prob(racer_win_prob, comb[1], 1)
    return problist

def income_nirenfuku(racer_win_prob, target_comb_dic, method='ntop', threshold=0.1, ntop=5):
    nirenfuku_prolist = problist_nirenfuku(racer_win_prob)
    revenue = 0
    payment = 0
    sorted_key_target_comb_dic = {}
    for (key, val) in target_comb_dic.items():
        sorted_key = tuple(sorted(key))
        sorted_key_target_comb_dic[sorted_key] = val
    prob_sorted = sorted(nirenfuku_prolist.items(), key=lambda x:x[1], reverse=True)
    if method == 'threshold':
        for comb, prob in prob_sorted:
            if prob < threshold: break
            payment += 100
            if comb in sorted_key_target_comb_dic:
                revenue += sorted_key_target_comb_dic[comb]
    elif method == 'ntop':
        for comb, prob in prob_sorted[:ntop]:
            payment += 100
            if comb in sorted_key_target_comb_dic:
                revenue += sorted_key_target_comb_dic[comb]
    return payment, revenue

def problist_nirenfuku(racer_win_prob):
    nirenfuku_comb = list(combinations(range(6), 2))
    problist = {}
    for comb in nirenfuku_comb:
        problist[comb] = get_lane_win_prob(racer_win_prob, comb[0], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[1], 1) +\
                        get_lane_win_prob(racer_win_prob, comb[1], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[0], 1)
    return problist

#def problist_kakuranfuku(racer_win_prob):
#    kakurenfuku_comb = list(combinations(range(6), 2))
#    problist = {}
#    for comb in kakurenfuku_comb:
#        problist[comb] = get_lane_win_prob(racer_win_prob, comb[0], 0) *\
#                        get_lane_win_prob(racer_win_prob, comb[1], 1) +\
#                        get_lane_win_prob(racer_win_prob, comb[1], 0) *\
#                        get_lane_win_prob(racer_win_prob, comb[0], 1)

def income_sanrentan(racer_win_prob, target_comb_dic, method='ntop', threshold=0.1, ntop=5):
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

def income_sanrenfuku(racer_win_prob, target_comb_dic, method='ntop', threshold=0.1, ntop=5):
    sanrenfuku_prolist = problist_sanrenfuku(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(sanrenfuku_prolist.items(), key=lambda x:x[1], reverse=True)
    sorted_key_target_comb_dic = {}
    for (key, val) in target_comb_dic.items():
        sorted_key = tuple(sorted(key))
        sorted_key_target_comb_dic[sorted_key] = val
    if method == 'threshold':
        for comb, prob in prob_sorted:
            if prob < threshold: break
            payment += 100
            if comb in sorted_key_target_comb_dic:
                revenue += sorted_key_target_comb_dic[comb]
    elif method == 'ntop':
        for comb, prob in prob_sorted[:ntop]:
            payment += 100
            if comb in target_comb_dic:
                revenue += sorted_key_target_comb_dic[comb]
    return payment, revenue

def problist_sanrenfuku(racer_win_prob):
    sanrenfuku_comb = list(combinations(range(6), 3))
    problist = {}
    for comb in sanrenfuku_comb:
        problist[comb] = get_lane_win_prob(racer_win_prob, comb[0], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[1], 1) *\
                        get_lane_win_prob(racer_win_prob, comb[2], 2) +\
                        get_lane_win_prob(racer_win_prob, comb[0], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[2], 1) *\
                        get_lane_win_prob(racer_win_prob, comb[1], 2) +\
                        get_lane_win_prob(racer_win_prob, comb[1], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[0], 1) *\
                        get_lane_win_prob(racer_win_prob, comb[2], 2) +\
                        get_lane_win_prob(racer_win_prob, comb[1], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[2], 1) *\
                        get_lane_win_prob(racer_win_prob, comb[0], 2) +\
                        get_lane_win_prob(racer_win_prob, comb[2], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[1], 1) *\
                        get_lane_win_prob(racer_win_prob, comb[0], 2) +\
                        get_lane_win_prob(racer_win_prob, comb[2], 0) *\
                        get_lane_win_prob(racer_win_prob, comb[0], 1) *\
                        get_lane_win_prob(racer_win_prob, comb[1], 2)
    return problist