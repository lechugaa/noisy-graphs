from igraph import Graph
from math import log2


def _translate_graph(graph):
    h = Graph()
    h.add_vertices(list(graph.nodes))
    h.add_edges(list(graph.edges))
    return h


def orbits(graph):
    g = _translate_graph(graph)
    no_nodes = graph.number_of_nodes()
    g_auts = g.get_automorphisms_vf2()

    g_orbits = []
    for i in range(no_nodes):
        orbit = set([aut[i] for aut in g_auts])
        if orbit not in g_orbits:
            g_orbits.append(orbit)

    return g_orbits


def entropy(graph):
    g_entropy = 0
    no_nodes = graph.number_of_nodes()
    g_orbits = orbits(graph)
    for orbit in g_orbits:
        p = len(orbit) / no_nodes
        g_entropy += -p * log2(p)

    return g_entropy


def entropy_change(graph, added_edge):
    eo = entropy(graph)
    graph_f = graph.copy()
    graph_f.add_edge(added_edge[0], added_edge[1])
    ef = entropy(graph_f)
    return abs(ef - eo)


def entropy_change_list(graph):
    entropy_deltas = []
    nodes = list(graph.nodes)
    no_nodes = graph.number_of_nodes()
    for i in range(no_nodes):
        for j in range(i + 1, no_nodes):
            edge = (nodes[i], nodes[j])
            if not graph.has_edge(*edge):
                entropy_delta = entropy_change(graph, edge)
                if entropy_delta != 0:
                    entropy_deltas.append((edge, entropy_delta))

    return entropy_deltas
