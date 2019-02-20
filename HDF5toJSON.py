# HDF5 to JSON Converter

import h5py
import json

def all(name):
    return True;

def main():
    #h5py.run_tests();

    f = h5py.File('testFiles/WaterProperties.hdf5', 'r')

    print("Collecting Data");
    # Grid Information Handling
    latitude = f['Grid']['Latitude'];
    longitude = f['Grid']['Longitude'];
    grid = [];
    for x in latitude:
        yArray = [];
        for y in x:
            #print(y);
            yArray.append(y);
        grid.append(yArray);
    #print(grid);


    # Time Information Handling
    dates = f['Time'];
    allDates = [];
    for date in dates:
        current = f['Time'][date];
        #Should add an ISO 8601 format option
        time = {
            "year": int(current[0]),
            "month": int(current[1]),
            "day": int(current[2]),
            "hour": int(current[3]),
            "minute": int(current[4]),
            "second": int(current[5])
        }
        allDates.append(time);


    # Results Tables Handling
    results = f['Results'];
    print(results);
    resultsData = {};
    for result in results :
        stat = f['Results'][result];
        print(stat.name);

        for t in stat:
            col = stat[t];
            #print(col);
            r = [];

            for x in col[0]:
                yArray = [];
                for y in x:
                    yArray.append(y);
                r.append(yArray);
        #print(r);
        resultsData[stat.name]=r;
    #print(resultsData);





    # JSON Object To Be Written
    print("Exporting Data to JSON");
    jsonData = {
        'Grid':grid,
        "Time":allDates,
        "Data":resultsData
    };

    with open('testFiles/data.json', 'w') as outfile:
        json.dump(jsonData, outfile)

    #print(jsonData);

    print("Exiting Program")


main()
