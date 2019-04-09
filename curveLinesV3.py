import h5py
#import json
from decimal import Decimal
import simplejson as json
import multiprocessing as mp

import time

INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'

#RANGEX = 243;
#RANGEY = 113;

RANGEX = 20;
RANGEY = 20;

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

    cachedValue = round(magnitude[magDict[mag] + "_00001"][0][0][0], 1)

    y = 0
    xList = [0] * RANGEY  #List of the X value for each Y

    polygonStartedY = 0
    cachedX = 0

    polygonFinished = False
    newLine = False

    polygonCoordsLeft = []
    polygonCoordsRight = []

    while y < RANGEY:
        x = xList[y]
        if polygonFinished:
            polygonStartedY = y
            polygonFinished = False
            # Add polygon and cached value to geojs, clear arrays
            polygon = {
                "type": "Feature",
                "properties": {magDict[mag] + "_00001": cachedValue},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [polygonCoordsLeft[0]],
                        [polygonCoordsRight[0]],
                        [polygonCoordsRight[1]],
                        [polygonCoordsLeft[1]],
                        [polygonCoordsLeft[0]],
                    ]]
                }
            }
            geojs["features"].append(polygon)
            polygonCoordsLeft = []
            polygonCoordsRight = []
            cachedValue = round(magnitude[magDict[mag] + "_00001"][0][x][y], 1)
        while x < RANGEX:
            value = round(magnitude[magDict[mag] + "_00001"][0][x][y], 1)
            if ( value == cachedValue ):
                if newLine :            # If we jumped to a new line, and the value remains the same as the cached value
                    newLine = False     # then this still belongs to the polygon, and we should add the coordinates
                    polygonCoordsLeft.append([round(longitude[x][y], 5), round(latitude[x][y], 5)])
                x += 1
            elif ( value != cachedValue):
                if newLine :
                    polygonCoordsRight.append([round(longitude[x+1][y], 5), round(latitude[x+1][y], 5)])
                    polygonCoordsLeft.append([round(longitude[x][y], 5), round(latitude[x][y], 5)])
                    polygonCoordsLeft.append([round(longitude[xList[polygonStartedY]-1][polygonStartedY], 5), round(latitude[xList[polygonStartedY]-1][polygonStartedY], 5)])
                    polygonFinished = True
                    newLine = False
                    y = polygonStartedY           # Reset Y and start the process over from the top
                    break                         # The line starts where the X was the last we were on that line (xList)
                else:
                    polygonCoordsRight.append([round(longitude[x][y], 5), round(latitude[x][y], 5)])
                    xList[y] = x  # Register the x where this line skipped to the next
                    y += 1         # Jump to the next line
                    newLine = True
                    break


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

