import myfunc
import os
import numpy as np
import sys
import networkx as nx

#################
# Parameters 
#################

# SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/Sym_Airline/'
SAVE_PATH = '/home/mk139/WorkSpace/AirlineNW/SaveData/ToyModel/Experiment/'



n_sample = 1000
# N = 100
N_list = [200]
#P_list = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
c = 1
#m = int(sys.argv[1])
m = 400
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

        ########################################################################
        # Extract original network structure
        ########################################################################

        simple_graph = myfunc.make_simple_graph(airline_nw, N)
        G = nx.Graph(simple_graph)
        connected_component = [len(c) for c in sorted(
                            nx.connected_components(G), 
                            key = len, 
                            reverse = True)]

        largest_cc = np.max(connected_component)
        connected_component.remove(largest_cc)
        ########################################################################


        n_satisfied, n_unsatisfied, n_empty, tot_dist, tot_hop, remnant_network = \
        myfunc.new_booking_dynamics(demand_list, airline_nw, distance_matrix)

        remnant_network = myfunc.make_simple_graph(remnant_network)
        G = nx.Digraph(remnant_network)

        weakly_connected = [len(c) for c in sorted(
                            nx.weakly_connected_components(G), 
                            key = len, 
                            reverse = True)]
        strongly_connected = [len(c) for c in sorted(
                            nx.strongly_connected_components(G), 
                            key = len, 
                            reverse = True)]



        largest_wcc = np.max(weakly_connected)
        largest_scc = np.max(strongly_connected)

        weakly_connected.remove(largest_wcc)
        strongly_connected.remove(largest_scc)

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

        with open(SAVE_PATH + f"Largest_cc_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %largest_cc)

        with open(SAVE_PATH + f"Largest_wcc_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %largest_wcc)

        with open(SAVE_PATH + f"Largest_scc_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            f.write("%d\n" %largest_scc)

        with open(SAVE_PATH + f"Finite_cc_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in connected_component:
                f.write("%d\n" %x)

        with open(SAVE_PATH + f"Finite_wcc_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in weakly_connected:
                f.write("%d\n" %x)

        with open(SAVE_PATH + f"Finite_scc_N{N}_P{P}_c{c}_m{m}.dat", "a") as f:
            for x in strongly_connected:
                f.write("%d\n" %x)
        
        
        if n_empty < 0:
            sys.exit(f'n_empty = {n_empty}!!!!!')




