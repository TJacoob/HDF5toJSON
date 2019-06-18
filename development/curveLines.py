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

    for x in range(0, 10):
        for y in range(0, 10):
            # Marching Squares Implementation
            for time_series in magnitude:
                if (int(time_series[-5:]) == 1):
                    value = round(magnitude[time_series][0][x][y],1)
                    if value not in lines:
                        lines[value] = []
                    if ( value != -9900000000000000.0 ): # Check if data is relevant
                        direita = round(magnitude[time_series][0][x+1][y],1)
                        baixo = round(magnitude[time_series][0][x][y+1], 1)
                        direitabaixo = round(magnitude[time_series][0][x+1][y+1], 1)
                        if (x == 0 and y == 0):
                            lines[value].append([round(longitude[x][y], 5), round(latitude[x][y], 5)])
                        elif ( value != direita ):  # Direita
                            if ( direita not in lines ):
                                lines[direita] = []
                            lines[value].append([round(longitude[x][y], 5), round(latitude[x][y], 5)])
                            lines[direita].append([round(longitude[x+1][y], 5), round(latitude[x+1][y], 5)])
                            print("Cell (%s, %s) added" % (x, y))
                        elif ( value != baixo ):  # Baixo
                            if ( baixo not in lines ):
                                lines[baixo] = []
                            lines[value].append([round(longitude[x][y], 5), round(latitude[x][y], 5)])
                            lines[baixo].append([round(longitude[x][y+1], 5), round(latitude[x][y+1], 5)])
                            print("Cell (%s, %s) added" % (x, y))
                        elif ( value != direitabaixo ):  # Baixo e Direita
                            if ( direitabaixo not in lines ):
                                lines[direitabaixo] = []
                            lines[value].append([round(longitude[x][y], 5), round(latitude[x][y], 5)])
                            lines[direitabaixo].append([round(longitude[x+1][y+1], 5), round(latitude[x+1][y+1], 5)])
                            print("Cell (%s, %s) added" % (x, y))
                        else:
                            print("Cell (%s, %s) ignored" % (x,y))

    print(lines)

    print("Transforming Values into geoJson")

    geojs = {
        "type": "FeatureCollection",
        "features": []
    };

    for value in lines:

        #print("Valor: ",value)
        #print(len(lines[value]))

        if len(lines[value]) == 1:
            continue

        print(lines[value])
        lines[value].append(lines[value][0])
        print(lines[value])

        area = {
            "type": "Feature",
            "properties": {magDict[mag]:value},
            "geometry": {
                "type": "Polygon",
                "coordinates": [lines[value]]
            }
        }

        geojs["features"].append(area)


    #value = magnitude[0][x][y]
    #if ( value )

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

