import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import datetime
import glob

from models import Base, RacerInfo

def get_racer_info_list(path):
    #df = pd.read_csv('dataset/fan1504.csv', encoding="SHIFT_JIS")
    df = pd.read_csv(path, encoding="SHIFT_JIS")
    racer_info_list = []
    for idx, data_row in enumerate(df.iterrows()):
        try:
            racer_id = int(data_row[1][0])
            racer_name_kanji = data_row[1][1]
            racer_name_kana = data_row[1][2].rstrip()
            branch_prefecture = data_row[1][3]
            racer_rank = data_row[1][4].lstrip()
            
            if racer_rank == "A1":
                racer_rank_int = 1
            elif racer_rank == "A2":
                racer_rank_int = 2
            elif racer_rank == "B1":
                racer_rank_int = 3
            else:
                racer_rank_int = 4
            
            name_of_year = data_row[1][5]
            base_year = 0
            if name_of_year == 'S':
                base_year = 1926
            elif name_of_year == 'H':
                base_year = 1989
            birth_number = int(data_row[1][6])
            tmp_year = int(birth_number / 10000)
            birth_month = int((birth_number - tmp_year*10000) / 100)
            birth_day = birth_number - tmp_year * 10000 - birth_month * 100
            year_adjust = 0
            if birth_month < 4:
                year_adjust = -1
            birth_year = base_year + tmp_year + year_adjust
            birth_date = datetime.date(birth_year, birth_month, birth_day)
            racer_sex = int(data_row[1][7])
            racer_age = int(data_row[1][8])
            racer_height = int(data_row[1][9])
            racer_weight = int(data_row[1][10])
            racer_blood_type = data_row[1][11].rstrip()
            racer_win_rate = float(data_row[1][12]) / 1000
            racer_double_win_rate = float(data_row[1][13]) / 1000
            racer_first_arrival_times = int(data_row[1][14])
            racer_second_arrival_times = int(data_row[1][15])
            racer_start_times = int(data_row[1][16])
            winner_race_start_times = int(data_row[1][17])
            num_of_win = int(data_row[1][18])
            average_start_timing = float(data_row[1][19]) / 100

            first_course_entry_time = int(data_row[1][20])
            first_course_double_win_rate = float(data_row[1][21]) / 1000
            first_course_average_start_timing = int(data_row[1][22])
            first_course_average_start_rank = float(data_row[1][23])/ 100

            second_course_entry_time = int(data_row[1][24])
            second_course_double_win_rate = float(data_row[1][25]) / 1000
            second_course_average_start_timing = int(data_row[1][26])
            second_course_average_start_rank = float(data_row[1][27]) / 100

            third_course_entry_time = int(data_row[1][28])
            third_course_double_win_rate = float(data_row[1][29]) / 1000
            third_course_average_start_timing = int(data_row[1][30])
            third_course_average_start_rank = float(data_row[1][31]) / 100

            fourth_course_entry_time = int(data_row[1][32])
            fourth_course_double_win_rate = float(data_row[1][33]) / 1000
            fourth_course_average_start_timing = int(data_row[1][34])
            fourth_course_average_start_rank = float(data_row[1][35]) / 100

            fifth_course_entry_time = int(data_row[1][36])
            fifth_course_double_win_rate = float(data_row[1][37]) / 1000
            fifth_course_average_start_timing = int(data_row[1][38])
            fifth_course_average_start_rank = float(data_row[1][39]) / 100

            sixth_course_entry_time = int(data_row[1][40])
            sixth_course_double_win_rate = float(data_row[1][41]) / 1000
            sixth_course_average_start_timing = int(data_row[1][42])
            sixth_course_average_start_rank = float(data_row[1][43]) / 100

            previous_period_rank = data_row[1][44].lstrip()
            
            if previous_period_rank == "A1":
                previous_period_rank_int = 1
            elif previous_period_rank == "A2":
                previous_period_rank_int = 2
            elif previous_period_rank == "B1":
                previous_period_rank_int = 3
            else:
                previous_period_rank_int = 4
            
            
            previous_second_period_rank = data_row[1][45].lstrip()
            
            if previous_second_period_rank == "A1":
                previous_second_period_rank_int = 1
            elif previous_second_period_rank == "A2":
                previous_second_period_rank_int = 2
            elif previous_second_period_rank == "B1":
                previous_second_period_rank_int = 3
            else:
                previous_second_period_rank_int = 4
            
            
            previous_third_period_rank = data_row[1][46].lstrip()
            
            if previous_third_period_rank == "A1":
                previous_third_period_rank_int = 1
            elif previous_third_period_rank == "A2":
                previous_third_period_rank_int = 2
            elif previous_third_period_rank == "B1":
                previous_third_period_rank_int = 3
            else:
                previous_third_period_rank_int = 4
                

            previous_period_capability_index = float(data_row[1][47]) / 100
            this_period_capability_index = float(data_row[1][48]) / 100

            year = int(data_row[1][49])
            period = int(data_row[1][50])

            calculation_period_begin_datetime = datetime.datetime.strptime(str(int(data_row[1][51])), '%Y%m%d')
            calculation_period_begin = datetime.date(calculation_period_begin_datetime.year, calculation_period_begin_datetime.month, calculation_period_begin_datetime.day)
            calculation_period_end_datetime = datetime.datetime.strptime(str(int(data_row[1][52])), '%Y%m%d')
            calculation_period_end = datetime.date(calculation_period_end_datetime.year, calculation_period_end_datetime.month, calculation_period_end_datetime.day)

            training_period = int(data_row[1][53])

            first_course_first_arrive =     int(data_row[1][54])
            first_course_second_arrive =    int(data_row[1][55])
            first_course_third_arrive =     int(data_row[1][56])
            first_course_fourth_arrive =    int(data_row[1][57])
            first_course_fifth_arrive =     int(data_row[1][58])
            first_course_sixth_arrive =     int(data_row[1][59])
            first_course_f_times =          int(data_row[1][60])
            first_course_l0_times =         int(data_row[1][61])
            first_course_l1_times =         int(data_row[1][62])
            first_course_k0_times =         int(data_row[1][63])
            first_course_k1_times =         int(data_row[1][64])
            first_course_s0_times =         int(data_row[1][65])
            first_course_s1_times =         int(data_row[1][66])
            first_course_s2_times =         int(data_row[1][67])

            second_course_first_arrive =     int(data_row[1][68])
            second_course_second_arrive =    int(data_row[1][69])
            second_course_third_arrive =     int(data_row[1][70])
            second_course_fourth_arrive =    int(data_row[1][71])
            second_course_fifth_arrive =     int(data_row[1][72])
            second_course_sixth_arrive =     int(data_row[1][73])
            second_course_f_times =          int(data_row[1][74])
            second_course_l0_times =         int(data_row[1][75])
            second_course_l1_times =         int(data_row[1][76])
            second_course_k0_times =         int(data_row[1][77])
            second_course_k1_times =         int(data_row[1][78])
            second_course_s0_times =         int(data_row[1][79])
            second_course_s1_times =         int(data_row[1][80])
            second_course_s2_times =         int(data_row[1][81])

            third_course_first_arrive =     int(data_row[1][82])
            third_course_second_arrive =    int(data_row[1][83])
            third_course_third_arrive =     int(data_row[1][84])
            third_course_fourth_arrive =    int(data_row[1][85])
            third_course_fifth_arrive =     int(data_row[1][86])
            third_course_sixth_arrive =     int(data_row[1][87])
            third_course_f_times =          int(data_row[1][88])
            third_course_l0_times =         int(data_row[1][89])
            third_course_l1_times =         int(data_row[1][90])
            third_course_k0_times =         int(data_row[1][91])
            third_course_k1_times =         int(data_row[1][92])
            third_course_s0_times =         int(data_row[1][93])
            third_course_s1_times =         int(data_row[1][94])
            third_course_s2_times =         int(data_row[1][95])

            fourth_course_first_arrive =     int(data_row[1][96])
            fourth_course_second_arrive =    int(data_row[1][97])
            fourth_course_third_arrive =     int(data_row[1][98])
            fourth_course_fourth_arrive =    int(data_row[1][99])
            fourth_course_fifth_arrive =     int(data_row[1][100])
            fourth_course_sixth_arrive =     int(data_row[1][101])
            fourth_course_f_times =          int(data_row[1][102])
            fourth_course_l0_times =         int(data_row[1][103])
            fourth_course_l1_times =         int(data_row[1][104])
            fourth_course_k0_times =         int(data_row[1][105])
            fourth_course_k1_times =         int(data_row[1][106])
            fourth_course_s0_times =         int(data_row[1][107])
            fourth_course_s1_times =         int(data_row[1][108])
            fourth_course_s2_times =         int(data_row[1][109])

            fifth_course_first_arrive =     int(data_row[1][110])
            fifth_course_second_arrive =    int(data_row[1][111])
            fifth_course_third_arrive =     int(data_row[1][112])
            fifth_course_fourth_arrive =    int(data_row[1][113])
            fifth_course_fifth_arrive =     int(data_row[1][114])
            fifth_course_sixth_arrive =     int(data_row[1][115])
            fifth_course_f_times =          int(data_row[1][116])
            fifth_course_l0_times =         int(data_row[1][117])
            fifth_course_l1_times =         int(data_row[1][118])
            fifth_course_k0_times =         int(data_row[1][119])
            fifth_course_k1_times =         int(data_row[1][120])
            fifth_course_s0_times =         int(data_row[1][121])
            fifth_course_s1_times =         int(data_row[1][122])
            fifth_course_s2_times =         int(data_row[1][123])

            sixth_course_first_arrive =     int(data_row[1][124])
            sixth_course_second_arrive =    int(data_row[1][125])
            sixth_course_third_arrive =     int(data_row[1][126])
            sixth_course_fourth_arrive =    int(data_row[1][127])
            sixth_course_fifth_arrive =     int(data_row[1][128])
            sixth_course_sixth_arrive =     int(data_row[1][129])
            sixth_course_f_times =          int(data_row[1][130])
            sixth_course_l0_times =         int(data_row[1][131])
            sixth_course_l1_times =         int(data_row[1][132])
            sixth_course_k0_times =         int(data_row[1][133])
            sixth_course_k1_times =         int(data_row[1][134])
            sixth_course_s0_times =         int(data_row[1][135])
            sixth_course_s1_times =         int(data_row[1][136])
            sixth_course_s2_times =         int(data_row[1][137])

            no_course_l0_times = int(data_row[1][138])
            no_course_l1_times = int(data_row[1][139])
            no_course_k0_times = int(data_row[1][140])
            no_course_k1_times = int(data_row[1][141])

            birth_place = data_row[1][142]
            new_racer_info = RacerInfo(
                racer_id=racer_id,
                racer_name_kanji = racer_name_kanji,
                racer_name_kana = racer_name_kana,
                branch_prefecture = branch_prefecture,
                racer_rank = racer_rank,
                racer_rank_int = racer_rank_int,
                birth_date = birth_date,
                racer_sex = racer_sex,
                racer_age = racer_age,
                racer_height = racer_height,
                racer_weight = racer_weight,
                racer_blood_type = racer_blood_type,
                racer_win_rate = racer_win_rate,
                racer_double_win_rate = racer_double_win_rate,
                racer_first_arrival_times = racer_first_arrival_times,
                racer_second_arrival_times = racer_second_arrival_times,
                racer_start_times = racer_start_times,
                winner_race_start_times = winner_race_start_times,
                number_of_win = num_of_win,
                average_start_timing = average_start_timing,
                first_course_entry_time = first_course_entry_time,
                first_course_double_win_rate = first_course_double_win_rate,
                first_course_average_start_timing = first_course_average_start_timing,
                first_course_average_start_rank = first_course_average_start_rank,
                second_course_entry_time = second_course_entry_time,
                second_course_double_win_rate = second_course_double_win_rate,
                second_course_average_start_timing = second_course_average_start_timing,
                second_course_average_start_rank = second_course_average_start_rank,
                third_course_entry_time = third_course_entry_time,
                third_course_double_win_rate = third_course_double_win_rate,
                third_course_average_start_timing = third_course_average_start_timing,
                third_course_average_start_rank = third_course_average_start_rank,
                fourth_course_entry_time = fourth_course_entry_time,
                fourth_course_double_win_rate = fourth_course_double_win_rate,
                fourth_course_average_start_timing = fourth_course_average_start_timing,
                fourth_course_average_start_rank = fourth_course_average_start_rank,
                fifth_course_entry_time = fifth_course_entry_time,
                fifth_course_double_win_rate = fifth_course_double_win_rate,
                fifth_course_average_start_timing = fifth_course_average_start_timing,
                fifth_course_average_start_rank = fifth_course_average_start_rank,
                sixth_course_entry_time = sixth_course_entry_time,
                sixth_course_double_win_rate = sixth_course_double_win_rate,
                sixth_course_average_start_timing = sixth_course_average_start_timing,
                sixth_course_average_start_rank = sixth_course_average_start_rank,
                previous_period_rank = previous_period_rank,
                previous_period_rank_int = previous_period_rank_int,                
                previous_second_period_rank = previous_second_period_rank,
                previous_second_period_rank_int = previous_second_period_rank_int,
                previous_third_period_rank = previous_third_period_rank,
                previous_third_period_rank_int = previous_third_period_rank_int,
                previous_period_capability_index = previous_period_capability_index,
                this_period_capability_index = this_period_capability_index,
                year = year,
                period = period,
                calculation_period_begin = calculation_period_begin,
                calculation_period_end = calculation_period_end,
                training_period = training_period,
                first_course_first_arrive =     first_course_first_arrive,
                first_course_second_arrive =    first_course_second_arrive,
                first_course_third_arrive =     first_course_third_arrive,
                first_course_fourth_arrive =    first_course_fourth_arrive,
                first_course_fifth_arrive =     first_course_fifth_arrive,
                first_course_sixth_arrive =     first_course_sixth_arrive,
                first_course_f_times =          first_course_f_times,
                first_course_l0_times =         first_course_l0_times,
                first_course_l1_times =         first_course_l1_times,
                first_course_k0_times =         first_course_k0_times,
                first_course_k1_times =         first_course_k1_times,
                first_course_s0_times =         first_course_s0_times,
                first_course_s1_times =         first_course_s1_times,
                first_course_s2_times =         first_course_s2_times,
                second_course_first_arrive =     second_course_first_arrive,
                second_course_second_arrive =    second_course_second_arrive,
                second_course_third_arrive =     second_course_third_arrive,
                second_course_fourth_arrive =    second_course_fourth_arrive,
                second_course_fifth_arrive =     second_course_fifth_arrive,
                second_course_sixth_arrive =     second_course_sixth_arrive,
                second_course_f_times =          second_course_f_times,
                second_course_l0_times =         second_course_l0_times,
                second_course_l1_times =         second_course_l1_times,
                second_course_k0_times =         second_course_k0_times,
                second_course_k1_times =         second_course_k1_times,
                second_course_s0_times =         second_course_s0_times,
                second_course_s1_times =         second_course_s1_times,
                second_course_s2_times =         second_course_s2_times,
                third_course_first_arrive =     third_course_first_arrive,
                third_course_second_arrive =    third_course_second_arrive,
                third_course_third_arrive =     third_course_third_arrive,
                third_course_fourth_arrive =    third_course_fourth_arrive,
                third_course_fifth_arrive =     third_course_fifth_arrive,
                third_course_sixth_arrive =     third_course_sixth_arrive,
                third_course_f_times =          third_course_f_times,
                third_course_l0_times =         third_course_l0_times,
                third_course_l1_times =         third_course_l1_times,
                third_course_k0_times =         third_course_k0_times,
                third_course_k1_times =         third_course_k1_times,
                third_course_s0_times =         third_course_s0_times,
                third_course_s1_times =         third_course_s1_times,
                third_course_s2_times =         third_course_s2_times,
                fourth_course_first_arrive =     fourth_course_first_arrive,
                fourth_course_second_arrive =    fourth_course_second_arrive,
                fourth_course_third_arrive =     fourth_course_third_arrive,
                fourth_course_fourth_arrive =    fourth_course_fourth_arrive,
                fourth_course_fifth_arrive =     fourth_course_fifth_arrive,
                fourth_course_sixth_arrive =     fourth_course_sixth_arrive,
                fourth_course_f_times =          fourth_course_f_times,
                fourth_course_l0_times =         fourth_course_l0_times,
                fourth_course_l1_times =         fourth_course_l1_times,
                fourth_course_k0_times =         fourth_course_k0_times,
                fourth_course_k1_times =         fourth_course_k1_times,
                fourth_course_s0_times =         fourth_course_s0_times,
                fourth_course_s1_times =         fourth_course_s1_times,
                fourth_course_s2_times =         fourth_course_s2_times,
                fifth_course_first_arrive =     fifth_course_first_arrive,
                fifth_course_second_arrive =    fifth_course_second_arrive,
                fifth_course_third_arrive =     fifth_course_third_arrive,
                fifth_course_fourth_arrive =    fifth_course_fourth_arrive,
                fifth_course_fifth_arrive =     fifth_course_fifth_arrive,
                fifth_course_sixth_arrive =     fifth_course_sixth_arrive,
                fifth_course_f_times =          fifth_course_f_times,
                fifth_course_l0_times =         fifth_course_l0_times,
                fifth_course_l1_times =         fifth_course_l1_times,
                fifth_course_k0_times =         fifth_course_k0_times,
                fifth_course_k1_times =         fifth_course_k1_times,
                fifth_course_s0_times =         fifth_course_s0_times,
                fifth_course_s1_times =         fifth_course_s1_times,
                fifth_course_s2_times =         fifth_course_s2_times,
                sixth_course_first_arrive =     sixth_course_first_arrive,
                sixth_course_second_arrive =    sixth_course_second_arrive,
                sixth_course_third_arrive =     sixth_course_third_arrive,
                sixth_course_fourth_arrive =    sixth_course_fourth_arrive,
                sixth_course_fifth_arrive =     sixth_course_fifth_arrive,
                sixth_course_sixth_arrive =     sixth_course_sixth_arrive,
                sixth_course_f_times =          sixth_course_f_times,
                sixth_course_l0_times =         sixth_course_l0_times,
                sixth_course_l1_times =         sixth_course_l1_times,
                sixth_course_k0_times =         sixth_course_k0_times,
                sixth_course_k1_times =         sixth_course_k1_times,
                sixth_course_s0_times =         sixth_course_s0_times,
                sixth_course_s1_times =         sixth_course_s1_times,
                sixth_course_s2_times =         sixth_course_s2_times,
                no_course_l0_times = no_course_l0_times,
                no_course_l1_times = no_course_l1_times,
                no_course_k0_times = no_course_k0_times,
                no_course_k1_times = no_course_k1_times,
                birth_place = birth_place
            )
            #print(birth_place)
            racer_info_list.append(new_racer_info)
        except ValueError as e:
            print(e)

    return racer_info_list

def main():
    engine = create_engine('sqlite:///race_database_new.sqlite3')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    files = glob.glob('dataset/senshu_csv_data/*')
    files.sort()
    for target_file in files:
        racer_info_list = get_racer_info_list(target_file)
        session.add_all(racer_info_list)
    session.commit()

if __name__ == '__main__':
    main()

