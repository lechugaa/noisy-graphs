import networkx as nx
from negative_graphs.noisy_graph import NoisyGraph
from networkx.algorithms.centrality import group_betweenness_centrality, group_degree_centrality
from networkx.algorithms.dominating import dominating_set


if __name__ == '__main__':

    original_ws = nx.watts_strogatz_graph(50, 5, 0.1)
    ws_dom_set = dominating_set(original_ws)
    print(f"Number of nodes in dominating set {len(ws_dom_set)}")

    noisy_ws = NoisyGraph()
    noisy_ws.add_edges_from(original_ws.edges, real=True)
    missing_edges = noisy_ws.missing_edges()
    print(f"Number of missing edges {len(missing_edges)}")

    print('fraction, dom_group_centrality, graph_uncertainty, mean_uncertainty, std_dev_uncertainty')
    for i in range(101):
        fraction = i / 100
        noisy_ws.add_random_missing_edges(fraction)
        modified_ws = nx.Graph(noisy_ws.edges())

        dom_group_centrality = group_degree_centrality(modified_ws, ws_dom_set)
        graph_uncertainty = noisy_ws.uncertainty()
        mean_uncertainty, std_dev_uncertainty = noisy_ws.uncertainty_profile()
        print(f'{fraction}, {dom_group_centrality}, {graph_uncertainty}, {mean_uncertainty}, {std_dev_uncertainty}')

        noisy_ws.clear_fake_edges()
