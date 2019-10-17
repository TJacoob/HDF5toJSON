import multiprocessing as mp
import time
import traceback

import simplejson as json
from config import *

from converter import areaConverter
from converter import vectorConverter

# -- MAIN PROGRAM --
# This program converts HDF5 files to GeoJSON format

# The algorithm reads rows of the HDF5 file, for each square
# it checks its value with the adjacent (->) square and if their
# values are similar joins them in a single GeoJSON polygon

# Adjustments are performed on the extremes of the polygon to adapt
# its shape to the shoreline of the maps in the domain of this work

# The goal of this program is to run regularly converting MARETEC models results
# into a readable format, ready to be applied to any web map visualization library

if __name__ == '__main__':

    mp.freeze_support()         #Necessary for execution on Windows Platforms

    print("Starting Execution")
    start = time.time()

    # Load the desired domain (as configured)
    #DOMAIN = getattr(domains, CONF_DOMAIN)
    #print("Current Domain is: "+DOMAIN['name'])
    DOMAIN = None

    with open('domains.json') as f:
        domains = json.load(f)

    with open('magnitudes.json') as f:
        MAGNITUDES = json.load(f)

    for type in domains:
        for domain in domains[type][0]["features"]:
            # In case the same feature has two domains (such as PCOMS and PCOMSv2), it needs treatment
            if isinstance(domain["properties"]['name'], list):
                for index, dom in enumerate(domain["properties"]['name']):
                    if dom == CONF_DOMAIN:
                        DOMAIN = domain
                        properties = {}
                        for property in domain["properties"]:
                            if isinstance(domain["properties"][property], list):
                                properties[property] = domain["properties"][property][index]
                            else:
                                properties[property] = domain["properties"][property]
                        DOMAIN["properties"] = properties
            else:
                if domain["properties"]["name"] == CONF_DOMAIN:
                    DOMAIN = domain

    print("Current Domain is: "+DOMAIN['properties']['name'])

    # Get and print list of all the available variables for the domain
    areaMagnitudes = []
    vectorMagnitudes = []
    availableVariables = DOMAIN['properties']['availableVariables']
    #print("Available Magnitudes: ", end='')
    for m in availableVariables :
        timebasis = int(DOMAIN["properties"]["timeHourBasis"])
        if MAGNITUDES[(m.replace(" ", "_")).upper()]['showTogether'] is not "":
            availableVariables.append(MAGNITUDES[(m.replace(" ", "_")).upper()]['showTogether'])
        if MAGNITUDES[(m.replace(" ", "_")).upper()]['vector'] is True:
            if CONF_ALLTIMEFRAMES:
                for timeframe in range(0, 24, timebasis):
                    vectorMagnitudes.append((DOMAIN['properties'], m, CONF_24HOURLIST[timeframe]))
            else:
                vectorMagnitudes.append((DOMAIN['properties'], m, CONF_TIMEFRAME))
        else:
            if CONF_ALLTIMEFRAMES:
                for timeframe in range(0, 24, timebasis):
                    areaMagnitudes.append((DOMAIN['properties'], m, CONF_24HOURLIST[timeframe]))
            else:
                areaMagnitudes.append((DOMAIN['properties'],m, CONF_TIMEFRAME))


        #print(m+", ", end='')
    #print("")

    # This process is done for area Magnitudes and repeated for Vector Magnitudes
    try:
        mp.set_start_method('spawn')
        pool = mp.Pool(mp.cpu_count() - 1)
        if CONF_MULTIPROCESSING:
            #print("AREA:")
            results = pool.map(areaConverter, areaMagnitudes)
            #print("VECTOR:")
            results = pool.map(vectorConverter, vectorMagnitudes)
        else:
            if CONF_ALLTIMEFRAMES:
                for timeframe in range(0, 24, timebasis):
                    if MAGNITUDES[CONF_MAGNITUDE]['vector']:
                        vectorConverter((DOMAIN['properties'], CONF_MAGNITUDE, CONF_24HOURLIST[timeframe]))
                    else:
                        areaConverter((DOMAIN['properties'],CONF_MAGNITUDE, CONF_24HOURLIST[timeframe]))
            else:
                if MAGNITUDES[CONF_MAGNITUDE]['vector']:
                    vectorConverter((DOMAIN['properties'], CONF_MAGNITUDE, CONF_TIMEFRAME))
                else:
                    areaConverter((DOMAIN['properties'],CONF_MAGNITUDE, CONF_TIMEFRAME))

    except Exception as e:
        tb = traceback.format_exc()

    else:
        tb = "Successfully Executed"
    finally:
        print(tb)

    end = time.time()
    print("Elapsed time: ", round(end - start, 2))