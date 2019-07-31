import sqlalchemy
from sqlalchemy import create_engine, distinct, or_
from sqlalchemy.orm import sessionmaker
import pandas as pd

from setting import session
from models import Base, RaceResult, RaceInfo

def main():
    engine = create_engine('sqlite:///race_database_new.sqlite3')
    Base.metadata.create_all(engine)
    #race_num_list = session.query(RaceResult).distinct(RaceResult.race_num).all()
    race_info_list = []
    print('a')
    race_result_list_year = {}
    race_metadata = pd.read_csv('dataset/whole_race_meta.csv', encoding="SHIFT_JIS", dtype={'year':'int'})
    for year in range(2000, 2019):
        tmp_res_list = session.query(RaceResult).filter(RaceResult.year==year)
        race_result_list_year[year] = tmp_res_list

    for year in range(2000, 2019):
        race_metadata_year = race_metadata[race_metadata['year']==year]

        race_result_year_all = race_result_list_year[year].distinct(RaceResult.race_num).all()
        race_result_num_year_all = session.query(RaceResult.race_num).filter(RaceResult.year==year).distinct(RaceResult.race_num).all()

        non_valid_race_result_year = race_result_list_year[year].filter(RaceResult.rank>6, RaceResult.rank<1).all()
        non_valid_race_num_list_year = [race_result.race_num for race_result in non_valid_race_result_year]
        non_valid_race_num_set_year = set(non_valid_race_num_list_year)

        non_valid_race_times_record_year = race_result_list_year[year].filter(RaceResult.race_time == None).all()
        non_valid_race_times_record_num_list_year = [race_result.race_num for race_result in non_valid_race_times_record_year]
        non_valid_race_times_record_num_set_year = set(non_valid_race_times_record_num_list_year)

        for idx, race_num_obj in enumerate(race_result_num_year_all):
            race_num = race_num_obj.race_num
            race_result_info = race_metadata_year[race_metadata_year['race_num']==race_num]
            if not race_result_info.empty:
                lane_length = str(race_result_info['lane_length'].iat[0])
                weather = str(race_result_info['weather'].iat[0])
                wind_direction = str(race_result_info['wind_direction'].iat[0])
                wind_strength = int(race_result_info['wind_strength'])
                wave_height = int(race_result_info['wave_height'])
                #print(race_metadata_year[race_metadata_year['race_num']==race_num])
                is_race_no_flying = False
                is_race_times_record_valid = False
                if not race_num in non_valid_race_num_set_year:
                    is_race_no_flying = True
                if not race_num in non_valid_race_times_record_num_set_year:
                    is_race_times_record_valid = True
                new_race_info = RaceInfo(race_num=race_num, year=year, is_race_no_flying=is_race_no_flying,
                is_race_times_record_valid=is_race_times_record_valid, lane_length=lane_length,
                weather=weather, wind_direction=wind_direction, wind_strength=wind_strength, wave_height=wave_height)
                race_info_list.append(new_race_info)


    session.add_all(race_info_list)
    session.commit()
    

if __name__ == '__main__':
    main()