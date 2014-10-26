#/usr/env/bin python

import pandas as pd
import numpy as np
import sys
import model
from sqlalchemy.orm import sessionmaker
from model import engine
Session = sessionmaker(bind=engine)
session = Session()

def get_or_create(session, mdl, **kwargs):
    instance = session.query(mdl).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = mdl(**kwargs)
        session.add(instance)
        return instance

# process command line args
if len(sys.argv) != 2:
    print "Usage: python detect_jam.py <filename> "
    sys.exit (1)
filename = sys.argv[1]

# get XYZ and station name out of file
fid = open(filename, 'r')
for idx in np.arange(1,7):
    line = fid.readline()
temp = line.split()
if len(temp) > 5:
    X = temp[3]
    Y = temp[4]
    Z = temp[5]
else:
    print "cannot get X, Y, Z data"
    X = []
    Y = []
    Z = []

# get the station name
line = fid.readline()
temp = line.split()
station = temp[-1][0:4]
station = station.upper()

# read the data into a pandas data structure
try: 
    data = pd.read_table(filename, skiprows=8, sep='\s+', parse_dates=[[0,1]],
        names = ['date', 'time', 'sat', 'S1C', 'ELE'], header=None,
        skipfooter=1, engine='python')
except:
    print("failure in parsing file ", filename)
    sys.exit(1)

# Elevation compensation
# SVs at low angles have lower C/No 
data_idx = data.loc[:,'ELE']<50.0 # && data['ELE'] > 0.0)
data_zero = data.loc[:,'ELE']==0.0 # && data['ELE'] > 0.0)
data.loc[data_idx,'S1C'] += (17.0/50.0)*(50.0-data.loc[data_idx,'ELE'])
#data.loc[data_zero,'S1C'] -= (17.0/50.0)*(50.0-data[data_zero]['ELE'])

# find the unique SVs in view
sats = np.unique(data['sat'])

# compute the jamming metrics
indicator = (data['S1C'].median() - pd.rolling_mean(data['S1C'], 30).values) > 4
intensity = data['S1C'].median() - pd.rolling_mean(data['S1C'], 30).values
date = data['date_time'].values

for idx, record in enumerate(date):
    obs = get_or_create(session, model.Observation, x=X, y=Y, z=Z, station_name=station, jam_indicator=True if indicator[idx].astype(int) == 1 else False, jam_intensity=intensity[idx], date_time=pd.to_datetime(date[idx]))

session.commit()
