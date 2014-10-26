from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('postgresql://wn:wn@localhost:5432/wndb')

Base = declarative_base()

from sqlalchemy import Column, Integer, Float, DateTime, Boolean, String
class Observation(Base):
    __tablename__ = 'obs'

    id = Column(Integer, primary_key=True)
    station_name = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    jam_indicator = Column(Boolean)
    jam_intensity = Column(Float)
    date_time = Column(DateTime)

    def __repr__(self):
       return "<Observation(station_name='%r', x='%f', y='%f', z='%f', jam_indicator='%r', jam_intensity='%f', date_time='%r')>" % (
                            self.station_name, self.x, self.y, self.z, self.jam_indicator, self.jam_intensity, self.date_time)

Base.metadata.create_all(engine)

