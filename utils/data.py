import numpy as np
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import case, cast, Float

from models import RaceResult, RacerInfo, RaceInfo, RaceOdds
from setting import session
from collections import namedtuple

rank_dic = {1:150, 2:100, 3:50, 4:0}
RaceOddsInfo = namedtuple('RaceOddsInfo', ['rank1_lane', 'rank2_lane', 'rank3_lane',
                                           'tanshou', 'fukushou1', 'fukushou2', 'nirentan',
                                           'nirenfuku', 'kakurenfuku1_2', 'kakurenfuku1_3',
                                           'kakurenfuku2_3', 'sanrentan', 'sanrenfuku'])

def load_data(year, data_num=1000000000):
    # for training
    race_result_list_this_year = session.query(RaceResult).filter(RaceResult.year==year)
    race_info_list_this_year = session.query(RaceInfo).filter(RaceInfo.year==year)
    race_odds_list_this_year = session.query(RaceOdds).filter(RaceOdds.year==year)
    racer_info_list_last_year = session.query(RacerInfo).filter(RacerInfo.year==(year-1))
    # for test
    #race_result_list2018 = session.query(RaceResult).filter(RaceResult.year==2018).all()
    #racer_info_list2018 = session.query(RacerInfo).filter(RacerInfo.year==2018).all()
    #race_id_list = racer_info_list17.filter(RaceResult.race_num).distinct(RaceResult.race_num).all()
    #race_result17_ordered = race_result_list17.order_by(RaceResult.race_num, RaceResult.pitout_lane).limit(data_num)
    #race_result17_ordered = session.execute('select * from race_result where year={} order by race_num, pitout_lane limit {};'.format(year, data_num*6))

    #race_result_thisyear_ordered = session.execute('select * from inner join race_info on race_result.race_num = race_info.race_num and race_result.year=race_info.year\
    #                where race_result. year={} and is_race_no_flying=1 and is_race_times_record_valid=1 order by race_num, pitout_lane limit {};'.format(year, data_num*6))

    race_result_thisyear_ordered = session.execute('select * from (race_result inner join race_info on\
                    race_result.race_num = race_info.race_num and race_result.year = race_info.year) as\
                    TMP1 inner join race_odds on TMP1.race_num = race_odds.race_num and TMP1.year = race_odds.year\
                    where race_result.year={} and is_race_no_flying=1 and is_race_times_record_valid=1\
                    order by race_num, pitout_lane limit {}'.format(year, data_num))

    input_feature_list = []
    target_list = []
    race_odds_list = []
    feature_vec = []
    target_vec = []
    target_vec_part = [0 for i in range(6)]

    # create training data
    print('start')
    for idx, race_data in enumerate(race_result_thisyear_ordered):
        #print(idx)
        #race_info = race_info_list17.filter(RaceInfo.race_num==race_data.race_num).first()
        #race_info = session.execute('select * from race_info where race_num={} and year={};'.format(race_data.race_num, year)).first()
        ri = racer_info_list_last_year.filter(RacerInfo.racer_id==race_data.racer_id).first()
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
            if len(feature_vec) == 96:
                input_feature_list.append(feature_vec)
                target_list.append(target_vec)
                race_odds_info = RaceOddsInfo(race_data.rank1_lane, race_data.rank2_lane, race_data.rank3_lane,
                    race_data.tanshou, race_data.fukushou1, race_data.fukushou2,
                    race_data.nirentan, race_data.nirenfuku, race_data.kakurenfuku1_2,
                    race_data.kakurenfuku1_3, race_data.kakurenfuku2_3, race_data.sanrentan,
                    race_data.sanrenfuku)
                race_odds_list.append(race_odds_info)
            feature_vec = []
            target_vec = []
    return input_feature_list, target_list, race_odds_list


def load_odds(year, race_num):
    # for training
    race_odd_data = session.query(RaceOdds).filter(RaceOdds.year==year, RaceOdds.race_num==race_num).first()
    return race_odd_data

def load_test_data(year=2018, data_num=1000000000):

    res_test_features = session.query(
            RaceResult.race_num.label("race_num"),
            RaceInfo.is_race_no_flying.label("valid"),
            cast(RacerInfo.racer_rank_int, Float).label("racer_rank_int"),
            cast(RaceResult.rank, Float).label("result_rank"),
            cast(RacerInfo.this_period_capability_index, Float).label("racer_capability_index"),
            case([(RaceResult.pitout_lane == 1, cast(RacerInfo.first_course_first_arrive, Float) / cast(RacerInfo.first_course_entry_time, Float)),
            (RaceResult.pitout_lane == 2, cast(RacerInfo.second_course_first_arrive, Float) / cast(RacerInfo.second_course_entry_time, Float)),
            (RaceResult.pitout_lane == 3, cast(RacerInfo.third_course_first_arrive, Float) / cast(RacerInfo.third_course_entry_time, Float)),
            (RaceResult.pitout_lane == 4, cast(RacerInfo.fourth_course_first_arrive, Float) / cast(RacerInfo.fourth_course_entry_time, Float)),
            (RaceResult.pitout_lane == 5, cast(RacerInfo.fifth_course_first_arrive, Float) / cast(RacerInfo.fifth_course_entry_time, Float)),
            (RaceResult.pitout_lane == 6, cast(RacerInfo.sixth_course_first_arrive, Float) / cast(RacerInfo.sixth_course_entry_time, Float)),]).label("win_rate"),
            case([(RaceResult.pitout_lane == 1, RacerInfo.first_course_double_win_rate),
            (RaceResult.pitout_lane == 2, RacerInfo.second_course_double_win_rate),
            (RaceResult.pitout_lane == 3, RacerInfo.third_course_double_win_rate),
            (RaceResult.pitout_lane == 4, RacerInfo.fourth_course_double_win_rate),
            (RaceResult.pitout_lane == 5, RacerInfo.fifth_course_double_win_rate),
            (RaceResult.pitout_lane == 6, RacerInfo.sixth_course_double_win_rate)]).label("double_win_rate"),
            RaceOdds.rank1_lane.label("rank1_lane"),
            RaceOdds.rank2_lane.label("rank2_lane"),
            RaceOdds.rank3_lane.label("rank3_lane"),
            RaceOdds.tanshou.label("tanshou"),
            RaceOdds.fukushou1.label("fukushou1"),
            RaceOdds.fukushou2.label("fukushou2"),
            RaceOdds.nirentan.label("nirentan"),
            RaceOdds.nirenfuku.label("nirenfuku"),
            RaceOdds.sanrentan.label("sanrentan"),
            RaceOdds.sanrenfuku.label("sanrenfuku")).join(
                RacerInfo, RacerInfo.racer_id == RaceResult.racer_id).join(
                    RaceInfo, RaceInfo.race_num == RaceResult.race_num).join(
                    RaceOdds, RaceInfo.race_num == RaceOdds.race_num).filter(
                    RaceInfo.is_race_no_flying == 1,
                    RaceInfo.year == year,
                    RaceResult.year == year,
                    RaceOdds.year == year,
                    RacerInfo.year == year-1,
                    RacerInfo.period == 1
                ).order_by(RaceResult.race_num.asc(), RaceResult.pitout_lane.asc()).all()

    race_numbers = []
    test_input_features = []
    test_input_features_part = []
    test_target_labels = []
    test_target_labels_part = []
    odds_sanrentan_list = []
    odds_nirentan_list = []
    odds_tanshou_list = []
    odds_rank_top3_list = []

    for idx, r in enumerate(res_test_features):
        rank_vec = [0,0,0,0,0,0]
        if (idx)%6 == 0:
            test_input_features_part = []
            test_target_labels_part = []

            rank_existing_list = [False for i in range(6)]
            RANK1 = False
            RANK2 = False
            RANK3 = False
            RANK4 = False
            RANK5 = False
            RANK6 = False

        test_input_features_part += [r.racer_rank_int, r.racer_capability_index, r.win_rate, r.double_win_rate]
        rank_vec[int(r.result_rank)-1] = 1
        test_target_labels_part += rank_vec

        rank_existing_list[int(r.result_rank)-1] = True

        if idx%6 == 5:
            if True in pd.isnull(test_input_features_part):
                continue
            if False in rank_existing_list:
                continue
            race_numbers.append(r.race_num)
            odds_rank_top3_list.append([r.rank1_lane, r.rank2_lane, r.rank3_lane])
            odds_sanrentan_list.append(r.sanrentan)
            odds_nirentan_list.append(r.nirentan)
            test_input_features.append(test_input_features_part)
            test_target_labels.append(test_target_labels_part)

    test_input_features = np.array(test_input_features)
    test_target_labels = np.array(test_target_labels)
    odds_sanrentan = np.array(odds_sanrentan_list)
    odds_nirentan = np.array(odds_nirentan_list)
    odds_tanshou = np.array(odds_tanshou_list)
    odds_rank_top3 = np.array(odds_rank_top3_list)

    odds_dir = {"sanrentan": odds_sanrentan, "nirentan": odds_nirentan, "tanshou": odds_tanshou}

    return race_numbers, test_input_features, test_target_labels, odds_rank_top3, odds_dir

def load_train_data(year=2017, data_num=1000000000):
    session.rollback()

    res = session.query(
        RaceResult.race_num.label("race_num"),
        RaceInfo.is_race_no_flying.label("valid"),
        cast(RacerInfo.racer_rank_int, Float).label("racer_rank_int"),
        cast(RaceResult.rank, Float).label("result_rank"),
        cast(RacerInfo.this_period_capability_index, Float).label("racer_capability_index"),
        case([(RaceResult.pitout_lane == 1, cast(RacerInfo.first_course_first_arrive, Float) / cast(RacerInfo.first_course_entry_time, Float)),
        (RaceResult.pitout_lane == 2, cast(RacerInfo.second_course_first_arrive, Float) / cast(RacerInfo.second_course_entry_time, Float)),
        (RaceResult.pitout_lane == 3, cast(RacerInfo.third_course_first_arrive, Float) / cast(RacerInfo.third_course_entry_time, Float)),
        (RaceResult.pitout_lane == 4, cast(RacerInfo.fourth_course_first_arrive, Float) / cast(RacerInfo.fourth_course_entry_time, Float)),
        (RaceResult.pitout_lane == 5, cast(RacerInfo.fifth_course_first_arrive, Float) / cast(RacerInfo.fifth_course_entry_time, Float)),
        (RaceResult.pitout_lane == 6, cast(RacerInfo.sixth_course_first_arrive, Float) / cast(RacerInfo.sixth_course_entry_time, Float)),]).label("win_rate"),
        case([(RaceResult.pitout_lane == 1, RacerInfo.first_course_double_win_rate),
        (RaceResult.pitout_lane == 2, RacerInfo.second_course_double_win_rate),
        (RaceResult.pitout_lane == 3, RacerInfo.third_course_double_win_rate),
        (RaceResult.pitout_lane == 4, RacerInfo.fourth_course_double_win_rate),
        (RaceResult.pitout_lane == 5, RacerInfo.fifth_course_double_win_rate),
        (RaceResult.pitout_lane == 6, RacerInfo.sixth_course_double_win_rate)]).label("double_win_rate")).join(
            RacerInfo, RacerInfo.racer_id == RaceResult.racer_id).join(
            RaceInfo, RaceInfo.race_num == RaceResult.race_num
            ).filter(
                RaceInfo.is_race_no_flying == 1,
                RaceInfo.year == year,
                RaceResult.year == year,
                RacerInfo.year == year-1,
                RacerInfo.period == 2
            ).order_by(RaceResult.race_num.asc(), RaceResult.pitout_lane.asc()).all()

    input_features = []
    input_features_part = []
    target_labels = []
    target_labels_part = []


    for idx, r in enumerate(res):
        rank_vec = [0,0,0,0,0,0]
        if (idx)%6 == 0:
            input_features_part = []
            target_labels_part = []

            RANK1 = False
            RANK2 = False
            RANK3 = False
            RANK4 = False
            RANK5 = False
            RANK6 = False

        input_features_part += [r.racer_rank_int, r.racer_capability_index, r.win_rate, r.double_win_rate]
        rank_vec[int(r.result_rank)-1] = 1
        target_labels_part += rank_vec

        if r.result_rank==1:
            RANK1 = True
        elif r.result_rank==2:
            RANK2 = True
        elif r.result_rank==3:
            RANK3 = True
        elif r.result_rank==4:
            RANK4 = True
        elif r.result_rank==5:
            RANK5 = True
        elif r.result_rank==6:
            RANK6 = True

        if idx%6 == 5:
            if True in pd.isnull(input_features_part):
                continue
            if not(RANK1 and RANK2 and RANK3 and RANK4 and RANK5 and RANK6):
                continue

            input_features.append(input_features_part)
            target_labels.append(target_labels_part)

    input_features = np.array(input_features)
    target_labels = np.array(target_labels)

    return input_features, target_labels