import myfunc
import os
import numpy as np
import sys

#################
# Parameters 
#################

SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/Sym_Airline/'
SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/Test/'



n_sample = 1000
# N = 100
N_list = [200]
#P_list = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
c = 1
#m = int(sys.argv[1])
m=400
#P = 4000
P = int(sys.argv[1])

for N in N_list:
    print(f"N = {N}\n")
    print(f"P = {P}\n")
    # list_of_satisfied = []
    # list_of_unsatisfied = []
    # list_of_wasted = []
    # list_of_distance = []
    # list_of_hop = []
    for i in range(n_sample):


        demand_list = myfunc.make_demand_list(N, m)
        distance_matrix = myfunc.make_distance_matrix(N)
        airline_nw = myfunc.make_airline_network(N, P, c, Symmetry = True)

        n_satisfied, n_unsatisfied, n_empty, tot_dist, tot_hop, remnant_network = \
        myfunc.new_booking_dynamics(demand_list, airline_nw, distance_matrix)

        #######################################################
        #
        # remnant of airline network -> undirected graph
        #
        #######################################################
        undirected_graph1 = myfunc.make_undirected_graph_OR(remnant_network, N)
        undirected_graph2 = myfunc.make_undirected_graph_AND(remnant_network, N)

        #######################################################
        #
        # undirected graph -> size of connected components
        #
        #######################################################
        connected_component1 = myfunc.extract_connected_component(undirected_graph1)
        connected_component2 = myfunc.extract_connected_component(undirected_graph2)

        largest_size1 = np.max(connected_component1)
        largest_size2 = np.max(connected_component2)

        connected_component1.remove(largest_size1)
        connected_component2.remove(largest_size2)

        with open(SAVE_PATH + f"Satisfied_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %n_satisfied)
        
        with open(SAVE_PATH + f"Unsatisfied_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %n_unsatisfied)

        with open(SAVE_PATH + f"Wasted_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %n_empty)

        with open(SAVE_PATH + f"Distance_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %tot_dist)

        with open(SAVE_PATH + f"Hop_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %tot_hop)

        with open(SAVE_PATH + f"S1_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %largest_size1)

        with open(SAVE_PATH + f"S2_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %largest_size2)

        with open(SAVE_PATH + f"finite_component1_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in connected_component1:
                f.write("%d\n" %x)

        with open(SAVE_PATH + f"finite_component2_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in connected_component2:
                f.write("%d\n" %x)
        
        

        if n_empty < 0:
            sys.exit(f'n_empty = {n_empty}!!!!!')


    # with open(SAVE_PATH + f"Satisfied_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    #     for x in list_of_satisfied:
    #         f.write("%d\n" %x)
        
    # with open(SAVE_PATH + f"Unsatisfied_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    #     for x in list_of_unsatisfied:
    #         f.write("%d\n" %x)

    # with open(SAVE_PATH + f"Wasted_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    #     for x in list_of_wasted:
    #         f.write("%d\n" %x)

    # with open(SAVE_PATH + f"Distance_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    #     for x in list_of_distance:
    #         f.write("%d\n" %x)

    # with open(SAVE_PATH + f"Hop_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
    #     for x in list_of_hop:
    #         f.write("%d\n" %x)

