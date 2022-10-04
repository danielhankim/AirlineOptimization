import myfunc
import os
import sys

#################
# Parameters 
#################

SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/Sym_Airline/'

n_sample = 50
N = 100
N_list = [100, 200, 400]
P_list = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
c = 20
m = 8000

for N in N_list:
    for P in P_list:
        print(f"P = {P}")
        list_of_satisfied = []
        list_of_unsatisfied = []
        list_of_wasted = []
        list_of_distance = []
        for i in range(n_sample):
            demand_matrix = myfunc.make_demand_matrix(N, m)
            distance_matrix = myfunc.make_distance_matrix(N)
            airline_nw = myfunc.make_airline_network(N, P, c, Symmetry = True)

            n_satisfied, n_unsatisfied, n_empty, tot_dist, failure_matrix = \
            myfunc.booking_dynamics(demand_matrix, airline_nw, distance_matrix)

            list_of_satisfied.append(n_satisfied)
            list_of_unsatisfied.append(n_unsatisfied)
            list_of_wasted.append(n_empty)
            list_of_distance.append(tot_dist)
            if n_empty < 0:
                # print(f'n_empty = {n_empty}!!!!!')
                sys.exit(f'n_empty = {n_empty}!!!!!')
            # if i % 100 == 0:
            #     print(f"{i}/{n_sample} done...")


        with open(SAVE_PATH + f"Satisfied_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in list_of_satisfied:
                f.write("%d\n" %x)
            
        with open(SAVE_PATH + f"Unsatisfied_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in list_of_unsatisfied:
                f.write("%d\n" %x)

        with open(SAVE_PATH + f"Wasted_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in list_of_wasted:
                f.write("%d\n" %x)

        with open(SAVE_PATH + f"Distance_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in list_of_distance:
                f.write("%d\n" %x)


