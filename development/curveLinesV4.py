import h5py
#import json
from decimal import Decimal
import simplejson as json
import multiprocessing as mp

import time

INPUT = 'testFiles/WaterProperties_Surface.hdf5'
#OUTPUT = 'testFiles/newdata.json'

RANGEX = 124;
RANGEY = 176;

#RANGEX = 100;
#RANGEY = 100;

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
    print(magDict[mag])
    OUTPUT = 'testFiles/' + magDict[mag] + '.json'

    for y in range(0,RANGEY):
        startValue = round(magnitude[magDict[mag] + "_00001"][0][0][y], 1)
        polygonStartX = 0
        coords = [None, None, None, None, None]
        for x in range(0, RANGEX):
            value = round(magnitude[magDict[mag] + "_00001"][0][x][y], 1)
            if ( value == startValue and x!= RANGEX-1):
                continue

            # If the value is different from the previous cell than the polygon is over
            # Now we should check the first and last cells for adjustments
            # The adjustments check the adjacent cells to decide the shape it should take

            # These adjustments use the cells above and below to decide, so they don't work on the first and last line
            if ( y == 0 or y == RANGEY ):
                # Not quite sure what should happen
                #print("Edge of the map")
                continue

            else:
                # Check above and below for the first cell (left):
                valueAbove = round(magnitude[magDict[mag] + "_00001"][0][polygonStartX][y+1], 1)
                valueBelow = round(magnitude[magDict[mag] + "_00001"][0][polygonStartX][y-1], 1)
                if ( valueAbove == startValue and valueBelow == startValue ):      # Same above and below: |
                    coords[0] = [round(longitude[polygonStartX][y], 5), round(latitude[polygonStartX][y], 5)]
                    coords[3] = [round(longitude[polygonStartX][y+1], 5), round(latitude[polygonStartX][y+1], 5)]
                elif (valueAbove == startValue and valueBelow != startValue):  # Same only above: \
                    coords[0] = [round(longitude[polygonStartX + 1][y], 5), round(latitude[polygonStartX + 1][y], 5)]
                    coords[3] = [round(longitude[polygonStartX][y + 1], 5), round(latitude[polygonStartX][y + 1], 5)]
                elif (valueAbove != startValue and valueBelow == startValue):  # Same only below: /
                    coords[0] = [round(longitude[polygonStartX][y], 5), round(latitude[polygonStartX][y], 5)]
                    coords[3] = [round(longitude[polygonStartX + 1][y + 1], 5),round(latitude[polygonStartX + 1][y + 1], 5)]
                elif (valueAbove != startValue and valueBelow != startValue):  # Both different (to do): |
                    coords[0] = [round(longitude[polygonStartX][y], 5), round(latitude[polygonStartX][y], 5)]
                    coords[3] = [round(longitude[polygonStartX][y+1], 5), round(latitude[polygonStartX][y+1], 5)]

                coords[4] = coords[0]   # First and last coords must be the same to close the polygon
                                        # This way we don't read the same value twice, (slightly) improving performance

                # Check above and below for the last cell (right):
                valueAbove = round(magnitude[magDict[mag] + "_00001"][0][x][y + 1], 1)
                valueBelow = round(magnitude[magDict[mag] + "_00001"][0][x][y - 1], 1)
                if ( valueAbove == value and valueBelow == value ):      # Same above and below: |
                    coords[1] = [round(longitude[x][y], 5), round(latitude[x][y], 5)]
                    coords[2] = [round(longitude[x][y+1], 5), round(latitude[x][y+1], 5)]
                elif (valueAbove == value and valueBelow != value):  # Same only above: \
                    coords[1] = [round(longitude[x + 1][y], 5), round(latitude[x + 1][y], 5)]
                    coords[2] = [round(longitude[x][y + 1], 5), round(latitude[x][y + 1], 5)]
                elif (valueAbove != value and valueBelow == value):  # Same only below: /
                    coords[1] = [round(longitude[x][y], 5), round(latitude[x][y], 5)]
                    coords[2] = [round(longitude[x + 1][y + 1], 5), round(latitude[x + 1][y + 1], 5)]
                elif (valueAbove != value and valueBelow != value):  # Both different (to do): |
                    coords[1] = [round(longitude[x][y], 5), round(latitude[x][y], 5)]
                    coords[2] = [round(longitude[x][y+1], 5), round(latitude[x][y+1], 5)]

            if ( startValue != -9900000000000000):

                # Add polygon to the geojson if relevant aka != -9900000000000000
                polygon = {
                    "type": "Feature",
                    "properties": {magDict[mag] + "_00001": startValue},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coords]
                    }
                }
                geojs["features"].append(polygon);

            # We set the start of the next polygon as the current value
            polygonStartX = x
            startValue = round(magnitude[magDict[mag] + "_00001"][0][x][y], 1)
            coords = [None, None, None, None, None]
            continue


    #print("Exporting Data to JSON");

    with open(OUTPUT, 'w') as outfile:
        json.dump(geojs, outfile)

    #print(geojs);

    #print("Exiting Program")

    end = time.time()
    #print("Script Execution: ",round(end - start, 2))


if __name__ == '__main__':
    mp.freeze_support()

    start = time.time()

    curveLine(17)
    '''
    try:
        mp.set_start_method('spawn')
        pool = mp.Pool(mp.cpu_count())
        # results = pool.map(line, range(0, GRID_X));
        results = pool.map(curveLine, range(0, 19))
    except Exception as e:
        print(e)
        # Logs the error appropriately.
    '''

    # print( results )
    # results = [pool.apply(line, args=(x, )) for x in range(0, GRID_X)]

    print("Exiting MP Program")

    end = time.time()
    print("Script Execution: ", round(end - start, 2))

#curveLine(17)
#multiProcessing()
