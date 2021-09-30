import numpy
import random
import networkx as nx
from experiment_utils import create_data_path_file, perform_experiment


# Barabási-Albert experiments:
#     - n: size of graph
#     - m: new connections per node
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
    data_path = "results/BA.csv"
    create_data_path_file(data_path)

    # experiments
    for n in graph_sizes:

        # iterations
        for m_fraction in fractions:
            # determining m
            m = int(n * m_fraction)
            m = (m - 1) if (m == n) else m

            for r in fractions:
                # setting seeds for reproducibility
                random.seed(seed)
                numpy.random.seed(seed)

                experiment_name = f"BA_{n}_{m_fraction}_{r}"
                graph = nx.barabasi_albert_graph(n=n, m=m)
                perform_experiment(original_graph=graph, ftrp=r, exp_name=experiment_name, data_path=data_path)
