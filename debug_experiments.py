import networkx as nx
from noisy_graphs.noisy_graph import NoisyGraph


if __name__ == '__main__':
    graph = nx.barabasi_albert_graph(n=20, m=3)
    n_graph = NoisyGraph(ftrp=0.5)
    n_graph.construct_graph(graph)
    print(n_graph.degree_centrality_profile(graph))
