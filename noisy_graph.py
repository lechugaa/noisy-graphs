import networkx as nx
import statistics
from math import log
from scipy.special import comb


class NoisyGraph:

    def __init__(self, edges=None):
        if edges is None:
            edges = []
        self.__graph = nx.Graph()
        self.__graph.add_edges_from(edges)
        nx.set_edge_attributes(self.__graph, True, name="real")

    @staticmethod
    def number_of_hypotheses(no_total, no_false, exact=True):
        no_hypotheses = 0
        if exact:
            no_hypotheses = comb(no_total, no_false, exact=True)
        else:
            for i in range(no_false + 1):
                no_hypotheses += comb(no_total, i, exact=True)

        return no_hypotheses

    def get_nodes(self):
        return [node for node in self.__graph.nodes]

    def add_edge(self, n1, n2, real=True):
        self.__graph.add_edge(n1, n2, real=real)

    def add_edges_from(self, edge_list, real=True):
        self.__graph.add_edges_from(edge_list, real=real)

    def get_edges(self, real=None):
        if real is None:
            return [(n1, n2) for (n1, n2) in self.__graph.edges]

        return [(n1, n2) for (n1, n2) in self.__graph.edges if self.__graph[n1][n2]['real'] == real]

    def get_node_edges(self, node, real=None):
        if node not in self.__graph.nodes:
            return None

        if real is None:
            return [(node, n) for n in self.__graph[node]]

        return [(node, n) for n in self.__graph[node] if self.__graph[node][n]['real'] == real]

    def count_edges(self):
        total = self.__graph.number_of_edges()
        no_real_edges = len(self.get_edges(real=True))
        no_false_edges = total - no_real_edges
        return no_real_edges, no_false_edges, total

    def count_node_edges(self, node):
        if node not in self.__graph.nodes:
            return None

        total = len(self.get_node_edges(node))
        no_real_edges = len(self.get_node_edges(node, real=True))
        no_false_edges = total - no_real_edges
        return no_real_edges, no_false_edges, total

    def uncertainty(self, base=2, exact=True):
        _, no_false, no_total = self.count_edges()
        no_hypotheses = NoisyGraph.number_of_hypotheses(no_total, no_false, exact)
        return log(no_hypotheses, base)

    def node_uncertainty(self, node, base=2, exact=True):
        if node not in self.__graph.nodes:
            return None

        _, no_false, no_total = self.count_node_edges(node)
        no_hypotheses = NoisyGraph.number_of_hypotheses(no_total, no_false, exact)
        return log(no_hypotheses, base)

    def node_uncertainties(self, base=2, exact=True):
        return [self.node_uncertainty(node, base, exact) for node in self.__graph.nodes]

    def uncertainty_profile(self, base=2, exact=True):
        uncertainties = self.node_uncertainties(base, exact)
        mean = sum(uncertainties) / len(uncertainties)
        stdev = statistics.pstdev(uncertainties)
        return mean, stdev
