#/usr/env/bin python

import pandas as pd
import numpy as np
import sys
import model
from model import engine
from model import table
conn = engine.connect()

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
dates = data['date_time'].values

vals = []
print 'Adding record to db...'
for idx, record in enumerate(dates):
    date=pd.to_datetime(dates[idx])
    record_dict = {}
    record_dict['x']=X
    record_dict['y']=Y
    record_dict['z']=Z
    record_dict['station_name']=station
    record_dict['jam_indicator']=True if indicator[idx].astype(int) == 1 else False
    record_dict['jam_intensity']=intensity[idx]
    record_dict['date_time']=date
    vals.append(record_dict)

conn.execute(table.insert(), vals)
print 'Record successfully added.'
