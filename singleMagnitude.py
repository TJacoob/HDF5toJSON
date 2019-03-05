import h5py
#import json
from decimal import Decimal
import simplejson as json

import time

INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'

def singleMagnitude(mag):
    print("Start Script")
    start = time.time()

    f = h5py.File(INPUT, 'r')

    geojs = {
        "type": "FeatureCollection",
        "features": []
    };

    longitude = f['Grid']['Longitude'];
    latitude = f['Grid']['Latitude'];

    latDif = round(f['Grid']['Latitude'][0][1] - f['Grid']['Latitude'][0][0],5)
    print(latDif)

    lonDif = round(f['Grid']['Longitude'][1][0] - f['Grid']['Longitude'][0][0], 5)
    print(lonDif)

    magnitude = f['Results'][mag];

    for x in range(0, 244):
        for y in range(0, 115):
            cell = {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[]]
                }
            }

            lat = round(latitude[x][y],5)
            latPlus = lat + latDif

            lon = round(longitude[x][y], 5)
            lonPlus = lon + lonDif

            coordinates = [
                [json.dumps(lon), json.dumps(lat)],
                [json.dumps(lonPlus), json.dumps(lat)],
                [json.dumps(lonPlus), json.dumps(latPlus)],
                [json.dumps(lon), json.dumps(latPlus)],
                [json.dumps(lon), json.dumps(lat)],
            ];

            cell['geometry']['coordinates'][0] = coordinates;

            for time_series in magnitude:
                #print(time_series)
                if ( time_series[:5]=='00001' ):
                    data = f['Results'][mag][time_series]
                    cell['properties'][time_series] = json.dumps(round(Decimal(data[0][x][y]), 5))

            geojs['features'].append(cell)

    print("Exporting Data to JSON");

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    # print(geojs);

    print("Exiting Program")

    end = time.time()
    print("Script Execution: ",round(end - start, 2))




singleMagnitude('ammonia')

