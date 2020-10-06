import networkx as nx
import random
import time
from negative_graphs.noisy_graph import NoisyGraph
from networkx.algorithms import centrality
from negative_graphs.utilities import dict_squared_error_profile


if __name__ == '__main__':

    # timing execution
    t1 = time.perf_counter()

    # generating original graph
    # graph = nx.watts_strogatz_graph(1000, 5, 0.5, 200494)
    # graph = nx.erdos_renyi_graph(1000, 0.1, 200494)
    graph = nx.barabasi_albert_graph(1000, 20, 200494)

    # obtaining original centrality metrics
    o_degree_centrality = centrality.degree_centrality(graph)
    o_betweenness_centrality = centrality.betweenness_centrality(graph)
    o_closeness_centrality = centrality.closeness_centrality(graph)
    o_eigen_centrality = centrality.eigenvector_centrality(graph)

    # creating noisy graph
    noisy_graph = NoisyGraph()
    noisy_graph.add_edges_from(graph.edges, real=True)

    # obtaining missing edges list
    missing_edges = noisy_graph.missing_edges()

    # shuffling missing edges list
    random.shuffle(missing_edges)

    # starting counters
    no_missing_edges = len(missing_edges)
    start_index = 0

    # printing headers
    print('fraction,graph_uncertainty,mean_uncertainty,std_dev_uncertainty,'
          'mean_se_degree_centrality,min_se_degree_centrality,max_se_degree_centrality,'
          'mean_se_betweenness_centrality,min_se_betweenness_centrality,max_se_betweenness_centrality,'
          'mean_se_closeness_centrality,min_se_closeness_centrality,max_se_closeness_centrality,'
          'mean_se_eigen_centrality,min_se_eigen_centrality,max_se_eigen_centrality')

    for i in range(101):
        # obtaining ending index
        fraction = i / 100
        end_index = round(no_missing_edges * fraction)

        # adding edges from missing_edges list
        edges_to_add = missing_edges[start_index:end_index]
        noisy_graph.add_edges_from(edges_to_add, real=False)

        # updating start index
        start_index = end_index

        # calculating uncertainty values
        graph_uncertainty = noisy_graph.uncertainty()
        mean_uncertainty, std_dev_uncertainty = noisy_graph.uncertainty_profile()

        # calculating noisy centrality metrics
        graph = nx.Graph(noisy_graph.edges())
        n_degree_centrality = centrality.degree_centrality(graph)
        n_betweenness_centrality = centrality.betweenness_centrality(graph)
        n_closeness_centrality = centrality.closeness_centrality(graph)
        n_eigen_centrality = centrality.eigenvector_centrality(graph)

        # calculating mean square errors
        sep_degree_centrality = dict_squared_error_profile(o_degree_centrality, n_degree_centrality)
        sep_betweenness_centrality = dict_squared_error_profile(o_betweenness_centrality, n_betweenness_centrality)
        sep_closeness_centrality = dict_squared_error_profile(o_closeness_centrality, n_closeness_centrality)
        sep_eigen_centrality = dict_squared_error_profile(o_eigen_centrality, n_eigen_centrality)

        # printing results
        print(fraction, graph_uncertainty, mean_uncertainty, std_dev_uncertainty,
              sep_degree_centrality[0], sep_degree_centrality[1], sep_degree_centrality[2],
              sep_betweenness_centrality[0], sep_betweenness_centrality[1], sep_betweenness_centrality[2],
              sep_closeness_centrality[0], sep_closeness_centrality[1], sep_closeness_centrality[2],
              sep_eigen_centrality[0], sep_eigen_centrality[1], sep_eigen_centrality[2],
              sep=',')

    # timing execution
    t2 = time.perf_counter()
    print()
    print(f"Execution time: {round(t2 - t1, 3)} second(s)")
    print(f"Number of missing edges: {len(missing_edges)}")
