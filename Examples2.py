# HDF5 to JSON Converter

import h5py
#import json
from decimal import Decimal
import simplejson as json

import time

def main():
    #h5py.run_tests();
    start = time.time()
    print(start);

    geojs = {
        "type": "FeatureCollection",
        "features": []
    };

    f = h5py.File('testFiles/WaterProperties.hdf5', 'r')

    print("Collecting Data");

    # Setup
    longitude = f['Grid']['Longitude'];
    latitude = f['Grid']['Latitude'];

    results = f['Results'];

    for x in range(0,243):      # Should match the grid size
        for y in range(0,114):
            #print(x,y);
            unit = {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[]]
                }
            };

            # Grid
            coordinates = [
                [json.dumps(round(longitude[x][y],5)), json.dumps(round(latitude[x][y],5))],
                [json.dumps(round(longitude[x+1][y+1],5)), json.dumps(round(latitude[x][y],5))],
                [json.dumps(round(longitude[x+1][y+1],5)), json.dumps(round(latitude[x+1][y+1],5))],
                [json.dumps(round(longitude[x][y],5)), json.dumps(round(latitude[x+1][y+1],5))],
                [json.dumps(round(longitude[x][y],5)), json.dumps(round(latitude[x][y],5))],
            ];
            unit['geometry']['coordinates'][0]=coordinates;

            #print(coordinates);

            # Annex Results
            for result in results:
                stat = f['Results'][result];
                #print(stat.name);
                #unit['properties'][stat.name[9:]]=0;
                #print(stat);
                for t in stat:
                    #print(stat[t]);
                    if ( t[-5:] == "00001"):    # Only reading the first time entry (checks last 5 digits of the name)
                        #print(round(Decimal(stat[t][0][x][y]),5));
                        #unit['properties'][stat.name[9:]] = round(Decimal(stat[t][0][x][y]),5);   # Copies the value of the stat for this coordinate
                        #unit['properties'][stat.name[9:]] = stat[t][0][x][y];
                        unit['properties'][stat.name[9:]] = json.dumps(round(Decimal(stat[t][0][x][y]), 5));

            # Unit is Ready, annexing to the geojs
            geojs['features'].append(unit);


    print("Exporting Data to JSON");

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    #print(geojs);

    print("Exiting Program")

    end = time.time()
    print(end - start)

main()
