import pytest

from ..utils import income_metrics as em

def test_tanshou_income():
    test_win_prob =[0.9, 0, 0, 0, 0, 0.1,
                    0, 0.2, 0, 0.1, 0.4, 0.3,
                    0, 0.2, 0, 0.1, 0.2, 0.5,
                    0.1, 0.2, 0.5, 0.2, 0, 0,
                    0, 0.3, 0.4, 0.1, 0.2, 0,
                    0, 0.1, 0.1, 0.5, 0.2, 0.1]
    target_rank_list = [1, 5, 4]
    race_odds = 120
    threshold1 = 0.9
    threshold2 = 0.1
    threshold3 = 1.0
    target_comb_dic = { (target_rank_list[0]-1,): race_odds }

    payment1, revenue1 = em.income_tanshou(test_win_prob, target_comb_dic, threshold1)
    assert payment1 == 100 and revenue1 == race_odds
    payment2, revenue2 = em.income_tanshou(test_win_prob, target_comb_dic, threshold2)
    assert payment2 == 200 and revenue2 == race_odds
    payment3, revenue3 = em.income_tanshou(test_win_prob, target_comb_dic, threshold3)
    assert payment3 == 0 and revenue3 == 0

def test_fukushou_income():
    test_win_prob =[0.4, 0, 0.6, 0, 0, 0,
                    0.6, 0.3, 0.1, 0, 0, 0,
                    0, 0.7, 0.1, 0, 0.2, 0,
                    0, 0, 0.1, 0.8, 0, 0.1,
                    0, 0, 0.1, 0.1, 0.6, 0.2,
                    0, 0, 0, 0.1, 0.2, 0.7]
    target_rank_list = [2, 3, 1]
    race_odds1 = 210
    race_odds2 = 580
    threshold1 = 0.8
    threshold2 = 0.6
    threshold3 = 0.4
    target_comb_dic = {(target_rank_list[0]-1,): race_odds1,
                        (target_rank_list[1]-1,): race_odds2}

    payment1, revenue1 = em.income_fukushou(test_win_prob, target_comb_dic, threshold1)
    assert payment1 == 100 and revenue1 == race_odds1
    payment2, revenue2 = em.income_fukushou(test_win_prob, target_comb_dic, threshold2)
    assert payment2 == 200 and revenue2 == race_odds1 + race_odds2
    payment3, revenue3 = em.income_fukushou(test_win_prob, target_comb_dic, threshold3)
    assert payment3 == 300 and revenue3 == race_odds1 + race_odds2

def test_nirentan_income():
    test_win_prob =[0.4, 0, 0.6, 0, 0, 0,
                    0.6, 0.3, 0.1, 0, 0, 0,
                    0, 0.7, 0.1, 0, 0.2, 0,
                    0, 0, 0.1, 0.8, 0, 0.1,
                    0, 0, 0.1, 0.1, 0.6, 0.2,
                    0, 0, 0, 0.1, 0.2, 0.7]
    target_rank_list = [2, 3, 1]
    race_odds = 1510
    threshold1 = 0.4
    threshold2 = 0.2
    target_comb_dic = {(target_rank_list[0]-1, target_rank_list[1]-1): race_odds}

    payment1, revenue1 = em.income_nirentan(test_win_prob, target_comb_dic, threshold1)
    assert payment1 == 100 and revenue1 == race_odds
    payment2, revenue2 = em.income_nirentan(test_win_prob, target_comb_dic, threshold2)
    assert payment2 == 200 and revenue2 == race_odds

def test_nirenfuku_income():
    test_win_prob =[0.4, 0, 0.6, 0, 0, 0,
                    0.6, 0.3, 0.1, 0, 0, 0,
                    0, 0.7, 0.1, 0, 0.2, 0,
                    0, 0, 0.1, 0.8, 0, 0.1,
                    0, 0, 0.1, 0.1, 0.6, 0.2,
                    0, 0, 0, 0.1, 0.2, 0.7]
    target_rank_list = [2, 3, 1]
    race_odds = 1580
    threshold1 = 0.4
    threshold2 = 0.2
    target_comb_set = {(target_rank_list[0]-1, target_rank_list[1]-1): race_odds}

    payment1, revenue1 = em.income_nirentan(test_win_prob, target_comb_set, threshold1)
    assert payment1 == 100 and revenue1 == race_odds
    payment2, revenue2 = em.income_nirentan(test_win_prob, target_comb_set, threshold2)
    assert payment2 == 200 and revenue2 == race_odds

def test_sanrentan_income():
    test_win_prob =[0.4, 0, 0.6, 0, 0, 0,
                    0.6, 0.3, 0.1, 0, 0, 0,
                    0, 0.7, 0.1, 0, 0.2, 0,
                    0, 0, 0.1, 0.8, 0, 0.1,
                    0, 0, 0.1, 0.1, 0.6, 0.2,
                    0, 0, 0, 0.1, 0.2, 0.7]
    target_rank_list = [2, 3, 1]
    race_odds = 3370
    threshold1 = 0.2
    threshold2 = 0.04
    target_comb_dic = {(target_rank_list[0]-1, target_rank_list[1]-1,
                        target_rank_list[2]-1): race_odds}

    payment1, revenue1 = em.income_sanrentan(test_win_prob, target_comb_dic, threshold1)
    assert payment1 == 100 and revenue1 == race_odds
    payment2, revenue2 = em.income_sanrentan(test_win_prob, target_comb_dic, threshold2)
    assert payment2 == 300 and revenue2 == race_odds

def test_sanrenfuku_income():
    test_win_prob =[0.4, 0, 0.6, 0, 0, 0,
                    0.6, 0.3, 0.1, 0, 0, 0,
                    0, 0.7, 0.1, 0, 0.2, 0,
                    0, 0, 0.1, 0.8, 0, 0.1,
                    0, 0, 0.1, 0.1, 0.6, 0.2,
                    0, 0, 0, 0.1, 0.2, 0.7]
    target_rank_list = [2, 3, 1]
    race_odds = 200
    threshold1 = 0.2
    threshold2 = 0.02
    target_comb_dic = {(target_rank_list[0]-1, target_rank_list[1]-1,
                        target_rank_list[2]-1): race_odds}

    payment1, revenue1 = em.income_sanrenfuku(test_win_prob, target_comb_dic, threshold1)
    assert payment1 == 100 and revenue1 == race_odds
    payment2, revenue2 = em.income_sanrenfuku(test_win_prob, target_comb_dic, threshold2)
    assert payment2 == 500 and revenue2 == race_odds