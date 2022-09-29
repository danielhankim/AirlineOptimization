import myfunc
import os

#################
# Parameters 
#################

SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/'

n_sample = 500
N = 100
P_list = [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800]
c = 20
m = 8000


for P in P_list:
    print(f"P = {P}")
    list_of_satisfied = []
    list_of_unsatisfied = []
    list_of_wasted = []
    list_of_distance = []
    for i in range(n_sample):
        demand_matrix = myfunc.make_demand_matrix(N, m)
        distance_matrix = myfunc.make_distance_matrix(N)
        airline_nw = my_func.make_airline_network(N, P, c)

        n_satisfied, n_unsatisfied, n_empty, tot_dist, failure_matrix = \
        my_func.booking_dynamics(demand_matrix, airline_nw, distance_matrix)

        list_of_satisfied.append(n_satisfied)
        list_of_unsatisfied.append(n_unsatisfied)
        list_of_wasted.append(n_empty)
        list_of_distance.append(tot_dist)

        if i % 100 == 0:
            print(f"{i}/{n_sample} done...")


    with open(SAVE_PATH + f"Satisfied_N{N}_P{P}_c{c}_m{m}.dat") as f:
        for x in list_of_satisfied:
            f.write("%d\n" %x)
        
    with open(SAVE_PATH + f"Unsatisfied_N{N}_P{P}_c{c}_m{m}.dat") as f:
        for x in list_of_unsatisfied:
            f.write("%d\n" %x)

    with open(SAVE_PATH + f"Wasted_N{N}_P{P}_c{c}_m{m}.dat") as f:
        for x in list_of_wasted:
            f.write("%d\n" %x)

    with open(SAVE_PATH + f"Distance_N{N}_P{P}_c{c}_m{m}.dat") as f:
        for x in list_of_distance:
            f.write("%d\n" %x)


