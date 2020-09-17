import networkx as nx


from entropy import entropy, entropy_change, entropy_change_list


if __name__ == '__main__':

    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])

    print('---------------Calculating Entropy---------------')
    G.add_edges_from([(0, 1), (0, 3), (1, 3)])
    print(f'Entropy: {entropy(G):.4f}')

    G.add_edge(2, 3)
    print(f'Entropy: {entropy(G):.4f}')

    G.add_edge(0, 2)
    print(f'Entropy: {entropy(G):.4f}')

    G.add_edge(1, 2)
    print(f'Entropy: {entropy(G):.4f}')

    print('---------------Entropy Change---------------')
    H = nx.Graph()
    H.add_nodes_from([0, 1, 2, 3])
    H.add_edges_from([(0, 1), (0, 3), (1, 3)])
    print(f'Entropy change: {entropy_change(H, (2, 3)):.4f}')

    print('-------------Entropy Change List------------')
    deltas = entropy_change_list(H)
    for delta in deltas:
        print(f'Edge {delta[0]} changes entropy by {delta[1]:.4f}')

    print('------------Smallworld Change List----------')
    ws = nx.watts_strogatz_graph(15, 3, 0.5)
    ws_entropy = entropy(ws)
    print(f'Entropy: {ws_entropy:.4f}')
    ws_deltas = entropy_change_list(ws)
    for delta in ws_deltas:
        print(f'Edge {delta[0]} changes entropy by {delta[1]:.4f}')
