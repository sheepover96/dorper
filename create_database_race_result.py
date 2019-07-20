import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import datetime
import glob, re

from models import Base, RaceResult

def get_race_result_list(data_path):
    df = pd.read_csv(data_path, encoding="SHIFT_JIS")
    df2 = pd.read_csv('race_valid_2018.csv')
    year = 2018
    data_pk = 0
    race_result_list = []
    for data_row in df.iterrows():
        race_id = int(data_row[1][0])
        #is_valid = df2[df2['Race_num'] == race_id]
        #try:
        rank = str(data_row[1][1]).lstrip()
        if rank == "S0":
            rank=101
        elif rank == "S1":
            rank=102
        elif rank == "S2":
            rank=103
        elif rank == "F":
            rank=104
        elif rank == "L0":
            rank=105
        elif rank == "L1":
            rank=106
        elif rank == "K0":
            rank=107
        elif rank == "K1":
            rank=108
        else:
            rank=int(rank)
        pitout_lane = int(data_row[1][2])
        racer_id = int(data_row[1][3])
        racer_name = data_row[1][4].strip()
        motor = int(data_row[1][5])
        boat = int(data_row[1][6])
        tenji = float(data_row[1][7])
        shinnyu = int(data_row[1][8])
        start_timing = data_row[1][9].strip()
        if bool(re.compile("^\d+\.?\d*\Z").match(start_timing)):
            start_timing = float(start_timing)
        else:
            start_timing = -float(start_timing[1:])
        race_time = data_row[1][10]
        race_time_tmp = race_time[:-2].strip()
        if race_time.isdigit():
            m,s,ms = data_row["Race_Time"].split(".")
            race_time = float(m)*60.0 + float(s) + float(ms)/10
        else:
            race_time = None
        date_str = str(int(data_row[1][11]))
        print(date_str)
        if int(date_str[0]) >= 8:
            date = datetime.date(int('20' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))
        else:
            date = datetime.date(int('19' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))

        race_result_list.append(RaceResult(id=data_pk, race_num=race_id, rank=rank, pitout_lane=pitout_lane,
            racer_id=racer_id, racer_name=racer_name, motor=motor, boat=boat, tenji=tenji,
            shinnyu=shinnyu, start_timing=start_timing, race_time=race_time, date=date, year=year))
        data_pk += 1
        #except ValueError as e:
        #        print(e)

    return race_result_list

def main():
    engine = create_engine('sqlite:///race_result.sqlite3')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    files = glob.glob('dataset/kyousou_csv_data/*')
    files.sort()
    for target_file in files[:1]:
        race_result_list = get_race_result_list(target_file)
        session.add_all(race_result_list)
    session.commit()

if __name__ == '__main__':
    main()
