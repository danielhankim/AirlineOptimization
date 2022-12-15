import networkx as nx
import numpy as np
import os
import sys

DATA_ROOT = '/home/mk139/WorkSpace/AirlineNW/SaveData/'
DATA_PATH = os.path.join(DATA_ROOT, 'Shortest_Path_Percolation')

N = int(sys.argv[1])
k = int(sys.argv[2])
repeat = int(sys.argv[3])

for _ in range(repeat):

    p = k / N
    G = nx.erdos_renyi_graph(N, p)
    t = 0 
    n_removed = 0
    shortest_path_lengths = []

    while True:

        connected_component = [c for c in sorted(nx.connected_components(G),
                                                key = len, reverse = True)]
        connected_component_size = [len(c) for c in connected_component]
        finite_cluster_size = connected_component_size[1:]
        
        if len(finite_cluster_size) == 0:
                    finite_cluster_size.append(0)

        gcc_nodes = list(connected_component[0])

        if len(gcc_nodes) != np.max(connected_component_size):
            print("something wrong in computing gcc!")
            break

        FILE1 = f'Largest_cluster_size_ERN_N{N}_k{k}_t{t}.dat'
        FILE2 = f'Finite_cluster_size_ERN_N{N}_k{k}_t{t}.dat'
        FILE3 = f'Removed_link_ERN_N{N}_k{k}_t{t}.dat'

        with open(os.path.join(DATA_PATH, FILE1), 'a') as f:
            f.write("%d\n"%connected_component_size[0])

        with open(os.path.join(DATA_PATH, FILE2), 'a') as f:
            for c in finite_cluster_size:
                f.write("%d\n"%c)

        with open(os.path.join(DATA_PATH, FILE3), 'a') as f:
            f.write("%d\n"%n_removed)

        if connected_component_size[0] == 1:
            break

        o, d = np.random.choice(gcc_nodes, 2)

        shortest_paths = [p for p in nx.all_shortest_paths(G, source = o, 
                                                              target = d)]

        n_path = len(shortest_paths)
        r = np.random.randint(n_path)
        sp_length = len(shortest_paths[r]) - 1

        for u in range(sp_length):

            I1 = shortest_paths[r][u]
            I2 = shortest_paths[r][u + 1]
            G.remove_edge(I1, I2)

        t += 1
        shortest_path_lengths.append(sp_length)
        n_removed += (sp_length)