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


def dict_squared_error_profile(dict1, dict2):
    total_squared_error = 0
    min_squared_error = float('inf')
    max_squared_error = float('-inf')

    for key in dict1.keys():
        squared_error = (dict1[key] - dict2[key]) ** 2
        total_squared_error += squared_error
        min_squared_error = min(squared_error, min_squared_error)
        max_squared_error = max(squared_error, max_squared_error)

    mean_squared_error = total_squared_error / len(dict1)

    return mean_squared_error, min_squared_error, max_squared_error
