# %%
from sqlalchemy import Index
from sqlalchemy import *
engine = create_engine('sqlite:///race_database_new.sqlite3')

# %%
from models import RaceResult
race_result_index = Index('race_result_index_with_pitout_lane', RaceResult.year, RaceResult.racer_id, RaceResult.pitout_lane)
race_result_index.create(bind=engine)