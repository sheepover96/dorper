from sqlalchemy.sql import text

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