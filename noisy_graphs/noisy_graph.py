import networkx as nx
import numpy as np
import statistics
from math import log
from networkx.algorithms import centrality
from scipy.special import comb
from scipy.stats import spearmanr, wasserstein_distance


class NoisyGraph:
    """
    An undirected graph where some of the edges
    contained are fake.
    """
    def __init__(self, ftrp):
        """
        Initializes a noisy graph object.
        """
        self.__real_edges = {}
        self.__fake_edges = {}
        self.__sigmas = {}
        self.__ftrp = ftrp

    # MARK: Node methods
    def nodes(self):
        """
        Returns all the nodes in the graph
        :return: list hashable objects
        """
        return [node for node in self.__real_edges.keys()]

    def number_of_nodes(self):
        """
        Returns the number of nodes in the graph
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

    # MARK: Edges methods
    @staticmethod
    def __get_edge(node1, node2):
        """
        Returns a two-tuple with which elements are in increasing order.
        :param node1: hashable
        :param node2: hashable
        :return: a two-tuple with which elements are in increasing order
        """
        return (node1, node2) if node1 < node2 else (node2, node1)

    def edges_if(self, real):
        """
        Returns a set of all edges that satisfy the `real`
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
        """
        Return all edges in the graph, both real and fake.
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

        self.set_node_sigma(node1)
        self.set_node_sigma(node2)

    def node_neighbors_if(self, node, real):
        """
        Returns a set of all nodes that are neighbors of the passed one.
        The 'real' parameter determines if fake neighbors are returned
        or the real ones.
        :param node: hashable
        :param real: boolean
        :return: list of nodes
        """
        graph_dictionary = self.__real_edges if real else self.__fake_edges
        return graph_dictionary[node]

    def node_neighbors(self, node):
        """
        Returns a set of all nodes that are neighbors of the passed one.
        :param node: hashable
        :return: list of nodes
        """
        real_neighbors = self.node_neighbors_if(node, real=True)
        fake_neighbors = self.node_neighbors_if(node, real=False)
        return real_neighbors.union(fake_neighbors)

    def node_adjacency_if(self, node, real):
        """
        Returns a set of all edges connected to node that satisfy the
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
        """
        Returns a set of all edges connected to node.
        :param node: hashable
        :return: a set of tuples
        """
        real_edges = self.node_adjacency_if(node, True)
        fake_edges = self.node_adjacency_if(node, False)
        return real_edges.union(fake_edges)

    def number_of_edges(self):
        """
        Obtain the number of real, fake and total edges in the graph.
        :return: 3-tuple (no_real_edges, no_fake_edges, total_edges)
        """

        # TODO: Can be improved by using node neighbors instead
        total = len(self.edges())
        no_real_edges = len(self.edges_if(True))
        no_fake_edges = total - no_real_edges
        return no_real_edges, no_fake_edges, total

    def number_of_edges_for_node(self, node):
        """
        Obtain the number of real, fake and total
        edges in the graph for node.
        :param node: hashable
        :return: 3-tuple (no_real_edges, no_fake_edges, total_edges)
        """
        if node not in self.nodes():
            return None

        total = len(self.node_neighbors(node))
        no_real_edges = len(self.node_neighbors_if(node, True))
        no_fake_edges = total - no_real_edges
        return no_real_edges, no_fake_edges, total

    # MARK: Uncertainty methods
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
        return [self.node_uncertainty(node, base, exact) for node in self.nodes()]

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

    # MARK: Graph construction method
    def set_node_sigma(self, node):
        no_real_edges, no_fake_edges, _ = self.number_of_edges_for_node(node)
        node_ftrp = no_fake_edges / no_real_edges
        node_sigma = node_ftrp / self.__ftrp
        self.__sigmas[node] = node_sigma

    def get_node_sigma(self, node):
        return self.__sigmas[node]

    def get_graph_sigmas(self):
        return list(self.__sigmas.values())

    def number_of_fake_edges_to_add(self, no_real_edges):
        sample = np.random.random(no_real_edges)
        result = np.where(sample <= self.__ftrp)
        return len(result[0])

    def missing_neighbors_for_node(self, node):
        """
        Returns the nodes the given node is missing to be
        connected to all other ones along with their respective
        sigma
        :param node: hashable
        :return: list of 2-tuples
        """
        missing_neighbors = []
        existing_neighbors = self.node_neighbors(node)
        for node2 in self.nodes():
            if node != node2 and node2 not in existing_neighbors:
                sigma2 = self.get_node_sigma(node2)
                missing_neighbors.append((sigma2, node2))

        missing_neighbors.sort()
        return missing_neighbors

    def add_node_with_neighbors(self, node, neighbors):
        for neighbor in neighbors:
            self.add_edge(node1=node, node2=neighbor, real=True)

        node_sigma = self.get_node_sigma(node)
        if node_sigma < 1.0:
            no_real_edges = len(neighbors)
            no_fake_edges = self.number_of_fake_edges_to_add(no_real_edges)
            missing_neighbors = self.missing_neighbors_for_node(node)

            added_edges = 0
            for neighbor_sigma, missing_neighbor in missing_neighbors:
                # checks if missing edges have been added or if remaining
                # neighbors or node already have a sigma greater or equal to 1.0
                if added_edges >= no_fake_edges or neighbor_sigma >= 1.0 or node_sigma >= 1.0:
                    return

                self.add_edge(node1=node, node2=missing_neighbor, real=False)
                node_sigma = self.get_node_sigma(node)
                added_edges += 1

    def construct_graph(self, nx_graph):
        for node in nx_graph.nodes:
            neighbors = list(nx_graph.neighbors(node))

            # we do not want to deal with the case where
            # a node is not connected in the graph
            if len(neighbors) == 0:
                nx_graph.remove_node(node)
                continue

            self.add_node_with_neighbors(node, neighbors)

    # MARK: metrics
    def get_sigmas_profile(self):
        sigmas = self.get_graph_sigmas()
        mean = np.mean(sigmas)
        variance = np.var(sigmas)

        return mean, variance

    def get_uncertainty_profile(self):
        uncertainties = self.node_uncertainties()
        mean = np.mean(uncertainties)
        variance = np.var(uncertainties)

        return mean, variance

    def __get_centrality_metrics(self, centrality_algorithm):
        n_graph = nx.Graph(self.edges())
        if centrality_algorithm.__name__ == 'eigenvector_centrality':
            centrality_metric = centrality_algorithm(n_graph, max_iter=1000)
        else:
            centrality_metric = centrality_algorithm(n_graph)

        return centrality_metric

    def __get_centrality_profile(self, original_graph, centrality_algorithm):

        # obtaining metrics
        if centrality_algorithm.__name__ == 'eigenvector_centrality':
            original_metrics = centrality_algorithm(original_graph, max_iter=1000)
        else:
            original_metrics = centrality_algorithm(original_graph)

        noisy_metrics = self.__get_centrality_metrics(centrality_algorithm)

        # obtaining values
        original_values = list(original_metrics.values())
        noisy_values = list(noisy_metrics.values())

        # obtaining ordered keys
        original_keys = sorted(original_metrics, key=original_metrics.get)
        noisy_keys = sorted(noisy_metrics, key=noisy_metrics.get)

        # obtaining results
        distance = wasserstein_distance(original_values, noisy_values)
        correlation, _ = spearmanr(original_keys, noisy_keys)

        original_mean = np.mean(original_values)
        noisy_mean = np.mean(noisy_values)
        mean_change = abs(noisy_mean - original_mean) / original_mean

        return distance, correlation, mean_change

    def degree_centrality_profile(self, original_graph):
        return self.__get_centrality_profile(original_graph, centrality.degree_centrality)

    def betweenness_profile(self, original_graph):
        return self.__get_centrality_profile(original_graph, centrality.betweenness_centrality)

    def closeness_profile(self, original_graph):
        return self.__get_centrality_profile(original_graph, centrality.closeness_centrality)

    def eigenvector_centrality_profile(self, original_graph):
        return self.__get_centrality_profile(original_graph, centrality.eigenvector_centrality)
