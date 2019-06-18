import h5py

import time

def main():
    print("Starting Script")
    start = time.time()

    f = h5py.File('testFiles/WaterProperties.hdf5', 'r')
    print(f['Grid'])

    print("Finished Script")
    end = time.time() - start
    print("Execution time: ", end)

main()