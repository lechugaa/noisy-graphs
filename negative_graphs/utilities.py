import networkx as nx
from tqdm import tqdm


def negative_graph(graph):
    neg_graph = nx.Graph()
    neg_graph.add_nodes_from(graph.nodes)

    for node1 in tqdm(neg_graph.nodes):
        for node2 in neg_graph.nodes:
            if node1 != node2 and not graph.has_edge(node1, node2):
                neg_graph.add_edge(node1, node2)

    return neg_graph


def get_undirected_graph_from_txt(path):
    graph = nx.Graph()
    file = open(path, "r")
    for line in tqdm(file):
        node_list = line.split()
        graph.add_edge(node_list[0], node_list[1])
    file.close()

    return graph
