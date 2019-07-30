import sqlalchemy
from sqlalchemy import create_engine, distinct, or_
from sqlalchemy.orm import sessionmaker
import pandas as pd

import re, datetime, math
from setting import session
from models import Base, RaceOdds

def main():
    engine = create_engine('sqlite:///race_database_new.sqlite3')
    Base.metadata.create_all(engine)
    #race_num_list = session.query(RaceResult).distinct(RaceResult.race_num).all()
    race_odds_list = []
    race_odds_df = pd.read_csv('dataset/whole_race_odds.csv', encoding="SHIFT_JIS", dtype={'year':'int'})
    for idx, data_row in race_odds_df.iterrows():
        race_num = int(data_row['race_num'])
        year = int(data_row['year'])

        rank1_lane = data_row['rank1_lane']
        if not math.isnan(rank1_lane):
            rank1_lane = int(rank1_lane)

        rank2_lane = int(data_row['rank2_lane'])
        if not math.isnan(rank2_lane):
            rank2_lane = int(rank2_lane)

        rank3_lane = data_row['rank3_lane']
        if not math.isnan(rank3_lane):
            rank3_lane = int(rank3_lane)

        tanshou = data_row['tanshou']
        if not math.isnan(tanshou):
            tanshou = int(tanshou)

        fukushou1 = data_row['fukushou1']
        if not math.isnan(fukushou1):
            fukushou1 = int(fukushou1)

        fukushou2 = data_row['fukushou2']
        if not math.isnan(fukushou2):
            fukushou2 = int(fukushou2)

        nirentan = data_row['nirentan']
        if not math.isnan(nirentan):
            nirentan = int(nirentan)

        nirenfuku = data_row['nirenfuku']
        if not math.isnan(nirenfuku):
            nirenfuku = int(nirenfuku)

        kakurenfuku1_2 = data_row['kakurenfuku1_2']
        if not math.isnan(kakurenfuku1_2):
            kakurenfuku1_2 = int(kakurenfuku1_2)

        kakurenfuku1_3 = data_row['kakurenfuku1_3']
        if not math.isnan(kakurenfuku1_3):
            kakurenfuku1_3 = int(kakurenfuku1_3)

        kakurenfuku2_3 = data_row['kakurenfuku2_3']
        if not math.isnan(kakurenfuku2_3):
            kakurenfuku2_3 = int(kakurenfuku2_3)

        sanrentan = data_row['sanrentan']
        if not math.isnan(sanrentan):
            sanrentan = int(sanrentan)

        sanrenfuku = data_row['sanrenfuku']
        if not math.isnan(sanrenfuku):
            sanrenfuku = int(sanrenfuku)

        race_odds_list.append(RaceOdds(race_num=race_num, year=year, rank1_lane=rank1_lane, rank2_lane=rank2_lane,
            rank3_lane=rank3_lane, tanshou=tanshou, fukushou1=fukushou1, fukushou2=fukushou2,
            nirentan=nirentan, nirenfuku=nirenfuku, kakurenfuku1_2=kakurenfuku1_2,
            kakurenfuku1_3=kakurenfuku1_3, kakurenfuku2_3=kakurenfuku2_3, sanrentan=sanrentan,sanrenfuku=sanrenfuku))
    session.add_all(race_odds_list)
    session.commit()
    

if __name__ == '__main__':
    main()
