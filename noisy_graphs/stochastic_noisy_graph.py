import statistics
# import random
from math import log
from scipy.special import comb


from noisy_graphs.noisy_node import NoisyNode
from noisy_graphs.heaps import MaxHeap, MinHeap


class StochasticNoisyGraph:
    def __init__(self, ftrp):
        self.__real_edges = {}
        self.__fake_edges = {}
        self.__max_heap = MaxHeap()
        self.__min_heap = MinHeap()
        self.__ftrp = ftrp

    @property
    def nodes(self):
        return [node for node in self.__real_edges.keys()]

    @property
    def number_of_nodes(self):
        return len(self.nodes)

    def __node_with_value_exists(self, value):
        node = NoisyNode(value=value, desired_ftrp=self.__ftrp, real_connections=1, fake_connections=0)
        return node in self.nodes

    @staticmethod
    def __get_internal_edge(node1, node2):
        """
        Returns a two-tuple where elements are in increasing order.
        """
        return (node1, node2) if node1.value < node2.value else (node2, node1)

    @staticmethod
    def __get_regular_edge(node1, node2):
        """
        Returns a two-tuple where elements are in increasing order.
        """
        return (node1.value, node2.value) if node1.value < node2.value else (node2.value, node1.value)

    @staticmethod
    def __get_edge(node1, node2, internal):
        if internal:
            return StochasticNoisyGraph.__get_internal_edge(node1, node2)

        return StochasticNoisyGraph.__get_regular_edge(node1, node2)

    def edges_if(self, real, internal):
        """
        Returns a set of all edges in the graph that satisfy the `real`
        condition. If `internal` is set to true, the returned set
        will include the node's ftrp and sigma.
        """
        graph_dictionary = self.__real_edges if real else self.__fake_edges
        edge_set = set()

        for node1, nodes in graph_dictionary.items():
            for node2 in nodes:
                edge = StochasticNoisyGraph.__get_edge(node1, node2, internal=internal)
                edge_set.add(edge)

        return edge_set

    @property
    def internal_edges(self):
        """
        Return all edges in the graph, both real and fake.
        """
        real_edges = self.edges_if(real=True, internal=True)
        fake_edges = self.edges_if(real=False, internal=True)
        return real_edges.union(fake_edges)

    @property
    def regular_edges(self):
        """
        Return all edges in the graph, both real and fake.
        """
        real_edges = self.edges_if(real=True, internal=False)
        fake_edges = self.edges_if(real=False, internal=False)
        return real_edges.union(fake_edges)

    def node_neighbors_if(self, node, real):
        """
        Returns a set of all nodes connected to node that satisfy the
        real condition.
        """
        graph_dictionary = self.__real_edges if real else self.__fake_edges
        return graph_dictionary[node]

    def node_neighbors(self, node):
        """
        Returns a set of all nodes connected to node.
        """
        real_neighbors = self.node_neighbors_if(node, real=True)
        fake_neighbors = self.node_neighbors_if(node, real=False)
        return real_neighbors.union(fake_neighbors)

    def node_adjacency_if(self, node, real, internal):
        """
        Returns a set of all edges connected to node that satisfy the
        real condition.
        """
        adjacency_set = set()
        if node in self.nodes:
            graph_dictionary = self.__real_edges if real else self.__fake_edges
            neighbors = graph_dictionary[node]
            for neighbor in neighbors:
                edge = StochasticNoisyGraph.__get_edge(node, neighbor, internal=internal)
                adjacency_set.add(edge)

        return adjacency_set

    def node_adjacency(self, node, internal):
        """
        Returns a set of all edges connected to node.
        """
        real_edges = self.node_adjacency_if(node, real=True, internal=internal)
        fake_edges = self.node_adjacency_if(node, real=False, internal=internal)
        return real_edges.union(fake_edges)

    def number_of_edges(self):
        """
        Obtain the number of real, fake and total edges in the graph.
        :return: 3-tuple (no_real_edges, no_fake_edges, total_edges)
        """
        total = len(self.internal_edges)
        no_real_edges = len(self.edges_if(real=True, internal=True))
        no_fake_edges = total - no_real_edges
        return no_real_edges, no_fake_edges, total

    def number_of_edges_for_node(self, node):
        """
        Obtain the number of real, fake and total
        edges in the graph for node.
        :param node: hashable
        :return: 3-tuple (no_real_edges, no_fake_edges, total_edges)
        """
        if node not in self.nodes:
            return None

        total = len(self.node_adjacency(node, internal=True))
        no_real_edges = len(self.node_adjacency_if(node, real=True, internal=True))
        no_fake_edges = total - no_real_edges
        return no_real_edges, no_fake_edges, total

    def __add_node(self, node):
        if node not in self.nodes:
            self.__real_edges[node] = set()
            self.__fake_edges[node] = set()

    def add_node_with_edges(self, value, edges, add_fake_edges):
        no_real_edges = len(edges)
        node = NoisyNode(value=value, desired_ftrp=self.__ftrp, real_connections=no_real_edges, fake_connections=0)

        if node not in self.nodes:
            self.__add_node(node)
            # TODO: Aquí tienes que seguirle

    def add_edge(self, node1, node2, real):
        pass

    @staticmethod
    def __number_of_hypotheses(total_edges, fake_edges, exact=True):
        """
        Calculates the number of hypotheses an attacker will need to
        consider in case there are a total of 'fake_edges' among 'total_edges'
        possible. The 'exact' parameter indicates whether the attacker knows
        the exact number of fake edges (True) or the maximum number of
        fake edges (False).
        :param total_edges: integer
        :param fake_edges: integer
        :param exact: boolean
        :return: integer
        """
        no_hypotheses = 0
        if exact:
            no_hypotheses = comb(total_edges, fake_edges, exact=True)
        else:
            for i in range(fake_edges + 1):
                no_hypotheses += comb(total_edges, i, exact=True)

        return no_hypotheses

    def uncertainty(self, base=2, exact=True):
        """
        Calculates the graph uncertainty. The parameter `base` is used
        to determine the units i.e., bits, trits, etc. If `exact` is set
        to True it means that an attacker knows the exact number of fake
        edges. If it is set to False it means the attacker knows the
        maximum number of fake edges.
        :param base: positive integer
        :param exact: boolean
        :return: integer
        """
        _, no_fake_edges, total_edges = self.number_of_edges()
        no_hypotheses = StochasticNoisyGraph.__number_of_hypotheses(total_edges, no_fake_edges, exact)
        return log(no_hypotheses, base)

    def node_uncertainty(self, node, base=2, exact=True):
        """Calculates a given `node` uncertainty. The parameter `base` is
        used to determine the units i.e., bits, trits, etc. If `exact` is
        set to True it means that an attacker knows the exact number of fake
        edges. If it is set to False it means the attacker knows the maximum
        number of fake edges.
        :param node: hashable
        :param base: positive integer
        :param exact: boolean
        :return: integer or None if node does not exist in graph
        """
        if node not in self.nodes:
            return None

        _, no_fake_edges, total_edges = self.number_of_edges_for_node(node)
        no_hypotheses = StochasticNoisyGraph.__number_of_hypotheses(total_edges, no_fake_edges, exact)
        return log(no_hypotheses, base)

    def node_uncertainties(self, base=2, exact=True):
        """
        Calculates the uncertainty of all the nodes in the graph
        and returns a list. The parameter `base` is  used to determine the units
        i.e., bits, trits, etc. If `exact` is set to True it means that an attacker
        knows the exact number of fake edges per node. If it is set to False it means
        the attacker knows the maximum number of fake edges per node.
        :param base: positive integer
        :param exact: boolean
        :return: list of floats
        """
        return [self.node_uncertainty(node, base, exact) for node in self.nodes]

    def uncertainty_profile(self, base=2, exact=True):
        """
        Calculates the mean and standard deviation of the
        graph's nodes uncertainty. The parameter `base` is
        used to determine the units i.e., bits, trits, etc.
        If `exact` is set to True it means that an attacker knows
        the exact number of fake edges per node. If it is set to False
        it means the attacker knows the maximum number of fake edges
        per node.
        :param base: positive integer
        :param exact: boolean
        :return: tuple of floats corresponding to (mean, std_dev)
        """
        uncertainties = self.node_uncertainties(base, exact)
        mean = statistics.mean(uncertainties)
        std_dev = statistics.pstdev(uncertainties)
        minimum = min(uncertainties)
        maximum = max(uncertainties)

        return mean, std_dev, minimum, maximum
