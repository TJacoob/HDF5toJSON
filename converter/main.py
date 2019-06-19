import multiprocessing as mp
import time
import traceback

from converter import converter
from config import *
import domains

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
    DOMAIN = getattr(domains, CONF_DOMAIN)
    print("Current Domain is: "+DOMAIN['name'])

    # Get and print list of all the available variables for the domain
    magnitudes = []
    print("Available Magnitudes: ", end='')
    for m in DOMAIN['magnitudes']:
        magnitudes.append((DOMAIN['name'],m))
        print(m+",", end='')
    print("")

    try:

        if CONF_MULTIPROCESSING:
            mp.set_start_method('spawn')
            pool = mp.Pool(mp.cpu_count()-1)
            results = pool.map(converter, magnitudes)
        else:
            converter((DOMAIN['name'],CONF_MAGNITUDE))

    except Exception as e:
        tb = traceback.format_exc()

    else:
        tb = "Successfully Executed"
    finally:
        print(tb)

    end = time.time()
    print("Elapsed time: ", round(end - start, 2))