from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date

Base = declarative_base()
 
 
class RaceResult(Base):
    __tablename__ = 'race_result'
 
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    race_num = Column(Integer)
    rank = Column(Integer)
    course = Column(Integer)
    racer_id = Column(Integer)
    racer_name = Column(String(255))

    motor = Column(Integer)
    boat = Column(Integer)
    tenji = Column(Float)
    shinnyu = Column(Integer)
    start_timing = Column(Float)
    race_time = Column(Float)
    date = Column(Date)
 
    #def __repr__(self):
    #    return "<Student(id='%s', name='%s', score='%s')>" % (self.id, self.name, self.score)
 
