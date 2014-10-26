import argparse, datetime, json, requests, subprocess, urllib, urllib2

parser = argparse.ArgumentParser(description='Detect GPS interference using CORS.')
parser.add_argument('-minlat', help="minimum latitude of bounding box", required=True)
parser.add_argument('-minlon', help="minimum longitude of bounding box", required=True)
parser.add_argument('-maxlat', help="maximum latitude of bounding box", required=True)
parser.add_argument('-maxlon', help="maximum longitude of bounding box", required=True)
parser.add_argument('-s','--start', help="a string for the start date, e.g. 2014-10-23", required=True)
parser.add_argument('-e','--end', help="a string for the end date, e.g. 2014-10-24", required=True)
args = vars(parser.parse_args())

sql = "SELECT * FROM table_1_second_cors WHERE (the_geom %26%26 ST_MakeEnvelope({0}, {1}, {2}, {3}))".format(args['minlon'], args['minlat'], args['maxlon'], args['maxlat'])
url = 'http://raudabaugh.cartodb.com/api/v2/sql?q=' + sql
r = requests.get(url, auth=('sraudabaugh@gmail.com', 'whiskeynovember'))

data = r.json()

start = datetime.datetime.strptime(args['start'], "%Y-%m-%d").date()
end = datetime.datetime.strptime(args['end'], "%Y-%m-%d").date()

for station in data['rows']:
    while start != end + datetime.timedelta(days=1):
        print 'Downloading rinex for ' + station['name']
        # do POST
        url = 'http://geodesy.noaa.gov/UFCORS/ufcors'
        yday_str = "%03d" % (start.timetuple().tm_yday,)
        values = dict(yearday=str(start.year) + '|' + yday_str,
                      yearday_year=str(start.year),
                      yearday_doy=yday_str,
                      starttime='00:00',
                      timezone='UTC',
                      duration='24',
                      siteselection=station['name'],
                      epochInterval='As Is',
                      orbits='yes'
                      )
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        rsp = urllib2.urlopen(req)
        filename = '{0}-{1}-{2}.zip'.format(station['name'],str(start.year),yday_str)
        with open(filename, 'wb') as fd:
            fd.write(rsp.read())
        print filename + ' downloaded'
        subprocess.check_call(['./process_zip.sh', filename])
        start = start + datetime.timedelta(days=1)
