import networkx as nx
from noisy_graphs.noisy_graph import NoisyGraph


if __name__ == '__main__':
    graph = nx.erdos_renyi_graph(n=200, p=0.7)
    n_graph = NoisyGraph(ftrp=0.5)
    n_graph.construct_graph(graph)
    print(n_graph.degree_centrality_profile(graph))
