import h5py
import simplejson as json
import os

from config import *

'''
This function must receive a tuple of strings corresponding to:
    domain: name of the domain to dynamically load its info
    magnitude: the magnitude that will be computed and outputed

The function then opens and reads the file configured and
performs necessary computations to output the geoJson file
'''
def areaConverter(args):

    # Load requested domain and magnitude info
    DOMAIN = args[0]
    with open('magnitudes.json') as f:
        magnitudes = json.load(f)
    MAGNITUDE = magnitudes[(args[1].replace(" ", "_")).upper()]
    TIMEFRAME = args[2]

    # Scale values for the value mapper (check valueMapper)
    magScaleMin = MAGNITUDE["minValue"]
    magScaleMax = MAGNITUDE["maxValue"]

    # Open File using h5py Library
    '''
    data = h5py.File(CONF_INPUTDATA, 'r')
    print(data['results']);
    '''
    alldata = []
    # Open Files using h5py Library
    for file in CONF_INPUTDATA:
        alldata.append(h5py.File(file, 'r'))

    # Select file with the magnitude desired
    data = []
    for f in alldata:
        if MAGNITUDE["hdfName"] in f['Results']:
            data = f
            break

    # Get data related to the required magnitude
    results = data['Results'][MAGNITUDE["hdfName"]][MAGNITUDE["hdfName"] + "_" + CONF_TIMEFRAME][0]

    # Create Structure of the geoJSON output
    geojs = {
        "type": "FeatureCollection",
        "features": []
    }

    # The first object of the feature collection can include
    # information about this domain
    # Disabled for now
    '''
    if CONF_ADDDOMAININFO:
        domain_info = {
            "type": "Feature",
            "properties": {
                "name": DOMAIN["name"],
                "magnitude": MAGNITUDE["hdfName"],
                "time": timestamp,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": DOMAIN["coordinates"]
            }
        }
        geojs["features"].append(domain_info)
    '''

    # Copying Coordinates information to variables
    # reduces the number of accesses to the hdf files
    longitude = data['Grid']['Longitude']
    latitude = data['Grid']['Latitude']

    RANGEX = len(longitude)
    RANGEY = len(longitude[0])

    # To compress data we round every magnitude to a smaller value
    # This creates less polygons because the values are closer to each other
    # Magnitudes might need lose info if rounded too much, so this is a setting for each
    # Coordinates are always rounded to their own setting ( 4 or 5 )
    #magRound = int(MAGNITUDE['rounding'])
    coordRound = CONF_COORDINATEROUNDING

    # Iterate rows
    for y in range(0, RANGEY-2):

        # Initial row configurations
        startValue = valueMapper(results[0][y], magScaleMin, magScaleMax, MAGNITUDE)
        polygonStartX = 0
        coords = [None, None, None, None, None]

        # Iterate columns (-1 because the next square is used for computations)
        for x in range(0, RANGEX-1):
            value = valueMapper(results[x][y], magScaleMin, magScaleMax, MAGNITUDE)

            if ( value == startValue and x!= RANGEX-2):
                continue

            # If the value is different from the previous cell than the polygon is over
            # Now we should check the first and last cells for adjustments
            # The adjustments check the adjacent cells to decide the shape it should take

            # These adjustments use the cells above and below to decide, so they don't work on the first and last column
            if (y == 0 or y == RANGEY-2):
                continue

            else:
                # Check above and below for the first cell (left):
                valueAbove = valueMapper(results[polygonStartX][y+1], magScaleMin, magScaleMax, MAGNITUDE)
                valueBelow = valueMapper(results[polygonStartX][y-1], magScaleMin, magScaleMax, MAGNITUDE)

                # Same above and below: |
                if ( valueAbove == startValue and valueBelow == startValue ):
                    coords[0] = [round(longitude[polygonStartX][y],coordRound), round(latitude[polygonStartX][y], coordRound)]
                    coords[3] = [round(longitude[polygonStartX][y+1], coordRound), round(latitude[polygonStartX][y+1], coordRound)]

                # Same only above: \
                elif (valueAbove == startValue and valueBelow != startValue):
                    coords[0] = [round(longitude[polygonStartX + 1][y], coordRound), round(latitude[polygonStartX + 1][y], coordRound)]
                    coords[3] = [round(longitude[polygonStartX][y + 1], coordRound), round(latitude[polygonStartX][y + 1], coordRound)]

                # Same only below: /
                elif (valueAbove != startValue and valueBelow == startValue):
                    coords[0] = [round(longitude[polygonStartX][y], coordRound), round(latitude[polygonStartX][y], coordRound)]
                    coords[3] = [round(longitude[polygonStartX+1][y+1],coordRound),round(latitude[polygonStartX + 1][y+1],coordRound)]

                # Both different (can be improved): |
                elif (valueAbove != startValue and valueBelow != startValue):
                    coords[0] = [round(longitude[polygonStartX][y], coordRound), round(latitude[polygonStartX][y], coordRound)]
                    coords[3] = [round(longitude[polygonStartX][y+1], coordRound), round(latitude[polygonStartX][y+1], coordRound)]

                # First and last coords must be the same to close the polygon
                # This way we don't read the same value twice, (slightly) improving performance
                coords[4] = coords[0]

                # Check above and below for the last cell (right):
                valueAbove = valueMapper(results[x][y + 1], magScaleMin, magScaleMax, MAGNITUDE)
                valueBelow = valueMapper(results[x][y - 1], magScaleMin, magScaleMax, MAGNITUDE)

                # Same above and below: |
                if ( valueAbove == value and valueBelow == value ):
                    coords[1] = [round(longitude[x][y], coordRound), round(latitude[x][y], coordRound)]
                    coords[2] = [round(longitude[x][y+1], coordRound), round(latitude[x][y+1], coordRound)]

                # Same only above: \
                elif (valueAbove == value and valueBelow != value):
                    coords[1] = [round(longitude[x + 1][y], coordRound), round(latitude[x + 1][y], coordRound)]
                    coords[2] = [round(longitude[x][y + 1], coordRound), round(latitude[x][y + 1], coordRound)]

                # Same only below: /
                elif (valueAbove != value and valueBelow == value):
                    coords[1] = [round(longitude[x][y], coordRound), round(latitude[x][y], coordRound)]
                    coords[2] = [round(longitude[x + 1][y + 1], coordRound), round(latitude[x + 1][y + 1], coordRound)]

                # Both different (to do): |
                elif (valueAbove != value and valueBelow != value):
                    coords[1] = [round(longitude[x][y], coordRound), round(latitude[x][y], coordRound)]
                    coords[2] = [round(longitude[x][y+1], coordRound), round(latitude[x][y+1], coordRound)]

            # At this points, we have the coordinates for the polygon
            # So we need to write the polygon to the GeoJSON object

            if ( startValue != -9900000000000000):

                # Add polygon to the geojson if relevant aka != -9900000000000000
                polygon = {
                    "type": "Feature",
                    "properties": {MAGNITUDE["hdfName"]: startValue},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coords]
                    }
                }
                geojs["features"].append(polygon)

            # After writing the polygon to the object
            # We set the start of the next polygon as the current value
            polygonStartX = x
            startValue = valueMapper(results[x][y], magScaleMin, magScaleMax, MAGNITUDE)
            coords = [None, None, None, None, None]
            continue

    # Get time information of the data, to use in the output name
    time = data['Time']['Time_' + TIMEFRAME]
    #timestamp = str(int(time[0])) + "-" + str(int(time[1])) + "-" + str(int(time[2])) + "_" + str(int(time[3])) + ":" + str(int(time[4])) + ":" + str(int(time[5]))

    # Saving the json file with the converted data
    # Creates a folder for the domain and a folder inside with the date
    outputFolder = "../testFiles/"+DOMAIN['name']+"/"+str(int(time[0]))+"-"+str(int(time[1]))+"-"+str(int(time[2]))
    outputName = MAGNITUDE["hdfName"]+"_"+str(int(time[3]))+":"+str(int(time[4]))+":"+str(int(time[5]))+".json"
    os.makedirs(outputFolder, exist_ok=True)

    with open(outputFolder+"/"+outputName, 'w') as outfile:
        json.dump(geojs, outfile)



def vectorConverter(args):
    # Load requested domain and magnitude info
    DOMAIN = args[0]
    with open('magnitudes.json') as f:
        magnitudes = json.load(f)
    MAGNITUDE = magnitudes[(args[1].replace(" ", "_")).upper()]
    TIMEFRAME = args[2]

    # Scale values for the value mapper (check valueMapper)
    magScaleMin = MAGNITUDE["minValue"]
    magScaleMax = MAGNITUDE["maxValue"]

    # Open File using h5py Library
    '''
    data = h5py.File(CONF_INPUTDATA, 'r')
    print(data['results']);
    '''
    alldata = []
    # Open Files using h5py Library
    for file in CONF_INPUTDATA:
        alldata.append(h5py.File(file, 'r'))

    # Select file with the magnitudes desired
    dataX = []
    for f in alldata:
        if MAGNITUDE["hdfName"][0] in f['Results']:
            dataX = f
            break

    dataY = []
    for f in alldata:
        if MAGNITUDE["hdfName"][1] in f['Results']:
            dataY = f
            break

    # Get data related to the required magnitude
    resultsX = dataX['Results'][MAGNITUDE["hdfName"][0]][MAGNITUDE["hdfName"][0] + "_" + CONF_TIMEFRAME][0]
    #print(resultsX)
    resultsY = dataY['Results'][MAGNITUDE["hdfName"][1]][MAGNITUDE["hdfName"][1] + "_" + CONF_TIMEFRAME][0]
    #print(resultsY)

    # Create Structure of the geoJSON output
    geojs = {
        "type": "FeatureCollection",
        "features": []
    }

    # The first object of the feature collection can include
    # information about this domain
    # Disabled for now
    '''
    if CONF_ADDDOMAININFO:
        domain_info = {
            "type": "Feature",
            "properties": {
                "name": DOMAIN["name"],
                "magnitude": MAGNITUDE["hdfName"],
                "time": timestamp,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": DOMAIN["coordinates"]
            }
        }
        geojs["features"].append(domain_info)
    '''

    # Copying Coordinates information to variables
    # reduces the number of accesses to the hdf files
    longitude = dataX['Grid']['Longitude']
    latitude = dataX['Grid']['Latitude']

    RANGEX = len(longitude)
    RANGEY = len(longitude[0])

    # To compress data we round every magnitude to a smaller value
    # This creates less polygons because the values are closer to each other
    # Magnitudes might need lose info if rounded too much, so this is a setting for each
    # Coordinates are always rounded to their own setting ( 4 or 5 )
    # magRound = int(MAGNITUDE['rounding'])
    coordRound = CONF_COORDINATEROUNDING


    # Iterate Rows make calculations and get results



    # Get time information of the data, to use in the output name
    time = dataX['Time']['Time_' + TIMEFRAME]
    # timestamp = str(int(time[0])) + "-" + str(int(time[1])) + "-" + str(int(time[2])) + "_" + str(int(time[3])) + ":" + str(int(time[4])) + ":" + str(int(time[5]))

    # Saving the json file with the converted data
    # Creates a folder for the domain and a folder inside with the date
    outputFolder = "../testFiles/" + DOMAIN['name'] + "/" + str(int(time[0])) + "-" + str(int(time[1])) + "-" + str(
        int(time[2]))
    outputName = MAGNITUDE["name"] + "_" + str(int(time[3])) + ":" + str(int(time[4])) + ":" + str(
        int(time[5])) + ".json"
    os.makedirs(outputFolder, exist_ok=True)

    with open(outputFolder + "/" + outputName, 'w') as outfile:
        json.dump(geojs, outfile)


'''
This function maps values from a scale to another
Its used to "hide" the real value of a magnitude
We change it from its magnitude scale to a scale from 0 to 10 or 20
This way the visualization knows it only needs to match this value
to its own scale (index) of colors.
The return is always an int between the scale configured (CONF_MAXSCALE, CONF_MINSCALE)
This function can be disabled and configured in the config file (CONF_USESCALE)

It uses the following arguments:
    value: the original value
    minExist: the lower end of the magnitude scale
    maxExist: the higher end of the magnitude scale
'''
def valueMapper(value, minExist, maxExist, magnitude):

    if not CONF_USESCALE:
        return value

    minTarget = 0
    maxTarget = len(magnitude["colorScale"]) - 1
    # minTarget = CONF_MINSCALE
    # maxTarget = CONF_MAXSCALE

    # Useless values remain unchanged
    # Some domains use -9900000 for land, while others use 0
    # It isn't usual for a magnitude to take a value of EXACTLY zero, so we use it as a filter
    if value == -9900000000000000 or value == 0:
        return -9900000000000000

    value = round(value, int(magnitude['rounding']))

    return int(minTarget + (((value-minExist)*(maxTarget-minTarget))/(maxExist-minExist)))