from itertools import permutations, combinations

# 三連単の購入パターン

## 1位1人，2位1人，3位2人の組み合わせ
def get_sanrentan_nagashi_112_pattern(pred_result):
    pass

## 1,2位2人，3位4人の組み合わせ
def get_nagashi_22all_pattern(pred_result):
    purchase_patterns = []
    top2_lane_list = [pred_result.index(1)+1, pred_result.index(2)+1]
    top2_patterns = list(permutations(top2_lane_list))
    lower4_lane_list = [pred_result.index(3)+1, pred_result.index(4)+1,\
                       pred_result.index(5)+1, pred_result.index(6)+1]
    lower4_patterns = list(combinations(lower4_lane_list, 1))
    for top2_pattern in top2_patterns:
        for lower4_pattern in lower4_patterns:
            top2_pattern_list = list(top2_pattern)
            top2_pattern_list.extend(list(lower4_pattern))
            purchase_patterns.append(top2_pattern_list)

    return purchase_patterns

## 1,2位2人，3位2人の組み合わせ
def get_sanrentan_nagashi_222_pattern(pred_result):
    purchase_patterns = []
    top2_lane_list = [pred_result.index(1)+1, pred_result.index(2)+1]
    top2_patterns = list(permutations(top2_lane_list))
    lower2_lane_list = [pred_result.index(3)+1, pred_result.index(4)+1]
    lower2_patterns = list(combinations(lower2_lane_list, 1))
    for top2_pattern in top2_patterns:
        for lower2_pattern in lower2_patterns:
            top2_pattern_list = list(top2_pattern)
            top2_pattern_list.extend(list(lower2_pattern))
            purchase_patterns.append(top2_pattern_list)

    return purchase_patterns

## 上位n人の組み合わせを全て購入
def get_sanrentan_boxn_pattern(pred_result, n=3):
    topn_lane_list = []
    for i in range(n):
        topn_lane_list.append(pred_result.index(i+1)+1)
    topn_permutation = list(permutations(topn_lane_list))
    purchase_patterns = list(map(lambda x: list(x[:3]), topn_permutation))

    return purchase_patterns