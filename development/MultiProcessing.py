# IMPORTS
import h5py
import simplejson as json

from decimal import Decimal

import time

import multiprocessing as mp

# SETTINGS
PROCESSORS = 4      #os.cpu_count()
INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'
GRID_X = 200    # These are overriden below, but can be used for testing
GRID_Y = 114
longitude = []
latitude = []
results = []

def convertor():
    global longitude
    global latitude
    global results

    print("Processors: ", mp.cpu_count())

    print("Starting Convertor")
    start = time.time()

    f = h5py.File(INPUT, 'r')

    print("Setting Up Data")

    # Setup
    longitude = f['Grid']['Longitude'];
    latitude = f['Grid']['Latitude'];

    #GRID_X = longitude.shape[0];
    #GRID_Y = longitude.shape[1];

    results = f['Results'];

    print("Starting cycle");


    geojs = cycle()

    print("Exporting Data to JSON");

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    # print(geojs);

    print("Exiting Program")

    end = time.time()
    print(round(end - start,1))



def cycle():

    geojs = {
        "type": "FeatureCollection",
        "features": []
    }

    pool = mp.Pool(mp.cpu_count())
    #results = pool.map(line, range(0, GRID_X));
    pool.map(line, range(0, GRID_X))
    #results = [pool.apply(line, args=(x, )) for x in range(0, GRID_X)]

    #print(results[0])

    '''
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            unit = cell(x,y);
            geojs['features'].append(unit);
    '''
    for l in results:
        for c in l:
            geojs['features'].append(c);

    print ( geojs )
    return geojs;


def line(x):
    print("Line: ", x)
    # Receives a coordinate and returns a json object with the variables and coordinates
    line = []
    for y in range(0, GRID_Y):

        unit = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[]]
            }
        };

        # Grid
        '''
        coordinates = [
            [json.dumps(round(longitude[x][y], 5)), json.dumps(round(latitude[x][y], 5))],
            [json.dumps(round(longitude[x + 1][y + 1], 5)), json.dumps(round(latitude[x][y], 5))],
            [json.dumps(round(longitude[x + 1][y + 1], 5)), json.dumps(round(latitude[x + 1][y + 1], 5))],
            [json.dumps(round(longitude[x][y], 5)), json.dumps(round(latitude[x + 1][y + 1], 5))],
            [json.dumps(round(longitude[x][y], 5)), json.dumps(round(latitude[x][y], 5))],
        ];
        '''
        coordinates=[];
        unit['geometry']['coordinates'][0] = coordinates;

        # Annex Results
        for result in results:
            stat = results[result];
            for t in stat:
                if (t[-5:] == "00001"):  # Only reading the first time entry (checks last 5 digits of the name)
                    unit['properties'][stat.name[9:]] = json.dumps(round(Decimal(stat[t][0][x][y]), 5));  # Rounded down to 5

        line.append(unit)

    return line

convertor()