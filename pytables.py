from tables import *
import simplejson as json
from decimal import Decimal

import time

INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'

def convertor():
    h5file = open_file(INPUT, "r")

    #print(h5file.__dict__['filename'])

    start = time.time()
    print("Starting Script")

    geojs = {
        "type": "FeatureCollection",
        "features": []
    }

    results = h5file.get_node("/Results")

    for x in range(0,1):
        start = time.time()
        for y in range(0,115):
            cell = {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[]]
                }
            }

            for magnitude in results:
                for time_capture in magnitude:
                    if (time_capture.name[-5:] == "00001"):
                        cell['properties'][time_capture.name[:-6]] = json.dumps(round(Decimal(time_capture[0][x][y]), 5));

            geojs['features'].append(cell);

        end = time.time()
        print("Per Line: ", round(end - start, 2))

    #print(geojs);

    h5file.close()

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    #print(geojs);

    print("Exiting Program")



convertor()