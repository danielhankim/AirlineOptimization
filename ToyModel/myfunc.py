import numpy as np
import networkx as nx
# import matplotlib.pyplot as plt

def make_demand_list(N, m, Symmetry = False):

    demand = []

    if Symmetry == True:
        while m > 0:
            i, j = np.random.randint(N, size = 2)
            if i != j:
                demand.append(list([i, j]))
                demand.append(list([j, i]))
                m -= 2
    else:
        while m > 0:
            i, j = np.random.randint(N, size = 2)
            if i != j:
                demand.append(list([i, j]))
                m -= 1
    return demand

def make_airline_network(N, P, c, Symmetry = False):

    airline_nw = np.zeros((N, N), dtype = np.int64)

    if Symmetry == True:
        while P > 0:
            i, j = np.random.randint(N, size = 2)
            if i != j:
                airline_nw[i][j] += c 
                airline_nw[j][i] += c
                P -= 2
    
    else:
        while P > 0:
            i, j = np.random.randint(N, size = 2)
            if i != j:
                airline_nw[i][j] += c 
                P -= 1

    return airline_nw
    

def make_distance_matrix(N):

    distance_matrix = np.zeros((N, N), dtype = np.int64)

    for i in range(N):
        for j in range(i+1, N):
            d = np.random.randint(10)
            distance_matrix[i][j] = d
            distance_matrix[j][i] = d
 
    return distance_matrix


def make_simple_graph(origin, N):

    simple_graph = np.zeros((N, N), dtype = np.int64)

    for i in range(N):
        for j in range(N):
            if origin[i][j] > 0:
                simple_graph[i][j] = 1
                # simple_graph[j][i] = 1

    return simple_graph

def booking_dynamics(demand_list, airline_network, distance_matrix):

    rows, cols = airline_network.shape
    N = rows
    failure_matrix = np.zeros((N, N), dtype = np.int64)
    m = len(demand_list)
    n_satisfied = 0
    n_unsatisfied = 0
    tot_dist = 0
    tot_hop = 0

    i = 0
    while m > 0:
    
        simple_graph = make_simple_graph(airline_network, N)
        G = nx.DiGraph(simple_graph)

        ### setp 1: we randomly select a passenger's demand
        # while True:
        #     o, d = np.random.randint(N, size = 2)
        #     if demand_matrix[o][d] > 0:
        #         demand_matrix[o][d] -= 1
        #         break
        o, d = demand_list[i]
        i += 1

        ### step 2: we find available shortest pathes which satisfies the demand
        try:
            ### if there is at least one path, let's make a trip :)
            s_paths = [p for p in nx.all_shortest_paths(G, source = o, target = d)]
            n_path = len(s_paths)
            r = np.random.randint(n_path)
            for u in range(len(s_paths[r]) - 1):
                midpoint1 = s_paths[r][u]
                midpoint2 = s_paths[r][u + 1]
                airline_network[midpoint1][midpoint2] -= 1
                tot_dist += distance_matrix[midpoint1][midpoint2]
                #################################################
                # should think about a better distance measure
                #################################################
            n_satisfied += 1
            tot_hop += (len(s_paths[r]) - 1)

        except:
            ### if there is no path, the passenger cannot make a trip :(
            n_unsatisfied += 1
            failure_matrix[o][d] += 1
        m -= 1

    n_empty = np.sum(np.ndarray.flatten(airline_network))

    return n_satisfied, n_unsatisfied, n_empty, tot_dist, failure_matrix, tot_hop
