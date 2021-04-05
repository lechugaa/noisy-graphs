import numpy
import random
import networkx as nx
from noisy_graphs.noisy_graph import NoisyGraph


# experimental conditions
max_interval = 20

graph_sizes = [i * 50 for i in range(1, max_interval + 1)]                        # from 50 to 1,000
probabilities = [round(0.025 * i, 3) for i in range(1, max_interval + 1)]         # from 0.025 to 0.500
ring_neighbors = [5 * i for i in range(1, max_interval + 1)]                      # from 5 to 100
new_node_edges = [5 * i for i in range(1, max_interval + 1)]                      # from  to 100
ftrps = [round(0.05 * i, 3) for i in range(1, max_interval + 1)]                  # from 0.050 to 1.000


def create_data_path_file(data_path: str):
    header = "exp_name, sigma_mean, sigma_variance, uncertainty_mean, uncertainty_variance, dc_distance, " \
             "dc_correlation, dc_mean_change, bc_distance, bc_correlation, bc_mean_change, cc_distance, " \
             "cc_correlation, cc_mean_change, ec_distance, ec_correlation, ec_mean_change\n"
    f = open(data_path, "w")
    f.write(header)
    f.close()


def perform_experiment(original_graph: nx.Graph, ftrp: float, exp_name: str, data_path: str):
    print(exp_name)

    # removing graph isolates
    # NoisyGraph is not intended to deal with isolated nodes
    original_graph.remove_nodes_from(list(nx.isolates(original_graph)))

    # constructing noisy graph
    noisy_graph = NoisyGraph(ftrp=ftrp)
    noisy_graph.construct_graph(original_graph)

    # algorithm compliance
    sigma_mean, sigma_variance = noisy_graph.get_sigmas_profile()

    # uncertainty
    uncertainty_mean, uncertainty_variance = noisy_graph.get_uncertainty_profile()

    # centrality_metrics
    dc_distance, dc_correlation, dc_mean_change = noisy_graph.degree_centrality_profile(original_graph)
    bc_distance, bc_correlation, bc_mean_change = noisy_graph.betweenness_profile(original_graph)
    cc_distance, cc_correlation, cc_mean_change = noisy_graph.closeness_profile(original_graph)
    ec_distance, ec_correlation, ec_mean_change = noisy_graph.eigenvector_centrality_profile(original_graph)

    # create raw file with original edges and noisy edges
    f = open(f"raw_data/{experiment_name[:2]}.txt", "a")
    f.write(f"Experimental conditions: {experiment_name}\n")
    f.write(f"Real edges: {noisy_graph.edges_if(real=True)}\n")
    f.write(f"Fake edges: {noisy_graph.edges_if(real=False)}\n\n")
    f.close()

    # add result to csv
    result = f"{exp_name}, {sigma_mean}, {sigma_variance}, {uncertainty_mean}, {uncertainty_variance}, "
    result += f"{dc_distance}, {dc_correlation}, {dc_mean_change}, "
    result += f"{bc_distance}, {bc_correlation}, {bc_mean_change}, "
    result += f"{cc_distance}, {cc_correlation}, {cc_mean_change}, "
    result += f"{ec_distance}, {ec_correlation}, {ec_mean_change}"
    result += "\n"

    f = open(data_path, "a")
    f.write(result)
    f.close()


if __name__ == '__main__':

    # setting seeds
    seed = 200494
    random.seed(seed)
    numpy.random.seed(seed)

    # Erdös-Rényi experiments:
    #     - n: size of graph
    #     - p: connection probability
    #     - r: fake-to-real edge proportion
    data_path = "results/ER.csv"
    create_data_path_file(data_path)

    for n in graph_sizes:
        for p in probabilities:
            for r in ftrps:
                experiment_name = f"ER_{n}_{p}_{r}"
                graph = nx.erdos_renyi_graph(n=n, p=p)
                perform_experiment(original_graph=graph, ftrp=r, exp_name=experiment_name, data_path=data_path)

    # Watts-Strogatz experiments:
    #     - n: size of graph
    #     - k: number of ring neighbors
    #     - p: rewiring probability
    #     - r: fake-to-real edge proportion
    data_path = "results/WS.csv"
    create_data_path_file(data_path)
    for n in graph_sizes:
        for k in ring_neighbors:
            for p in probabilities:
                for r in ftrps:
                    experiment_name = f"WS_{n}_{k}_{p}_{r}"
                    graph = nx.watts_strogatz_graph(n=n, k=k, p=p)
                    perform_experiment(original_graph=graph, ftrp=r, exp_name=experiment_name, data_path=data_path)

    # Barabási-Albert experiments:
    #     - n: size of graph
    #     - m: new connections per node
    #     - r: fake-to-real edge proportion
    data_path = "results/BA.csv"
    create_data_path_file(data_path)
    for n in graph_sizes:
        for m in new_node_edges:
            for r in ftrps:
                experiment_name = f"BA_{n}_{m}_{r}"
                graph = nx.barabasi_albert_graph(n=n, m=m)
                perform_experiment(original_graph=graph, ftrp=r, exp_name=experiment_name, data_path=data_path)
