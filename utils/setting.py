from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///race_database_new.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()