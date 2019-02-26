# IMPORTS
import h5py
import simplejson as json

from decimal import Decimal

import time

# SETTINGS
INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'
GRID_X = 10    # These are overriden below, but can be used for testing
GRID_Y = 10
longitude = []
latitude = []
results = []

def convertor():
    global longitude
    global latitude
    global results

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

    print("starting cycle");

    geojs = cycle(0, GRID_X, 0, GRID_Y)

    print("Exporting Data to JSON");

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    # print(geojs);

    print("Exiting Program")

    end = time.time()
    print(end - start)



def cycle(minX, maxX, minY, maxY):

    geojs = {
        "type": "FeatureCollection",
        "features": []
    }

    for x in range(minX, maxX):
        for y in range(minY, maxY):
            unit = cell(x,y);
            geojs['features'].append(unit);

    return geojs;



def cell(x,y):
    # Receives a coordinate and returns a json object with the variables and coordinates
    unit = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[]]
        }
    };

    # Grid
    coordinates = [
        [json.dumps(round(longitude[x][y], 5)), json.dumps(round(latitude[x][y], 5))],
        [json.dumps(round(longitude[x + 1][y + 1], 5)), json.dumps(round(latitude[x][y], 5))],
        [json.dumps(round(longitude[x + 1][y + 1], 5)), json.dumps(round(latitude[x + 1][y + 1], 5))],
        [json.dumps(round(longitude[x][y], 5)), json.dumps(round(latitude[x + 1][y + 1], 5))],
        [json.dumps(round(longitude[x][y], 5)), json.dumps(round(latitude[x][y], 5))],
    ];
    unit['geometry']['coordinates'][0] = coordinates;

    # Annex Results
    for result in results:
        stat = results[result];
        for t in stat:
            if (t[-5:] == "00001"):  # Only reading the first time entry (checks last 5 digits of the name)
                unit['properties'][stat.name[9:]] = json.dumps(round(Decimal(stat[t][0][x][y]), 5));  # Rounded down to 5

    return unit

convertor()