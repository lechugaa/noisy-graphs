import networkx as nx
import random
import numpy


from negative_graphs.noisy_graph import NoisyGraph
from networkx.algorithms import centrality
from negative_graphs.utilities import dict_squared_error_profile


if __name__ == '__main__':

    seed = 200494
    random.seed(seed)
    numpy.random.seed(seed)

    m = 20
    graph_sizes = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    centrality_algorithms = [centrality.degree_centrality,
                             centrality.closeness_centrality,
                             centrality.betweenness_centrality,
                             centrality.eigenvector_centrality]

    # printing headers
    print('graph_size,fraction,no_edges,'
          'graph_uncertainty,mean_uncertainty,std_dev_uncertainty,min_uncertainty,max_uncertainty,'
          'centrality_metric,mean_se_value,min_se_value,max_se_value')

    # set of old_experiments for every graph size
    for graph_size in graph_sizes:

        # generating original graph
        graph = nx.barabasi_albert_graph(graph_size, m, seed)

        # obtaining original centrality metrics
        original_metrics = {alg.__name__: alg(graph) for alg in centrality_algorithms}

        # creating noisy graph
        noisy_graph = NoisyGraph()
        noisy_graph.add_edges_from(graph.edges, real=True)

        # obtaining missing edges list
        missing_edges = noisy_graph.missing_edges()
        random.shuffle(missing_edges)

        # starting counters
        no_missing_edges = len(missing_edges)
        start_index = 0

        # generating 20 observations
        for i in range(0, 101, 5):
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
            mean_uncertainty, std_dev_uncertainty, min_uncertainty, max_uncertainty = noisy_graph.uncertainty_profile()

            # creating noisy graph
            graph = nx.Graph(noisy_graph.edges())

            # iterating over centrality algorithms
            for alg in centrality_algorithms:
                modified_metrics = alg(graph)
                mean_se, min_se, max_se = dict_squared_error_profile(modified_metrics, original_metrics[alg.__name__])

                print(graph_size, fraction, graph.number_of_edges(),
                      graph_uncertainty, mean_uncertainty, std_dev_uncertainty, min_uncertainty, max_uncertainty,
                      alg.__name__, mean_se, min_se, max_se,
                      sep=',')
