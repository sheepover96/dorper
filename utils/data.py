import numpy as np
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import case, cast, func, Float

from models import RaceResult, RacerInfo, RaceOdds, RaceInfo, RaceResultGrouped
from .setting import session
from collections import namedtuple

rank_dic = {1:150, 2:100, 3:50, 4:0}
RaceOddsInfo = namedtuple('RaceOddsInfo', ['rank1_lane', 'rank2_lane', 'rank3_lane',
                                           'tanshou', 'fukushou1', 'fukushou2', 'nirentan',
                                           'nirenfuku', 'kakurenfuku1_2', 'kakurenfuku1_3',
                                           'kakurenfuku2_3', 'sanrentan', 'sanrenfuku'])

def load_data(year, data_num=1000000000):
    race_result_list_this_year = session.query(RaceResult).filter(RaceResult.year==year)
    race_info_list_this_year = session.query(RaceInfo).filter(RaceInfo.year==year)
    race_odds_list_this_year = session.query(RaceOdds).filter(RaceOdds.year==year)
    racer_info_list_last_year = session.query(RacerInfo).filter(RacerInfo.year==(year-1))
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

    # create data
    for idx, race_data in enumerate(race_result_thisyear_ordered):
        ri = racer_info_list_last_year.filter(RacerInfo.racer_id==race_data.racer_id).first()
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


def load_data_all(target_race_num_list, year, data_num=1000000000):
    res = session.query(
        #feature作成用
        cast(RacerInfo.racer_rank_int, Float).label("racer_rank_int"),
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
        #label作成用
        RaceResultGrouped.race_num.label("race_num"),
        RaceResultGrouped.lane1_result_rank.label("lane1_rank"),
        RaceResultGrouped.lane2_result_rank.label("lane2_rank"),
        RaceResultGrouped.lane3_result_rank.label("lane3_rank"),
        RaceResultGrouped.lane4_result_rank.label("lane4_rank"),
        RaceResultGrouped.lane5_result_rank.label("lane5_rank"),
        RaceResultGrouped.lane6_result_rank.label("lane6_rank"),
        #odds for evaluation
        RaceOdds.race_num.label("race_num"),
        RaceOdds.rank1_lane.label("rank1_lane"),
        RaceOdds.rank2_lane.label("rank2_lane"),
        RaceOdds.rank3_lane.label("rank3_lane"),
        RaceOdds.tanshou.label("tanshou"),
        RaceOdds.fukushou1.label("fukushou1"),
        RaceOdds.fukushou2.label("fukushou2"),
        RaceOdds.nirentan.label("nirentan"),
        RaceOdds.nirenfuku.label("nirenfuku"),
        RaceOdds.sanrentan.label("sanrentan"),
        RaceOdds.sanrenfuku.label("sanrenfuku")
    ).join(
        RaceResult, RacerInfo.racer_id == RaceResult.racer_id,
        RaceResultGrouped.race_num == RaceResult.race_num,
        RaceOdds.race_num == RaceResult.race_num,
        ).filter(
        RaceResult.year == year,
        RacerInfo.year == year-1,
        RacerInfo.period == 2
    ).order_by(RaceResult.race_num.asc(), RaceResult.pitout_lane.asc()).all()

    return res


def load_target_labels(race_num_list, year=2017):

    res = session.query(
        RaceResultGrouped.race_num.label("race_num"),
        RaceResultGrouped.lane1_result_rank.label("lane1_rank"),
        RaceResultGrouped.lane2_result_rank.label("lane2_rank"),
        RaceResultGrouped.lane3_result_rank.label("lane3_rank"),
        RaceResultGrouped.lane4_result_rank.label("lane4_rank"),
        RaceResultGrouped.lane5_result_rank.label("lane5_rank"),
        RaceResultGrouped.lane6_result_rank.label("lane6_rank")
    ).join(RaceInfo, RaceResultGrouped.race_num==RaceInfo.race_num).filter(
        RaceResultGrouped.race_num.in_(race_num_list),
        RaceResultGrouped.year == year,
        RaceInfo.year == year,
        RaceInfo.is_race_no_flying == 1).order_by(RaceResultGrouped.race_num.asc()).all()

    use_race_num_list = []
    target_vec_list = []
    print('ar',len(res))

    for r in res:
        rank_set = (r.lane1_rank, r.lane2_rank, r.lane3_rank, r.lane4_rank, r.lane5_rank, r.lane6_rank)
        if 100 in rank_set or None in rank_set:
            continue
        if len(set([r.lane1_rank, r.lane2_rank, r.lane3_rank, r.lane4_rank, r.lane5_rank, r.lane6_rank])) != 6:
            continue

        use_race_num_list.append(r.race_num)

        lane1_vec = [1 if i == r.lane1_rank-1 else 0 for i in range(6)]
        lane2_vec = [1 if i == r.lane2_rank-1 else 0 for i in range(6)]
        lane3_vec = [1 if i == r.lane3_rank-1 else 0 for i in range(6)]
        lane4_vec = [1 if i == r.lane4_rank-1 else 0 for i in range(6)]
        lane5_vec = [1 if i == r.lane5_rank-1 else 0 for i in range(6)]
        lane6_vec = [1 if i == r.lane6_rank-1 else 0 for i in range(6)]

        rank_vec = lane1_vec + lane2_vec + lane3_vec + lane4_vec + lane5_vec + lane6_vec
        target_vec_list.append(rank_vec)

    return target_vec_list

def load_features(use_race_num_list, year=2017):
    session.rollback()

    res = session.query(
        cast(RacerInfo.racer_rank_int, Float).label("racer_rank_int"),
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
        (RaceResult.pitout_lane == 6, RacerInfo.sixth_course_double_win_rate)]).label("double_win_rate")
    ).join(RaceResult, RacerInfo.racer_id == RaceResult.racer_id).filter(
                RaceResult.year == year,
                RacerInfo.year == year-1,
                RacerInfo.period == 2,
                RaceResult.race_num.in_(use_race_num_list)
            ).order_by(RaceResult.race_num.asc(), RaceResult.pitout_lane.asc()).all()

    input_features = []
    input_features_part = []

    print(len(res))
    for idx, r in enumerate(res):
        if (idx)%6 == 0:
            input_features_part = []

        input_features_part += [r.racer_rank_int, r.racer_capability_index, r.win_rate, r.double_win_rate]

        if idx%6 == 5:
            input_features.append(input_features_part)

    return input_features

def load_odds(race_num_list, year=2018):
    session.rollback()

    res_odds = session.query(
            RaceOdds.race_num.label("race_num"),
            RaceOdds.rank1_lane.label("rank1_lane"),
            RaceOdds.rank2_lane.label("rank2_lane"),
            RaceOdds.rank3_lane.label("rank3_lane"),
            RaceOdds.tanshou.label("tanshou"),
            RaceOdds.fukushou1.label("fukushou1"),
            RaceOdds.fukushou2.label("fukushou2"),
            RaceOdds.nirentan.label("nirentan"),
            RaceOdds.nirenfuku.label("nirenfuku"),
            RaceOdds.sanrentan.label("sanrentan"),
            RaceOdds.sanrenfuku.label("sanrenfuku")).filter(
                RaceOdds.race_num.in_(race_num_list),
                RaceOdds.year == year
                ).order_by(RaceOdds.race_num.asc()).all()

    return res_odds

def load_training_data(race_num_list):
    input_features = load_features(race_num_list, year=2017)
    input_features = np.array(input_features)
    target_labels = load_target_labels(race_num_list, year=2017)
    target_labels = np.array(target_labels)

    return input_features, target_labels

def load_test_data(race_num_list, year=2018):
    input_features = load_features(race_num_list, year=year)
    input_features = np.array(input_features)
    target_labels = load_target_labels(race_num_list, year=year)
    target_labels = np.array(target_labels)
    odds = load_odds(race_num_list, year=year)

    return race_num_list, input_features, target_labels, odds

def get_target_race_nums(year=2017):
    res = session.query(
        RaceResultGrouped.race_num.label("race_num"),
        RaceResultGrouped.lane1_result_rank.label("lane1_rank"),
        RaceResultGrouped.lane2_result_rank.label("lane2_rank"),
        RaceResultGrouped.lane3_result_rank.label("lane3_rank"),
        RaceResultGrouped.lane4_result_rank.label("lane4_rank"),
        RaceResultGrouped.lane5_result_rank.label("lane5_rank"),
        RaceResultGrouped.lane6_result_rank.label("lane6_rank")
    ).join(RaceInfo, RaceResultGrouped.race_num==RaceInfo.race_num).filter(
        RaceResultGrouped.year == year,
        RaceInfo.year == year,
        RaceInfo.is_race_no_flying == 1).all()

    use_race_num_list = []
    target_vec_list = []

    for r in res:
        rank_set = (r.lane1_rank, r.lane2_rank, r.lane3_rank, r.lane4_rank, r.lane5_rank, r.lane6_rank)
        if 100 in rank_set or None in rank_set:
            continue
        if len(set([r.lane1_rank, r.lane2_rank, r.lane3_rank, r.lane4_rank, r.lane5_rank, r.lane6_rank])) != 6:
            continue

        use_race_num_list.append(r.race_num)

    return use_race_num_list

def get_feature_race_nums(year=2017):
    subquery = session.query(
        RaceResult.race_num.label("race_num"),
        func.count(RaceResult.race_num).label("count")).join(
            RacerInfo, RacerInfo.racer_id == RaceResult.racer_id
        ).filter(
            RaceResult.year == year,
            RacerInfo.year == year-1,
            RacerInfo.period == 2
        ).group_by(RaceResult.race_num).subquery()

    res = session.query(
        subquery.c.race_num.label("race_num")
        ).filter(
            subquery.c.count == 6
        ).all()

    use_race_num_list = []

    for r in res:
        use_race_num_list.append(r.race_num)

    return use_race_num_list

def get_odds_race_nums(year=2018):
    res = session.query(
        RaceOdds.race_num.label("race_num")
    ).filter(
        RaceOdds.year == year).all()

    race_num_list = [r.race_num for r in res]

    return race_num_list