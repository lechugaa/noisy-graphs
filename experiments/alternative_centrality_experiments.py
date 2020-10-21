import networkx as nx
import random
import numpy


from negative_graphs.noisy_graph import NoisyGraph
from networkx.algorithms import centrality
from negative_graphs.utilities import dict_squared_error_profile


if __name__ == '__main__':

    # experimental setup
    seed = 200494
    random.seed(seed)
    numpy.random.seed(seed)

    centrality_algorithms = [centrality.degree_centrality,
                             centrality.closeness_centrality,
                             centrality.betweenness_centrality,
                             centrality.eigenvector_centrality]

    graph_sizes = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

    # printing headers
    print('graph_size,real_fraction,no_edges,'
          'graph_uncertainty,mean_uncertainty,std_dev_uncertainty,min_uncertainty,max_uncertainty,'
          'centrality_metric,mean_se_value,min_se_value,max_se_value')

    # model setup
    m = 20

    # set of experiments for every graph size
    for graph_size in graph_sizes:

        # generating original graph
        graph = nx.barabasi_albert_graph(graph_size, m, seed)

        # obtaining original centrality metrics
        original_metrics = {alg.__name__: alg(graph) for alg in centrality_algorithms}

        # creating noisy graph
        noisy_graph = NoisyGraph()
        noisy_graph.add_edges_from(graph.edges, real=True)

        # generating 20 observations
        for i in range(0, 101, 5):
            # obtaining fraction
            fraction = i / 100

            # adding edges from missing_edges list
            noisy_graph.add_missing_edges_per_node_ensuring_fraction(fraction)

            # calculating uncertainty values
            graph_uncertainty = noisy_graph.uncertainty()
            mean_uncertainty, std_dev_uncertainty, min_uncertainty, max_uncertainty = noisy_graph.uncertainty_profile()

            # disturbing graph
            graph = nx.Graph(noisy_graph.edges())

            # iterating over centrality algorithms
            for alg in centrality_algorithms:
                modified_metrics = alg(graph)
                mean_se, min_se, max_se = dict_squared_error_profile(modified_metrics, original_metrics[alg.__name__])

                print(graph_size, fraction, graph.number_of_edges(),
                      graph_uncertainty, mean_uncertainty, std_dev_uncertainty, min_uncertainty, max_uncertainty,
                      alg.__name__, mean_se, min_se, max_se,
                      sep=',')
