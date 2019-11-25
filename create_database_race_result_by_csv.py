import sqlalchemy
from sqlalchemy import create_engine, distinct, or_
from sqlalchemy.orm import sessionmaker
import pandas as pd

import re, datetime
from utils.setting import session
from models import Base, RaceResult, RaceInfo

def main():
    engine = create_engine('sqlite:///race_database_new.sqlite3')
    Base.metadata.create_all(engine)
    #race_num_list = session.query(RaceResult).distinct(RaceResult.race_num).all()
    race_result_list = []
    race_result = pd.read_csv('dataset/whole_race_result.csv', encoding="SHIFT_JIS", dtype={'year':'int'})
    for idx, data_row in race_result.iterrows():
        year = int(data_row['year'])
        race_num = int(data_row['race_num'])
        rank_str = str(data_row['rank'])
        rank = 0
        if rank_str == "S0":
            rank=101
        elif rank_str == "S1":
            rank=102
        elif rank_str == "S2":
            rank=103
        elif rank_str == "F":
            rank=104
        elif rank_str == "L0":
            rank=105
        elif rank_str == "L1":
            rank=106
        elif rank_str == "K0":
            rank=107
        elif rank_str == "K1":
            rank=108
        else:
            rank=int(rank_str)
        pitout_lane = int(data_row['pitout_lane'])
        racer_id = int(data_row['racer_ID'])
        racer_name = data_row['racer_name']

        motor = int(data_row['motor'])
        boat = int(data_row['boat'])
        tenji_str = str(data_row["tenji"]).replace(" ", "")
        if bool(re.compile("^\d+\.?\d*\Z").match(tenji_str)):
            tenji = float(tenji_str)
        else:
            tenji = None
        shinnyu_str = str(data_row["shinnyu"]).replace(" ", "")
        if bool(re.compile("^\d+\.?\d*\Z").match(shinnyu_str)):
            shinnyu = int(shinnyu_str)
        else:
            siunnyu = None
        start_timing_str = str(data_row["start_timing"]).strip()
        if bool(re.compile("^\d+\.?\d*\Z").match(start_timing_str)):
            start_timing = float(start_timing_str)
        else:
            start_timing = None

        race_time = data_row["race_time"]
        print(idx, race_time)
        if(race_time=="." or race_time[0]=="K"):
            race_time = None
        else:
            m,s,ms = race_time.split(".")
            race_time = float(m)*60.0 + float(s) + float(ms)/10

        date_str = str(int(data_row["date"])).lstrip()
        date_str = "0"*(6-len(date_str)) + date_str
        if int(date_str[0]) >= 8:
            date = datetime.date(int('19' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))
        else:
            date = datetime.date(int('20' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))

        race_result_list.append(RaceResult(race_num=race_num, rank=rank, rank_str=rank_str, pitout_lane=pitout_lane,
            racer_id=racer_id, racer_name=racer_name, motor=motor, boat=boat, tenji=tenji,
            shinnyu=shinnyu, start_timing=start_timing, race_time=race_time, date=date, year=year))
    session.add_all(race_result_list)
    session.commit()


if __name__ == '__main__':
    main()
