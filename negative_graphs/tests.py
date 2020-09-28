import statistics
import unittest
from math import log
from negative_graphs.noisy_graph import NoisyGraph


class NoisyGraphTest(unittest.TestCase):
    def setUp(self):
        self.empty_graph = NoisyGraph()

        self.disconnected_hexagon = NoisyGraph()
        self.disconnected_hexagon.add_nodes_from([0, 1, 2, 3, 4, 5])

        self.noisy_hexagon = NoisyGraph()
        self.noisy_hexagon.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)], True)
        self.noisy_hexagon.add_edges_from([(0, 2), (2, 4), (0, 4), (1, 3), (3, 5), (1, 5)], False)

        self.incomplete_graph = NoisyGraph()
        self.incomplete_graph.add_edges_from([(0, 1), (1, 2), (1, 3), (3, 4)], True)

    def test_empty_graph_nodes(self):
        assert self.empty_graph.number_of_nodes() == 0

    def test_node_addition_number_increase(self):
        self.empty_graph.add_node(0)
        assert self.empty_graph.number_of_nodes() == 1

    def test_multiple_node_addition_number_increase(self):
        self.empty_graph.add_nodes_from([0, 1, 2, 3, 4])
        assert self.empty_graph.number_of_nodes() == 5

    def test_node_addition(self):
        self.empty_graph.add_node(0)
        self.assertTrue(0 in self.empty_graph.nodes())

    def test_multiple_node_addition(self):
        node_list = [0, 1, 2, 3, 4]
        self.empty_graph.add_nodes_from(node_list)
        for node in node_list:
            self.assertTrue(node in self.empty_graph.nodes())

    def test_real_edge_addition(self):
        self.disconnected_hexagon.add_edge(0, 1, real=True)
        real, fake, total = self.disconnected_hexagon.number_of_edges()
        assert real == 1
        assert fake == 0
        assert total == 1
        self.assertTrue((0, 1) in self.disconnected_hexagon.edges())
        self.assertFalse((1, 0) in self.disconnected_hexagon.edges())
        self.assertTrue((0, 1) in self.disconnected_hexagon.edges_if(True))
        self.assertFalse((0, 1) in self.disconnected_hexagon.edges_if(False))

    def test_fake_edge_addition(self):
        self.disconnected_hexagon.add_edge(2, 3, real=False)
        real, fake, total = self.disconnected_hexagon.number_of_edges()
        assert real == 0
        assert fake == 1
        assert total == 1
        self.assertTrue((2, 3) in self.disconnected_hexagon.edges())
        self.assertFalse((3, 2) in self.disconnected_hexagon.edges())
        self.assertTrue((2, 3) in self.disconnected_hexagon.edges_if(False))
        self.assertFalse((2, 3) in self.disconnected_hexagon.edges_if(True))

    def test_multiple_edge_addition(self):
        real_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)]
        fake_edges = [(0, 2), (2, 4), (0, 4), (1, 3), (3, 5), (1, 5)]
        self.disconnected_hexagon.add_edges_from(real_edges, real=True)
        self.disconnected_hexagon.add_edges_from(fake_edges, real=False)
        real, fake, total = self.disconnected_hexagon.number_of_edges()
        assert real == 6
        assert fake == 6
        assert total == 12
        for edge in real_edges:
            self.assertTrue(edge in self.disconnected_hexagon.edges())
            self.assertTrue(edge in self.disconnected_hexagon.edges_if(True))
            self.assertFalse(edge in self.disconnected_hexagon.edges_if(False))
        for edge in fake_edges:
            self.assertTrue(edge in self.disconnected_hexagon.edges())
            self.assertTrue(edge in self.disconnected_hexagon.edges_if(False))
            self.assertFalse(edge in self.disconnected_hexagon.edges_if(True))

    def test_edge_addition_without_nodes(self):
        self.empty_graph.add_edge(0, 1, True)
        self.empty_graph.add_edge(1, 2, False)
        assert self.empty_graph.number_of_nodes() == 3
        for node in [0, 1, 2]:
            self.assertTrue(node in self.empty_graph.nodes())
        self.assertTrue((0, 1) in self.empty_graph.edges())
        self.assertTrue((1, 2) in self.empty_graph.edges())
        self.assertTrue((0, 1) in self.empty_graph.edges_if(True))
        self.assertTrue((1, 2) in self.empty_graph.edges_if(False))
        self.assertFalse((0, 1) in self.empty_graph.edges_if(False))
        self.assertFalse((1, 2) in self.empty_graph.edges_if(True))

    def test_adjacency(self):
        real_adjacency = [(0, 1), (0, 1)]
        fake_adjacency = [(0, 2), (0, 4)]
        for edge in real_adjacency:
            self.assertTrue(edge in self.noisy_hexagon.node_adjacency(0))
            self.assertTrue(edge in self.noisy_hexagon.node_adjacency_if(0, True))
            self.assertFalse(edge in self.noisy_hexagon.node_adjacency_if(0, False))
        for edge in fake_adjacency:
            self.assertTrue(edge in self.noisy_hexagon.node_adjacency(0))
            self.assertTrue(edge in self.noisy_hexagon.node_adjacency_if(0, False))
            self.assertFalse(edge in self.noisy_hexagon.node_adjacency_if(0, True))

    def test_number_of_edges_for_node(self):
        for node in self.noisy_hexagon.nodes():
            real, fake, total = self.noisy_hexagon.number_of_edges_for_node(node)
            assert real == 2
            assert fake == 2
            assert total == 4

    def test_number_of_edges_for_non_existent_node(self):
        self.assertTrue(self.noisy_hexagon.number_of_edges_for_node(10) is None)

    def test_exact_uncertainty(self):
        for node in self.noisy_hexagon.nodes():
            node_uncertainty = self.noisy_hexagon.node_uncertainty(node)
            self.assertEqual(node_uncertainty, log(6, 2))

        graph_uncertainty = self.noisy_hexagon.uncertainty()
        self.assertEqual(graph_uncertainty, log(924, 2))

    def test_inexact_uncertainty(self):
        for node in self.noisy_hexagon.nodes():
            node_uncertainty = self.noisy_hexagon.node_uncertainty(node, exact=False)
            self.assertEqual(node_uncertainty, log(11, 2))

        graph_uncertainty = self.noisy_hexagon.uncertainty(exact=False)
        self.assertEqual(graph_uncertainty, log(2510, 2))

    def test_number_uncertainty_for_non_existent_node(self):
        self.assertTrue(self.noisy_hexagon.node_uncertainty(10) is None)

    def test_node_uncertainties(self):
        uncertainties = [log(6, 2) for _ in self.noisy_hexagon.nodes()]
        self.assertEqual(uncertainties, self.noisy_hexagon.node_uncertainties())

    def test_uncertainty_profile(self):
        uncertainties = [log(6, 2) for _ in self.noisy_hexagon.nodes()]
        mean = statistics.mean(uncertainties)
        std_dev = statistics.pstdev(uncertainties)
        self.assertEqual((mean, std_dev), self.noisy_hexagon.uncertainty_profile())

    def test_missing_edges_for_node(self):
        missing_edges_dict = {
            0: [(0, 2), (0, 3), (0, 4)],
            1: [(1, 4)],
            2: [(0, 2), (2, 3), (2, 4)],
            3: [(0, 3), (2, 3)],
            4: [(0, 4), (1, 4), (2, 4)]
        }

        for node, edges in missing_edges_dict.items():
            missing_edges = self.incomplete_graph.missing_edges_for_node(node)
            assert len(missing_edges) == len(edges)
            for edge in edges:
                self.assertTrue(edge in missing_edges)

    def test_missing_edges_for_graph(self):
        missing_edges = [(0, 2), (0, 3), (0, 4), (1, 4), (2, 3), (2, 4)]
        graph_missing_edges = self.incomplete_graph.missing_edges()

        self.assertTrue(len(missing_edges) == len(graph_missing_edges))
        for edge in graph_missing_edges:
            self.assertTrue(edge in missing_edges)

    def test_random_missing_edges(self):
        missing_edges = {(0, 2), (0, 3), (0, 4), (1, 4), (2, 3), (2, 4)}
        graph_missing_edges = set(self.incomplete_graph.random_missing_edges(0.5))
        self.assertTrue(len(missing_edges.intersection(graph_missing_edges)) == 3)

    def test_add_random_missing_edges(self):
        missing_edges = {(0, 2), (0, 3), (0, 4), (1, 4), (2, 3), (2, 4)}
        fake_edges = set(self.incomplete_graph.edges_if(False))
        self.assertTrue(len(missing_edges.intersection(fake_edges)) == 0)

        self.incomplete_graph.add_random_missing_edges(0.5)
        fake_edges = set(self.incomplete_graph.edges_if(False))
        self.assertTrue(len(missing_edges.intersection(fake_edges)) == 3)


if __name__ == '__main__':
    unittest.main()
