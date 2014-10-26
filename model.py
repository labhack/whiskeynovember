from sqlalchemy import create_engine

engine = create_engine('postgresql://wn:wn@localhost:5432/wndb')

from sqlalchemy import Column, Integer, Float, DateTime, Boolean, String, MetaData

metadata = MetaData()
table = Table('obs', metadata, Column(Integer, primary_key=True),
    Column('station_name',String),
    Column('x',Float),
    Column('y',Float),
    Column('z',Float),
    Column('jam_indicator',Boolean),
    Column('jam_intensity',Float),
    Column('date_time',DateTime)
    )
