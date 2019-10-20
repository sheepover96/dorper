import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, distinct, or_
from sqlalchemy.orm import sessionmaker
import pandas as pd

import re, datetime
#from setting import session
from models import Base, RaceResult, RaceInfo, RaceResultGrouped

def main():
    engine = create_engine('sqlite:///race_database_new.sqlite3')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    #race_num_list = session.query(RaceResult).distinct(RaceResult.race_num).all()
    race_result_grouped_list = []
    race_result = pd.read_csv('dataset/race_result_grouped_csv/race_result_2017.csv', encoding="SHIFT_JIS", dtype={'year':'int'})
    year = 2017
    for idx, data_row in race_result.iterrows():
        race_num = int(data_row['race_num'])
        lane1_racer_id = int(data_row['lane1_ID'])

        lane2_racer_id = int(data_row['lane2_ID'])
        lane3_racer_id = int(data_row['lane3_ID'])
        lane4_racer_id = int(data_row['lane4_ID'])
        lane5_racer_id = int(data_row['lane5_ID'])
        lane6_racer_id = int(data_row['lane6_ID'])

        if np.isnan(data_row['result_rank1_lane']):
            lane1_result_rank = None
        else:
            lane1_result_rank = int(data_row['result_rank1_lane'])

        if np.isnan(data_row['result_rank2_lane']):
            lane2_result_rank = None
        else:
            lane2_result_rank = int(data_row['result_rank2_lane'])

        if np.isnan(data_row['result_rank3_lane']):
            lane3_result_rank = None
        else:
            lane3_result_rank = int(data_row['result_rank3_lane'])

        if np.isnan(data_row['result_rank4_lane']):
            lane4_result_rank = None
        else:
            lane4_result_rank = int(data_row['result_rank4_lane'])

        if np.isnan(data_row['result_rank5_lane']):
            lane5_result_rank = None
        else:
            lane5_result_rank = int(data_row['result_rank5_lane'])

        if np.isnan(data_row['result_rank6_lane']):
            lane6_result_rank = None
        else:
            lane6_result_rank = int(data_row['result_rank6_lane'])

        race_result_grouped_list.append(RaceResultGrouped(
            year=year, race_num=race_num, lane1_racer_id=lane1_racer_id,
            lane2_racer_id=lane2_racer_id, lane3_racer_id=lane3_racer_id,
            lane4_racer_id=lane4_racer_id, lane5_racer_id=lane5_racer_id,
            lane6_racer_id=lane6_racer_id, lane1_result_rank=lane1_result_rank,
            lane2_result_rank=lane2_result_rank, lane3_result_rank=lane3_result_rank,
            lane4_result_rank=lane4_result_rank, lane5_result_rank=lane5_result_rank,
            lane6_result_rank=lane6_result_rank
        ))

    session.add_all(race_result_grouped_list)
    session.commit()


if __name__ == '__main__':
    main()
