import numpy
import random
import networkx as nx
from experiment_utils import create_data_path_file, perform_experiment


# Watts-Strogatz experiments:
#     - n: size of graph
#     - k: number of ring neighbors
#     - p: rewiring probability
#     - r: fake-to-real edge proportion


# Experimental conditions
INTERVAL_NO = 10
MAX_N = 1000
MAX_F = 1.00


# Deltas
N_DELTA = MAX_N / INTERVAL_NO
F_DELTA = MAX_F / INTERVAL_NO


# Intervals
graph_sizes = [int(i * N_DELTA) for i in range(1, INTERVAL_NO + 1)]
fractions = [round(i * F_DELTA, 3) for i in range(1, INTERVAL_NO + 1)]


if __name__ == '__main__':

    # seeds
    seed = 200494

    # creating path
    data_path = "results/WS.csv"
    create_data_path_file(data_path)

    # experiments
    for n in graph_sizes:

        # setting seeds for reproducibility
        random.seed(seed)
        numpy.random.seed(seed)

        # iterations
        for k_fraction in fractions:

            # determining k
            k = int(n * k_fraction)

            for p in fractions:
                for r in fractions:

                    experiment_name = f"WS_{n}_{k_fraction}_{p}_{r}"
                    graph = nx.watts_strogatz_graph(n=n, k=k, p=p)
                    perform_experiment(original_graph=graph, ftrp=r, exp_name=experiment_name, data_path=data_path)
