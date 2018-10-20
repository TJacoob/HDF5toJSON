# HDF5 to JSON Example1

import h5py
import json

def example1():
    #h5py.run_tests();

    f = h5py.File('testFiles/WaterProperties.hdf5', 'r')

    ammonia_group = f['Results']['ammonia'];
    print(ammonia_group);

    ammonia = f['Results']['ammonia']['ammonia_00001']
    print(ammonia[0][0][0]);


    # Saving the data in a JSON Format
    data = {};
    data['ammonia'] = [ammonia[0][0][0]];
    with open('testFiles/data.txt', 'w') as outfile:
        json.dump(data, outfile)

    print("Exiting Program")


example1();
