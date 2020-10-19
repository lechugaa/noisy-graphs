import networkx as nx
import random


from negative_graphs.noisy_graph import NoisyGraph
from networkx.algorithms.centrality import degree_centrality, closeness_centrality
from negative_graphs.utilities import dict_average


if __name__ == '__main__':

    # generating original graph
    graph = nx.barabasi_albert_graph(1000, 20, 200494)

    # creating noisy graph
    noisy_graph = NoisyGraph()
    noisy_graph.add_edges_from(graph.edges, real=True)

    # obtaining missing edges list
    missing_edges = noisy_graph.concurrent_missing_edges()
    random.shuffle(missing_edges)

    # starting counters
    no_missing_edges = len(missing_edges)
    start_index = 0

    # printing headers
    print('fraction,number_of_edges,graph_uncertainty,'
          'mean_uncertainty,std_dev_uncertainty,min_uncertainty,max_uncertainty,'
          'mean_degree_centrality, mean_closeness_centrality')

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
        uncertainty_profile = noisy_graph.uncertainty_profile()

        # calculating noisy centrality metrics
        graph = nx.Graph(noisy_graph.edges())
        mean_degree_centrality = dict_average(degree_centrality(graph))
        mean_closeness_centrality = dict_average(closeness_centrality(graph))

        # printing results
        print(fraction, graph.number_of_edges(), graph_uncertainty,
              uncertainty_profile[0], uncertainty_profile[1], uncertainty_profile[2], uncertainty_profile[3],
              mean_degree_centrality, mean_closeness_centrality, sep=',')
