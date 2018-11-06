# HDF5 to JSON Converter

import h5py
import json

def main():
    #h5py.run_tests();

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

    for x in range(0,115):      # Should match the grid size
        for y in range(0,115):
            print(x,y);
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
                [longitude[x][y], latitude[x][y]],
                [longitude[x+1][y+1], latitude[x][y]],
                [longitude[x+1][y+1], latitude[x+1][y+1]],
                [longitude[x][y], latitude[x+1][y+1]],
                [longitude[x][y], latitude[x][y]],
            ];
            unit['geometry']['coordinates'][0]=coordinates;

            # Annex Results
            for result in results:
                stat = f['Results'][result];
                #print(stat.name);
                #unit['properties'][stat.name[9:]]=0;
                #print(stat);
                for t in stat:
                    if ( t[-5:] == "00001"):    # Only reading the first time entry
                        #print(stat[t][0][x][y]);
                        unit['properties'][stat.name[9:]] = stat[t][0][x][y];

            # Unit is Ready, annexing to the geojs
            geojs['features'].append(unit);


    print("Exporting Data to JSON");

    with open('testFiles/newdata.json', 'w') as outfile:
        json.dump(geojs, outfile)

    # print(jsonData);

    print("Exiting Program")




    '''
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
    
    '''


main()
