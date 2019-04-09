import h5py
#import json
from decimal import Decimal
import simplejson as json
import multiprocessing as mp

import time

INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'

RANGEX = 243;
RANGEY = 113;

def curveLine(mag):
    #print("Start Script")
    start = time.time()

    f = h5py.File(INPUT, 'r')

    geojs = {
        "type": "FeatureCollection",
        "features": []
    };

    longitude = f['Grid']['Longitude'];
    latitude = f['Grid']['Latitude'];

    #latDif = round(f['Grid']['Latitude'][0][1] - f['Grid']['Latitude'][0][0],5)
    #print(latDif)

    #lonDif = round(f['Grid']['Longitude'][1][0] - f['Grid']['Longitude'][0][0], 5)
    #print(lonDif)

    # Multi Process
    magDict = {0: "ammonia", 1: "cohesive sediment", 2: "density", 3: "dissolved non-refractory organic nitrogen", 4:"dissolved non-refractory organic phosphorus", 5:"dissolved refractory organic nitrogen", 6:"dissolved refractory organic phosphorus", 7:"inorganic phosphorus", 8:"nitrate", 9:"nitrite", 10:"oxygen", 11:"particulate organic nitrogen", 12:"particulate organic phosphorus", 13:"phytoplankton", 14:"salinity", 15:"short wave solar radiation", 16:"short wave solar radiation extinction", 17:"temperature", 18:"zooplankton"}
    magnitude = f['Results'][magDict[mag]]
    print(magnitude)

    # Single Process
    #magnitude = f['Results'][mag];

    for y in range(0,RANGEY):       #113
        cachedValue = round(magnitude[magDict[mag]+"_00001"][0][0][y],1)
        cachedX = 0
        print(cachedValue)
        for x in range(0,RANGEX):   #243
            relevant = False
            value = round(magnitude[magDict[mag]+"_00001"][0][x][y],1)
            if ( value != cachedValue ):
                relevant = True
            if ( x == RANGEX ):         # If in the last square
                relevant = True
            if relevant:
                if ( cachedValue != -9900000000000000):
                    if ( value == -9900000000000000):
                        if ( y < RANGEY and y > 0 ):
                            valueAbove = round(magnitude[magDict[mag] + "_00001"][0][x][y+1], 1)
                            valueBelow = round(magnitude[magDict[mag] + "_00001"][0][x][y-1], 1)
                            if ( value != valueBelow and value != valueAbove ):
                                coord = [
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                    [round(longitude[x+1][y], 5), round(latitude[x+1][y], 5)],
                                    [round(longitude[x+1][y + 1], 5), round(latitude[x+1][y + 1], 5)],
                                    [round(longitude[cachedX][y + 1], 5), round(latitude[cachedX + 1][y + 1], 5)],
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                ]
                            elif ( value != valueAbove ):
                                coord = [
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                    [round(longitude[x][y], 5), round(latitude[x][y], 5)],
                                    [round(longitude[x+1][y + 1], 5), round(latitude[x+1][y + 1], 5)],
                                    [round(longitude[cachedX][y + 1], 5), round(latitude[cachedX+1][y + 1], 5)],
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                ]
                            elif ( value != valueBelow ):
                                coord = [
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                    [round(longitude[x+1][y], 5), round(latitude[x+1][y], 5)],
                                    [round(longitude[x][y + 1], 5), round(latitude[x][y + 1], 5)],
                                    [round(longitude[cachedX][y + 1], 5), round(latitude[cachedX + 1][y + 1], 5)],
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                ]
                            else:
                                coord = [
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                    [round(longitude[x][y], 5), round(latitude[x][y], 5)],
                                    [round(longitude[x][y + 1], 5), round(latitude[x][y + 1], 5)],
                                    [round(longitude[cachedX][y + 1], 5), round(latitude[cachedX + 1][y + 1], 5)],
                                    [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                                ]
                    else:
                        coord = [
                            [round(longitude[cachedX][y],5),round(latitude[cachedX][y],5)],
                            [round(longitude[x][y],5),round(latitude[x][y],5)],
                            [round(longitude[x][y+1], 5), round(latitude[x][y+1], 5)],
                            [round(longitude[cachedX][y+1], 5), round(latitude[cachedX][y+1], 5)],
                            [round(longitude[cachedX][y], 5), round(latitude[cachedX][y], 5)],
                        ]

                    polygon = {
                        "type": "Feature",
                        "properties": {magDict[mag]+"_00001":cachedValue},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [ coord ]
                        }
                    }
                    geojs["features"].append(polygon);



                cachedX = x;
                cachedValue = value;


    print("Exporting Data to JSON");

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    print(geojs);

    print("Exiting Program")

    end = time.time()
    print("Script Execution: ",round(end - start, 2))


def multiProcessing():
    pool = mp.Pool(mp.cpu_count())
    # results = pool.map(line, range(0, GRID_X));
    results = pool.map(curveLine, range(0, 3))

    print( results )
    # results = [pool.apply(line, args=(x, )) for x in range(0, GRID_X)]

curveLine(17)
#multiProcessing()

