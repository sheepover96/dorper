import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import datetime

from models import Base, RaceResult

def get_race_result_list():
    df = pd.read_csv('race_2018.csv', encoding="SHIFT_JIS")
    df2 = pd.read_csv('race_valid_2018.csv')
    year = 2018
    data_pk = 0
    race_result_list = []
    for data_row in df.iterrows():
        race_id = int(data_row[1][0])
        is_valid = df2[df2['Race_num'] == race_id]
        if is_valid.iat[0,1]:
            try:
                rank = int(data_row[1][1])
                course = int(data_row[1][2])
                racer_id = int(data_row[1][3])
                racer_name = data_row[1][4]
                motor = int(data_row[1][5])
                boat = int(data_row[1][6])
                tenji = float(data_row[1][7])
                shinnyu = int(data_row[1][8])
                start_timing = float(data_row[1][9])
                race_time = float(data_row[1][10][:-2])
                date_str = str(data_row[1][11])
                if int(date_str[0]) > -1 and 7 > int(date_str[0]):
                    date = datetime.date(int('20' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))
                else:
                    date = datetime.date(int('19' + date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))
                print(date)

                race_result_list.append(RaceResult(id=data_pk, race_num=race_id, rank=rank, course=course,
                    racer_id=racer_id, racer_name=racer_name, motor=motor, boat=boat, tenji=tenji,
                    shinnyu=shinnyu, start_timing=start_timing, race_time=race_time, date=date, year=year))
                data_pk += 1
            except ValueError as e:
                print(e)

    return race_result_list

def main():
    engine = create_engine('sqlite:///race_result.sqlite3')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    race_result_list = get_race_result_list()
    session.add_all(race_result_list)
    session.commit()

if __name__ == '__main__':
    main()
