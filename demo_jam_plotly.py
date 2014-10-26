#/usr/env/bin python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import plotly.plotly as py


# Use argv for filename and default if doesn't exist
if len(sys.argv) != 2:
    print "Usage: python demo_jam.py <filename> "
    filename = 'sc013070-09o.rindump'
    print "Using default data file for demo: ", filename
else:
    filename = sys.argv[1]

# read the data into a pandas data structure
try:
    data = pd.read_table(filename, skiprows=8, sep='\s+', parse_dates=[[0,1]],
                names = ['date', 'time', 'sat', 'S1C', 'ELE'], header=None,
                skipfooter=1, engine='python')
except:
    print("failure in parsing file ", filename)
    sys.exit(1)

py.sign_in('nuthaus', '2c9uspwge8')
# find the unique SVs in view
sats = np.unique(data['sat'])

# create a plot of all the PRNs to frame the detection problem
plt.figure()
svgroup = data.groupby('sat')
svgroup['S1C'].plot()
plt.title('Carrier-to-Noise Ratio: Is GPS jamming present?')
plot_url = py.plot_mpl(plt.gcf())

# compute the jamming metrics
indicator = (data['S1C'].median()-pd.rolling_mean(data['S1C'], 30).values) > 4
intensity = data['S1C'].median() - pd.rolling_mean(data['S1C'], 30).values
dates = data['date_time'].values

# plot the jamming metrics
plt.figure(tight_layout=True)
plt.subplot(211)
plt.ylabel('Intensity')
plt.plot(intensity)
plt.title('Developing a jamming intensity and detection metric')
plt.subplot(212)
plt.plot(indicator)
plt.ylabel('Indicator')
plot_url = py.plot_mpl(plt.gcf())
#plt.show()

# TODO: make into subplots?
demo_sats = ['G08', 'G11', 'G13', 'G17', 'G22']
for sv in demo_sats:
    plt.figure()
    plt.title(sv)
    svgroup['S1C'].get_group(sv).plot()
    svgroup['ELE'].get_group(sv).plot()
    plt.ylabel('C/N^o dB/Hz')
    py.plot_mpl(plt.gcf())
    #plt.show()

el_demo_sats = ['G32']
plt.figure()
plot_idx = 211
for sv in el_demo_sats:
    plt.subplot(plot_idx)
    title = 'Elevation Compensation ' + sv
    plt.title(title)
    svgroup['S1C'].get_group(sv).plot()
    svgroup['ELE'].get_group(sv).plot()
    plt.ylabel('C/N^o dB/Hz')

# Elevation compensation
# SVs at low angles have lower C/No 
data_idx = data.loc[:,'ELE']<50.0 # && data['ELE'] > 0.0)
data_zero = data.loc[:,'ELE']==0.0 # && data['ELE'] > 0.0)
data.loc[data_idx,'S1C'] += (17.0/50.0)*(50.0-data.loc[data_idx,'ELE'])
#data.loc[data_zero,'S1C'] -= (17.0/50.0)*(50.0-data[data_zero]['ELE'])

el_demo_sats = ['G32']
plot_idx = 212
for sv in el_demo_sats:
    title = 'Elevation Compensation ' + sv
    plt.title(title)
    svgroup['S1C'].get_group(sv).plot()
    svgroup['ELE'].get_group(sv).plot()
    plt.ylabel('C/N^o dB/Hz')
    plot_idx +=10
py.plot_mpl(plt.gcf())
