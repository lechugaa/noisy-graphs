import numpy
import random
import networkx as nx
from experiment_utils import create_data_path_file, perform_experiment


# Erdös-Rényi experiments:
#     - n: size of graph
#     - p: connection probability
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
    data_path = "results/ER.csv"
    create_data_path_file(data_path)

    # experiments
    for n in graph_sizes:

        # iterations
        for p in fractions:
            for r in fractions:
                # setting seeds for reproducibility
                random.seed(seed)
                numpy.random.seed(seed)

                experiment_name = f"ER_{n}_{p}_{r}"
                graph = nx.erdos_renyi_graph(n=n, p=p)
                perform_experiment(original_graph=graph, ftrp=r, exp_name=experiment_name, data_path=data_path)
