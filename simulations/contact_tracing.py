import networkx as nx
import random
import numpy


from negative_graphs.noisy_graph import NoisyGraph

if __name__ == '__main__':

    # experimental setup
    seed = 200494
    random.seed(seed)
    numpy.random.seed(seed)

    graph_size = 5000
    no_infected_nodes = round(0.01 * graph_size)
    m = 20

    graph = nx.barabasi_albert_graph(graph_size, m, seed)

    # creating noisy graph
    noisy_graph = NoisyGraph()
    noisy_graph.add_edges_from(graph.edges, real=True)

    # printing headers
    print('fraction,graph_uncertainty,mean_uncertainty,std_dev_uncertainty,min_uncertainty,max_uncertainty,'
          'number_contacts')

    # generating 20 observations
    for i in range(0, 101, 5):
        # obtaining fraction
        fraction = i / 100

        # adding edges from missing_edges list
        noisy_graph.add_missing_edges_per_node_ensuring_fraction(fraction)

        # calculating uncertainty values
        graph_uncertainty = noisy_graph.uncertainty()
        mean_uncertainty, std_dev_uncertainty, min_uncertainty, max_uncertainty = noisy_graph.uncertainty_profile()

        for j in range(10):
            infected_nodes = random.sample(noisy_graph.nodes(), no_infected_nodes)
            contacted_nodes = set()

            for node in infected_nodes:
                contacted_nodes = contacted_nodes.union(noisy_graph.node_neighbors(node))

            print(fraction,
                  graph_uncertainty, mean_uncertainty, std_dev_uncertainty, min_uncertainty, max_uncertainty,
                  len(contacted_nodes),
                  sep=',')
