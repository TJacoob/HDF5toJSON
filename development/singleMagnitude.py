import h5py
#import json
from decimal import Decimal
import simplejson as json
import multiprocessing as mp

import time

INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'

def singleMagnitude(mag):
    #print("Start Script")
    start = time.time()

    f = h5py.File(INPUT, 'r')

    geojs = {
        "type": "FeatureCollection",
        "features": []
    };

    longitude = f['Grid']['Longitude'];
    latitude = f['Grid']['Latitude'];

    latDif = round(f['Grid']['Latitude'][0][1] - f['Grid']['Latitude'][0][0],5)
    #print(latDif)

    lonDif = round(f['Grid']['Longitude'][1][0] - f['Grid']['Longitude'][0][0], 5)
    #print(lonDif)

    # Multi Process
    magDict = {0: "ammonia", 1: "cohesive sediment", 2: "density", 3: "dissolved non-refractory organic nitrogen", 4:"dissolved non-refractory organic phosphorus", 5:"dissolved refractory organic nitrogen", 6:"dissolved refractory organic phosphorus", 7:"inorganic phosphorus", 8:"nitrate", 9:"nitrite", 10:"oxygen", 11:"particulate organic nitrogen", 12:"particulate organic phosphorus", 13:"phytoplankton", 14:"salinity", 15:"short wave solar radiation", 16:"short wave solar radiation extinction", 17:"temperature", 18:"zooplankton"}
    magnitude = f['Results'][magDict[mag]]
    print(magnitude)

    # Single Process
    #magnitude = f['Results'][mag];

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
                    data = magnitude[time_series]
                    cell['properties'][time_series] = json.dumps(round(Decimal(data[0][x][y]), 5))

            geojs['features'].append(cell)

    #print("Exporting Data to JSON");

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    # print(geojs);

    #print("Exiting Program")

    end = time.time()
    print("Script Execution: ",round(end - start, 2))


def multiProcessing():
    pool = mp.Pool(mp.cpu_count())
    # results = pool.map(line, range(0, GRID_X));
    results = pool.map(singleMagnitude, range(0, 3))

    print( results )
    # results = [pool.apply(line, args=(x, )) for x in range(0, GRID_X)]

def main():
    try:
        singleMagnitude(17)
    except Exception as e:
        print("Some Exception")

main()
#multiProcessing()

