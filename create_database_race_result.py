import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import datetime
import glob, re, os

from models import Base, RaceResult

def get_race_result_list(path):
    df = pd.read_csv(path, encoding="SHIFT_JIS")
    #df = df[0:10]
    race_result_list = []
    for column_name, data_row in df.iterrows():
        try:
            race_id = int(data_row["Race_num"])
            rank = str(data_row["Rank"]).lstrip()
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
            pitout_lane = int(str(data_row["Cource"]).replace(" ", ""))
            racer_id = int(str(data_row["Racer_ID"]).replace(" ", ""))
            racer_name = data_row["Racer_Name"]
            motor = int(str(data_row["Motor"]).replace(" ", ""))
            boat = int(str(data_row["Boat"]).replace(" ", ""))
            tenji = str(data_row["Tenji"]).replace(" ", "")
            if bool(re.compile("^\d+\.?\d*\Z").match(tenji)):
                tenji = float(tenji)
            else:
                tenji = None
            shinnyu = str(data_row["Shinnyu"]).replace(" ", "")
            if bool(re.compile("^\d+\.?\d*\Z").match(shinnyu)):
                shinnyu = int(shinnyu)
            else:
                siunnyu = None
            start_timing = str(data_row["Start_timing"]).strip()
            #print(start_timing)
            if bool(re.compile("^\d+\.?\d*\Z").match(start_timing)):
                start_timing = float(start_timing)
            else:
                start_timing = None

            #if data_row["Race_Time"][:-2].isdigit():
            race_time = data_row["Race_Time"]
            if(race_time=="."):
                race_time = None
            else:
                m,s,ms = race_time.split(".")
                race_time = float(m)*60.0 + float(s) + float(ms)/10
            #if bool(re.compile("^\d+\.?\d*\Z").match(race_time)):
            date_str = str(int(data_row["Date"])).lstrip()
            date_str = "0"*(6-len(date_str)) + date_str
            if int(date_str[0]) >= 8:
                date = datetime.date(int('19' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))
            else:
                date = datetime.date(int('20' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))


            race_result_list.append(RaceResult(race_num=race_id, rank=rank, pitout_lane=pitout_lane,
                racer_id=racer_id, racer_name=racer_name, motor=motor, boat=boat, tenji=tenji,
                shinnyu=shinnyu, start_timing=start_timing, race_time=race_time, date=date, year=year))
            data_pk += 1
        except ValueError as e:
            #print(race_id)
            #print(race_time)
            print(e)
    return race_result_list, data_pk

def main():
    engine = create_engine('sqlite:///race_result_test.sqlite3')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    files = glob.glob('dataset/kyousou_csv_data/*')
    files.sort()
    for target_file in files:
        race_result_list = get_race_result_list(target_file)
        session.add_all(race_result_list)
    session.commit()

if __name__ == '__main__':
    main()
