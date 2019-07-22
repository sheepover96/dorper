import sqlalchemy
from sqlalchemy import create_engine, distinct, or_
from sqlalchemy.orm import sessionmaker

from setting import session
from models import Base, RaceResult, RaceInfo

def main():
    engine = create_engine('sqlite:///race_database_new.sqlite3')
    Base.metadata.create_all(engine)
    race_num_list = session.query(RaceResult).distinct(RaceResult.race_num).all()
    race_info_list = []
    print('a')
    race_result_list_year = {}
    for year in range(2000, 2019):
        tmp_res_list = session.query(RaceResult).filter(RaceResult.year==year)
        race_result_list_year[year] = tmp_res_list

    for year in range(2000, 2019):
        race_result_year_all = race_result_list_year[year].distinct(RaceResult.race_num).all()

        non_valid_race_result_year = race_result_list_year[year].filter(RaceResult.rank>6, RaceResult.rank<1).all()
        non_valid_race_num_list_year = [race_result.race_num for race_result in non_valid_race_result_year]
        non_valid_race_num_set_year = set(non_valid_race_num_list_year)
        for idx, race_num_obj in enumerate(race_result_year_all):
            print(idx)
            race_num = race_num_obj.race_num
            is_valid = False
            if not race_num in non_valid_race_num_set_year:
                is_valid = True
            new_race_info = RaceInfo(race_num=race_num, year=year, is_race_valid=is_valid)
            race_info_list.append(new_race_info)
        #print(race_info_list)
    session.add_all(race_info_list)
    session.commit()
    

if __name__ == '__main__':
    main()