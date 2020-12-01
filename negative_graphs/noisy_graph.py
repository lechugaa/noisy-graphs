import statistics
import concurrent.futures
import random
from math import log
from scipy.special import comb


class NoisyGraph:
    """An undirected graph where some of the edges
    contained are fake.
    """
    def __init__(self):
        """
        Initializes a noisy graph object.
        """
        self.__real_edges = {}
        self.__fake_edges = {}

    def nodes(self):
        """
        Returns all the nodes in the graph
        :return: list hashable objects
        """
        return [node for node in self.__real_edges.keys()]

    def number_of_nodes(self):
        """Returns the number of nodes in the graph
        :return: integer
        """
        return len(self.nodes())

    def add_node(self, node):
        """
        Adds a single node to the noisy graph object.
        If the node already exists, nothing is performed.
        :param node: hashable
        """
        if node not in self.nodes():
            self.__real_edges[node] = set()
            self.__fake_edges[node] = set()

    def add_nodes_from(self, nodes):
        """Adds multiple nodes from a node list.
        If a node already exists in the graph, it is not
        added again.
        :param nodes: a list of nodes
        """
        for node in nodes:
            self.add_node(node)

    @staticmethod
    def __get_edge(node1, node2):
        """Returns a two-tuple with which elements are in increasing order.
        :param node1: hashable
        :param node2: hashable
        :return: a two-tuple with which elements are in increasing order
        """
        return (node1, node2) if node1 < node2 else (node2, node1)

    def edges_if(self, real=True):
        """Returns a set of all edges that satisfy the `real`
        condition.
        :param real: boolean
        :return: a set of two-tuples
        """
        graph_dictionary = self.__real_edges if real else self.__fake_edges
        edge_set = set()

        for node1, nodes in graph_dictionary.items():
            for node2 in nodes:
                edge = NoisyGraph.__get_edge(node1, node2)
                edge_set.add(edge)

        return edge_set

    def edges(self):
        """Return all edges in the graph, both real and fake.
        :return: a set of two-tuples
        """
        real_edges = self.edges_if(real=True)
        fake_edges = self.edges_if(real=False)
        return real_edges.union(fake_edges)

    def add_edge(self, node1, node2, real):
        """
        Adds a single edge to the graph. If the nodes in the edge
        do not exists, they are added first to the graph. The `real`
        parameter indicates whether the edge is real or fake. If the
        edge already exists as the opposite (real or fake) it is updated.
        :param node1: hashable object
        :param node2: hashable object
        :param real: boolean
        """
        if node1 not in self.nodes():
            self.add_node(node1)
        if node2 not in self.nodes():
            self.add_node(node2)

        if real:
            self.__real_edges[node1].add(node2)
            self.__fake_edges[node1].discard(node2)
            self.__real_edges[node2].add(node1)
            self.__fake_edges[node2].discard(node1)
        else:
            self.__fake_edges[node1].add(node2)
            self.__real_edges[node1].discard(node2)
            self.__fake_edges[node2].add(node1)
            self.__real_edges[node2].discard(node1)

    def add_edges_from(self, edge_list, real):
        """Adds multiple edges to the graph. If the nodes in the edge
        do not exists, they are added first to the graph. The `real`
        parameter indicates whether the edge is real or fake. If the
        edge already exists as the opposite (real or fake) it is updated.
        :param edge_list: a list of tuples containing the edges as (node1, node2)
        :param real: boolean
        """
        for node1, node2 in edge_list:
            self.add_edge(node1, node2, real)

    def clear_fake_edges(self):
        """Removes all fake edges from noisy graph"""
        self.__fake_edges = {}
        for node in self.nodes():
            self.__fake_edges[node] = set()

    def node_neighbors_if(self, node, real=True):
        graph_dictionary = self.__real_edges if real else self.__fake_edges
        return graph_dictionary[node]

    def node_neighbors(self, node):
        real_neighbors = self.node_neighbors_if(node, real=True)
        fake_neighbors = self.node_neighbors_if(node, real=True)
        return real_neighbors.union(fake_neighbors)

    def node_adjacency_if(self, node, real=True):
        """Returns a set of all edges connected to node that satisfy the
        real condition.
        :param node: hashable
        :param real: boolean
        :return: a set of tuples
        """
        adjacency_set = set()
        if node in self.nodes():
            graph_dictionary = self.__real_edges if real else self.__fake_edges
            neighbors = graph_dictionary[node]
            for neighbor in neighbors:
                edge = NoisyGraph.__get_edge(node, neighbor)
                adjacency_set.add(edge)

        return adjacency_set

    def node_adjacency(self, node):
        """Returns a set of all edges connected to node.
        :param node: hashable
        :return: a set of tuples
        """
        real_edges = self.node_adjacency_if(node, True)
        fake_edges = self.node_adjacency_if(node, False)
        return real_edges.union(fake_edges)

    def number_of_edges(self):
        """Obtain the number of real, fake and total edges in the graph.
        :return: 3-tuple
        """
        total = len(self.edges())
        no_real_edges = len(self.edges_if(True))
        no_fake_edges = total - no_real_edges
        return no_real_edges, no_fake_edges, total

    def number_of_edges_for_node(self, node):
        """Obtain the number of real, fake and total
        edges in the graph for node.
        :param node: hashable
        :return: 3-tuple (no_real_edges, no_fake_edges, total_edges)
        """
        if node not in self.nodes():
            return None

        total = len(self.node_adjacency(node))
        no_real_edges = len(self.node_adjacency_if(node, True))
        no_fake_edges = total - no_real_edges
        return no_real_edges, no_fake_edges, total

    @staticmethod
    def __number_of_hypotheses(total_edges, fake_edges, exact=True):
        """Calculates the number of hypotheses an attacker will need to
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
        """Calculates the graph uncertainty. The parameter `base` is used
        to determine the units i.e., bits, trits, etc. If `exact` is set
        to True it means that an attacker knows the exact number of fake
        edges. If it is set to False it means the attacker knows the
        maximum number of fake edges.
        :param base: positive integer
        :param exact: boolean
        :return: integer
        """
        _, no_fake_edges, total_edges = self.number_of_edges()
        no_hypotheses = NoisyGraph.__number_of_hypotheses(total_edges, no_fake_edges, exact)
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
        if node not in self.nodes():
            return None

        _, no_fake_edges, total_edges = self.number_of_edges_for_node(node)
        no_hypotheses = NoisyGraph.__number_of_hypotheses(total_edges, no_fake_edges, exact)
        return log(no_hypotheses, base)

    def node_uncertainties(self, base=2, exact=True):
        """Calculates the uncertainty of all the nodes in the graph
        and returns a list. The parameter `base` is  used to determine the units
        i.e., bits, trits, etc. If `exact` is set to True it means that an attacker
        knows the exact number of fake edges per node. If it is set to False it means
        the attacker knows the maximum number of fake edges per node.
        :param base: positive integer
        :param exact: boolean
        :return: list of floats
        """
        return [self.node_uncertainty(node, base, exact) for node in self.nodes()]

    def uncertainty_profile(self, base=2, exact=True):
        """Calculates the mean and standard deviation of the
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

    def missing_edges_for_node(self, node):
        """
        Returns the edges the given node is missing to be
        connected to all other nodes.
        :param node: hashable
        :return: list of 2-tuples
        """
        missing_edges = []
        existing_edges = self.node_adjacency(node)
        for node2 in self.nodes():
            if node != node2:
                edge = NoisyGraph.__get_edge(node, node2)
                if edge not in existing_edges:
                    missing_edges.append(edge)

        return missing_edges

    def missing_edges(self):
        """
        Returns the edges the graph is missing to be
        a complete graph.
        :return: list of 2-tuples
        """
        missing_edges_set = set()
        for node in self.nodes():
            node_missing_edges = set(self.missing_edges_for_node(node))
            missing_edges_set = missing_edges_set.union(node_missing_edges)

        return list(missing_edges_set)

    def concurrent_missing_edges(self):
        """
        Returns the edges the graph is missing to be
        a complete graph.
        :return: list of 2-tuples
        """
        missing_edges_set = set()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.missing_edges_for_node, node) for node in self.nodes()]

            for f in concurrent.futures.as_completed(results):
                missing_edges_set = missing_edges_set.union(set(f.result()))

        return list(missing_edges_set)

    def random_missing_edges(self, fraction):
        """
        Returns a list containing a fraction of the graph's
        missing edges.
        :param fraction: floating number between 0 and 1
        :return: a list tuples
        """
        missing_edges = self.missing_edges()
        no_edges = round(len(missing_edges) * fraction)
        return random.sample(missing_edges, no_edges)

    def add_random_missing_edges(self, fraction):
        """
        Adds a fraction of the missing edges to the graph
        as fake edges.
        :param fraction: floating number between 0 and 1
        """
        missing_edges = self.random_missing_edges(fraction)
        self.add_edges_from(missing_edges, real=False)

    def fake_edges_ensuring_fraction(self, node, fraction):
        """
        Returns a list of a node's missing edges. The amount of
        missing edges that is returned is the necessary amount to
        ensure that, once added, the number of fake edges is at least
        equivalent to the fraction given of real edges.
        :param node: hashable
        :param fraction: floating number between 0 and 1
        :return: a list tuples
        """
        missing_edges = self.missing_edges_for_node(node)
        no_existing_real_edges, no_existing_fake_edges, _ = self.number_of_edges_for_node(node)

        # number that should exist at end of method
        total_fake_edges = round(fraction * no_existing_real_edges)

        # number of edges missing to ensure total_fake_edges
        no_missing_fake_edges = total_fake_edges - no_existing_fake_edges

        if no_missing_fake_edges < 0:
            no_missing_fake_edges = 0

        if no_missing_fake_edges > len(missing_edges):
            no_missing_fake_edges = len(missing_edges)

        return random.sample(missing_edges, no_missing_fake_edges)

    def add_missing_edges_ensuring_fraction(self, node, fraction):
        """
        Adds fake edges to a node. The number of fake edges added
        ensures that, once added, the number of fake edges is at least
        equivalent to the fraction given of real edges.
        :param node: hashable
        :param fraction: floating number between 0 and 1
        """
        edges = self.fake_edges_ensuring_fraction(node, fraction)
        self.add_edges_from(edges, real=False)

    def add_missing_edges_per_node_ensuring_fraction(self, fraction):
        """
        Adds fake edges to each node node. The number of fake edges added
        per node ensures that, once added, the number of fake edges is at
        least equivalent to the fraction given of real edges.
        :param fraction: floating number between 0 and 1
        """
        for node in self.nodes():
            self.add_missing_edges_ensuring_fraction(node, fraction)
