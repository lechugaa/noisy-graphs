import networkx as nx
from noisy_graph import NoisyGraph


if __name__ == '__main__':
    hex_real_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
    hex_false_edges = [(0, 2), (2, 4), (4, 0), (1, 3), (3, 5), (5, 1)]

    noisy_hex = NoisyGraph(hex_real_edges)
    noisy_hex.add_edges_from(hex_false_edges, real=False)
    print(f'All edges: {noisy_hex.get_edges()}')
    print(f'Real edges: {noisy_hex.get_edges(real=True)}')
    print(f'False edges: {noisy_hex.get_edges(real=False)}')

    print(f'Graph uncertainty: {noisy_hex.uncertainty()} bits')
    print(f'Nodes uncertainty: {noisy_hex.node_uncertainties()}')

    hex_mean, hex_stdv = noisy_hex.uncertainty_profile()
    print(f'Mean: {hex_mean}, Standard deviation: {hex_stdv}')

    noisy_hex.add_edge(0, 3, real=False)
    print(f'Graph uncertainty: {noisy_hex.uncertainty()} bits')
    print(f'Nodes uncertainty: {noisy_hex.node_uncertainties()}')
    hex_mean, hex_stdv = noisy_hex.uncertainty_profile()
    print(f'Mean: {hex_mean}, Standard deviation: {hex_stdv}')

    ws = nx.watts_strogatz_graph(30, 3, 0.1)
    noisy_ws = NoisyGraph(ws.edges)
    print(f'Graph uncertainty: {noisy_ws.uncertainty()}')
    print(f'Node uncertainty (mean, stdev): {noisy_ws.uncertainty_profile()}')

    random_noise_graph = nx.watts_strogatz_graph(30, 10, 0.5)
    noisy_edges = [edge for edge in random_noise_graph.edges if edge not in noisy_ws.get_edges(real=True)]
    noisy_ws.add_edges_from(noisy_edges, real=False)
    print(f'Graph uncertainty: {noisy_ws.uncertainty()}')
    print(f'Node uncertainty (mean, stdev): {noisy_ws.uncertainty_profile()}')
