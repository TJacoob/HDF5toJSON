# IMPORTS
import h5py
import simplejson as json

from decimal import Decimal

import time

import multiprocessing as mp
#from mpi4py import MPI

# SETTINGS
INPUT = 'testFiles/WaterProperties.hdf5'
OUTPUT = 'testFiles/newdata.json'

# Variables
dataset = []
#start = 0;

def convertor():
    global dataset
    #global start

    start = time.time()
    # Reads the HDF5 File and stores data in a global variable so every function can access it
    dataset = h5py.File(INPUT, 'r')

    print(dataset)

    geojs = {
        "type": "FeatureCollection",
        "features": []
    };

    #rank = MPI.COMM_WORLD.rank
    #print(rank)

    for x in range(0,20):
        #start = time.time()
        line = test(x)
        geojs['features'].append(line)
        #end = time.time()
        #print("Time per Line: ", round(end - start, 2))

    #out = test(0)

    #pool = mp.Pool(processes=4)
    #results = pool.map(test, range(1, 100))

    end = time.time()
    print("Time: ", round(end - start, 2))

    #print(results)


def test(x):
    global dataset

    line=[]

    for y in range(0, 20):
        cell = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[]]
            }
        }

        #print(dataset['Results'])


        for result in dataset['Results']:
            #print(result)
            series = dataset['Results'][result]


            for t in series:
                if (t[-5:] == "00001"):
                    cell['properties'][series.name[9:]] = json.dumps(round(Decimal(series[t][0][x][y]), 5))


        line.append(cell)

    return line

convertor()
