import multiprocessing as mp
import time

from converter import converter

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

    

    end = time.time()
    print("Finished Execution")
    print("Elapsed time: ", round(end - start, 2))