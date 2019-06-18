#MultiProcessing Based on Spliting the Results datasets, instead of the coordinates

import h5py
import simplejson as json

import multiprocessing as mp

import time

def convertor():

    print("Starting Script")
    start = time.time()

    magnitudes = {0:"ammonia", 1:"cohesive sediment", 2:"density", 3:"dissolved non-refractory organic nitrogen"}

    geojs = {
        "type": "FeatureCollection",
        "features": []
    };

    f = h5py.File('testFiles/WaterProperties.hdf5', 'r')

    for x in range(0,1):
        for y in range(0,1):
            cell = {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[]]
                }
            };

            print(f['Results'].items())

            # Unit is Ready, annexing to the geojs
            geojs['features'].append(cell)


convertor()