import myfunc
import numpy as np
import time


SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/Complexity/'

n_experiment = 1000
N = 400
c = 1
m = 1600
P = 40000
# P = int(sys.argv[1])



naive_implementation_time = []
modified_algorithm_time = []

for i in range(n_experiment):

    np.random.seed(i)

    start = time.time()
    demand_list = myfunc.make_demand_list(N, m)
    distance_matrix = myfunc.make_distance_matrix(N)
    airline_nw = myfunc.make_airline_network(N, P, c, Symmetry = True)

    _, _, _, _, _, _ = myfunc.new_booking_dynamics(demand_list, 
                                                    airline_nw, 
                                                    distance_matrix)
    end = time.time()

    modified_algorithm_time.append(end - start)




    np.random.seed(i)

    start = time.time()
    demand_list = myfunc.make_demand_list(N, m)
    distance_matrix = myfunc.make_distance_matrix(N)
    airline_nw = myfunc.make_airline_network(N, P, c, Symmetry = True)

    _, _, _, _, _, _ = myfunc.booking_dynamics(demand_list, 
                                                airline_nw, 
                                                distance_matrix)
    end = time.time()

    naive_implementation_time.append(end - start)



with open(SAVE_PATH + f"Naive_complexity_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    for x in naive_implementation_time:
        f.write("%f\n" %x)

with open(SAVE_PATH + f"NewAlg_complexity_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    for x in modified_algorithm_time:
        f.write("%f\n" %x)
