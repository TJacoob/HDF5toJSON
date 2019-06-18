import multiprocessing as mp

def cube(x):
    print(x)
    return x

pool = mp.Pool(processes=4)
results = pool.map(cube, range(1,100000000))
print(results)