import h5py
#import json
from decimal import Decimal
import simplejson as json
import multiprocessing as mp

import time

INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'

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

    lines = {}

    for x in range(0, 243):
        for y in range(0, 114):
            border = False
            for time_series in magnitude:
                if (int(time_series[-5:]) == 1):
                    data = magnitude[time_series][0][x][y]
                    if (data != -9900000000000000.0):      # Check if value is useful
                        data = round(data, 1)
                        if ( data != round(magnitude[time_series][0][x+1][y],1) or data != round(magnitude[time_series][0][x][y+1],1) or data != round(magnitude[time_series][0][x+1][y+1],1) ):
                            border = True
                        if ( border ):
                            coord = (round(longitude[x][y], 5),round(latitude[x][y],5))
                            if ( data in lines ):
                                lines[data].append(coord)
                                #print("value exists")
                            else:
                                #print("value doesnt exist")
                                lines[data] = [coord]

    print(lines)



            #value = magnitude[0][x][y]
            #if ( value )

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
    results = pool.map(curveLine, range(0, 3))

    print( results )
    # results = [pool.apply(line, args=(x, )) for x in range(0, GRID_X)]

curveLine(17)
#multiProcessing()

