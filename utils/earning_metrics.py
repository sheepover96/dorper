from itertools import permutations, combinations

def get_lane_win_prob(racer_win_prob, lane, rank):
    return racer_win_prob[lane*6+rank]

def earning_tanshou(racer_win_prob, target_comb_dic, threshold):
    tanshou_prolist = problist_tanshou(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(tanshou_prolist.items(), key=lambda x:x[1], reverse=True)
    for comb, prob in prob_sorted:
        if prob < threshold: break
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

def earning_fukushou(racer_win_prob, target_comb_dic, threshold):
    fukushou_prolist = problist_fukushou(racer_win_prob)
    revenue = 0
    payment = 0
    sorted_key_target_comb_dic = {}
    for (key, val) in target_comb_dic.items():
        sorted_key = tuple(sorted(key))
        sorted_key_target_comb_dic[sorted_key] = val
    prob_sorted = sorted(fukushou_prolist.items(), key=lambda x:x[1], reverse=True)
    for comb, prob in prob_sorted:
        if prob < threshold: break
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

def earning_nirentan(racer_win_prob, target_comb_dic, threshold):
    nirentan_prolist = problist_nirentan(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(nirentan_prolist.items(), key=lambda x:x[1], reverse=True)
    for comb, prob in prob_sorted:
        if prob < threshold: break
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

def earning_nirenfuku(racer_win_prob, target_comb_dic, threshold):
    nirenfuku_prolist = problist_nirenfuku(racer_win_prob)
    revenue = 0
    payment = 0
    sorted_key_target_comb_dic = {}
    for (key, val) in target_comb_dic.items():
        sorted_key = tuple(sorted(key))
        sorted_key_target_comb_dic[sorted_key] = val
    prob_sorted = sorted(nirenfuku_prolist.items(), key=lambda x:x[1], reverse=True)
    for comb, prob in prob_sorted:
        if prob < threshold: break
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

def earning_sanrentan(racer_win_prob, target_comb_dic, threshold):
    sanrentan_prolist = problist_sanrentan(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(sanrentan_prolist.items(), key=lambda x:x[1], reverse=True)
    for comb, prob in prob_sorted:
        if prob < threshold: break
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

def earning_sanrenfuku(racer_win_prob, target_comb_dic, threshold):
    sanrenfuku_prolist = problist_sanrenfuku(racer_win_prob)
    revenue = 0
    payment = 0
    prob_sorted = sorted(sanrenfuku_prolist.items(), key=lambda x:x[1], reverse=True)
    sorted_key_target_comb_dic = {}
    for (key, val) in target_comb_dic.items():
        sorted_key = tuple(sorted(key))
        sorted_key_target_comb_dic[sorted_key] = val
    for comb, prob in prob_sorted:
        if prob < threshold: break
        payment += 100
        if comb in sorted_key_target_comb_dic:
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