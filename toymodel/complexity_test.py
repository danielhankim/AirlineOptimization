import myfunc
import numpy as np
import time


SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/Complexity/'

n_experiment = 1000
N = 400
c = 1
m = 400
P = 4000




with open(SAVE_PATH + f"Naive_complexity_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    for x in naive_implementation_time:
        f.write("%f\n" %x)

with open(SAVE_PATH + f"NewAlg_complexity_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    for x in modified_algorithm_time:
        f.write("%f\n" %x)
