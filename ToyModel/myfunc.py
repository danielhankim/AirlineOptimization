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
            d = np.random.randint(low = 1, high = 11)
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

def make_undirected_graph_OR(origin, N):
    # make undirected graph based on "OR" rule
    undirected_graph = np.zeros((N, N), dtype = np.int64)

    for i in range(N):
        for j in range(i+1, N): # maybe I can modify this later! remove this tag after modification
            if origin[i][j] > 0 or origin[j][i] > 0:
                undirected_graph[i][j] = 1

    return undirected_graph

def make_undirected_graph_AND(origin, N):
    # make undirected graph based on "AND" rule
    undirected_graph = np.zeros((N, N), dtype = np.int64)

    for i in range(N):
        for j in range(i+1, N): # maybe I can modify this later! remove this tag after modification
            if origin[i][j] > 0 and origin[j][i] > 0:
                undirected_graph[i][j] = 1

    return undirected_graph

def extract_connected_component(undirected_graph):
    G = nx.Graph(undirected_graph)

    list_of_component_size = [len(c) for c in sorted(nx.connected_components(G), 
                                key = len, reverse = True)]

    return list_of_component_size

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



def new_booking_dynamics(demand_list, airline_network, distance_matrix):

    rows, cols = airline_network.shape
    N = rows
    # failure_matrix = np.zeros((N, N), dtype = np.int64)
    m = len(demand_list)
    n_satisfied = 0
    n_unsatisfied = 0
    tot_dist = 0
    tot_hop = 0
    path_memory = {}

    
    while m > 0:
        # print(f'm = {m}')
        simple_graph = make_simple_graph(airline_network, N)
        G = nx.DiGraph(simple_graph)

        ### Choose OD
        ### We can change this stochastically when we deal with real demand lists
        o, d = demand_list[m-1]


        ### Check if we have avialable path used before
        if (o, d) not in path_memory:
            ### If there is no path used before, we can find them
            # print(f'no path memory for (o,d)={o, d}')
            path_memory[(o, d)] = []
            
            try:
                path_memory[(o, d)] = [p for p in nx.all_shortest_paths(G, source = o, target = d)]
                # path_memory[(o, d)].append(paths)

            except:
                pass
                # n_unsatisfied += 1
                # failure_matrix[o][d] += 1

        else: 
            ### If we haved used them before, we can figure out
            ### whether we can use them again!
            ### Still needs to be modified i guess...

            check_missing = [0 for i in range(len(path_memory[(o, d)]))]
            for i in range(len(path_memory[(o, d)])):
                for j in range(len(path_memory[(o, d)][i]) - 1):
                    I1 = path_memory[(o, d)][i][j]
                    I2 = path_memory[(o, d)][i][j+1]

                    if G.has_edge(I1, I2) == False:
                        check_missing[i] = -1
                        break

            new_path = []
            for i in range(len(path_memory[(o, d)])):
                if check_missing[i] == 0:
                    new_path.append(path_memory[(o, d)][i])
            path_memory[(o, d)] = new_path

        # print(f'chosen path:{path_memory[(o, d)]}')

        ### Now let's try to make a trip
        if len(path_memory[(o, d)]) > 0:

            r = np.random.randint(len(path_memory[(o, d)]))

            # print(f'chosen path:{path_memory[(o, d)][r]}')

            for u in range(len(path_memory[(o, d)][r]) - 1):
                I1 = path_memory[(o, d)][r][u]
                I2 = path_memory[(o, d)][r][u + 1]
                airline_network[I1][I2] -= 1
                tot_dist += distance_matrix[I1][I2]
                
            
            n_satisfied += 1
            tot_hop += (len(path_memory[(o, d)][r]) - 1)


        else:

            n_unsatisfied += 1
            # failure_matrix[o][d] += 1

        m -= 1

    n_empty = np.sum(np.ndarray.flatten(airline_network))


    return n_satisfied, n_unsatisfied, n_empty, tot_dist, tot_hop, airline_network



