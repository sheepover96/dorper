import numpy as np

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