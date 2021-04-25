import time
import itertools
import multiprocessing

from scripts.algorithms.perlin import Noise

def genNoise(x, y):
    value = 0
    value += Noise(x * 0.005, y * 0.005) * 1.0
    value += Noise(x * 0.025, y * 0.025) * .5 
    value += Noise(x * 0.05, y * 0.05) * 0.25
    return value

def get_data(pos):
    n = genNoise(pos[0], pos[1])
    if n < -0.05:
        return "water"
    # n >= 0.65 and n < 0.7
    elif n < 0.0:
        return "l_water"
    # elif n >= 0.6 and n < 0.65:
    elif n < 0.05:
        return 'dirt'
    else:
        return 'grass'

def generate_map(tile_amount=650):
    tile = None
    map_data = []
    for i in range(tile_amount):
        map_data.append([])
        for j in range(tile_amount):
            # n = Noise(i*freq, j*freq) * amp
            n = genNoise(i,j)
            # if n >= 0.7 and n < 1.0:
            if n < -0.05:
                map_data[i].append('water')
            # n >= 0.65 and n < 0.7
            elif n < 0.0:
                map_data[i].append('l_water')
            # elif n >= 0.6 and n < 0.65:
            elif n < 0.05:
                map_data[i].append('dirt')
            else:
                map_data[i].append('grass')
            # convert to hex from string value

    return map_data

def generate_map_with_mpp(tile_amount = 650):
    i = range(650)
    paramlist = list(itertools.product(i,i))
    pool = multiprocessing.Pool(processes=8)
    return pool.map(get_data, paramlist)

if __name__ == "__main__":
    optimized = True
    if optimized:
        start = time.perf_counter()
        generate_map_with_mpp()
        finish = time.perf_counter()
    else:
        start = time.perf_counter()
        map = generate_map(650)
        finish = time.perf_counter()


    print("optimized: {1} - Time of execution {0} seconds".format(round(finish-start, 3), optimized))

    