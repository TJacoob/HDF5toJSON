# IMPORTS
import h5py
import simplejson as json

from decimal import Decimal

import time

# SETTINGS
INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'
GRID_X = 255    # These are overriden below, but can be used for testing
GRID_Y = 115

def convertor():
    start = time.time()
    print("Starting Conversion")

    # GeoJson object that will be dumped into a json file
    geojs = {
        "type": "FeatureCollection",
        "features": []
    }

    # Load Input File into h5py library
    f = h5py.File(INPUT, 'r')

    longitude = f['Grid']['Longitude']
    latitude = f['Grid']['Latitude']

    GRID_X = longitude.shape[0]
    GRID_Y = longitude.shape[1]

    results = f['Results']

    print("Collecting Data")

    for x in range(0,GRID_X):      # Should match the grid size
        for y in range(0,GRID_Y):
            # GeoJson object for each cell
            unit = {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[]]
                }
            }

            # Coordinates for this cell (rounded down to 5 decimals)
            coordinates = [
                [json.dumps(round(longitude[x][y],5)), json.dumps(round(latitude[x][y],5))],
                [json.dumps(round(longitude[x+1][y+1],5)), json.dumps(round(latitude[x][y],5))],
                [json.dumps(round(longitude[x+1][y+1],5)), json.dumps(round(latitude[x+1][y+1],5))],
                [json.dumps(round(longitude[x][y],5)), json.dumps(round(latitude[x+1][y+1],5))],
                [json.dumps(round(longitude[x][y],5)), json.dumps(round(latitude[x][y],5))],
            ]
            unit['geometry']['coordinates'][0]=coordinates

            # Annex Variables value for this cell
            for result in results:
                stat = f['Results'][result];
                for t in stat:          # Iterate over all variables
                    if ( t[-5:] == "00001"):    # Only reading the first time entry (checks last 5 digits of the name)
                        unit['properties'][stat.name[9:]] = json.dumps(round(Decimal(stat[t][0][x][y]), 5));    # Rounded down to 5 decimals

            # Unit is Ready, annexing to the geojs
            geojs['features'].append(unit);

    print("Exporting Data to JSON");

    with open(OUTPUT, 'w') as outfile:
        json.dump(geojs, outfile)

    # print(geojs);

    print("Finished Script")

    end = time.time()
    print(end - start)

convertor();