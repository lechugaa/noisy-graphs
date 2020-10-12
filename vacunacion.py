import networkx as nx
import time
from negative_graphs.noisy_graph import NoisyGraph


if __name__ == '__main__':

    # timing execution
    t1 = time.perf_counter()

    # generating original graph
    print("Creating original graph...")
    graph = nx.barabasi_albert_graph(5500, 50, 200494)

    # creating noisy graph
    print("Creating noisy graph...")
    noisy_graph = NoisyGraph()
    noisy_graph.add_edges_from(graph.edges, real=True)

    # obtaining missing edges list
    print("Obtaining missing edges...")
    missing_edges = noisy_graph.concurrent_missing_edges()
    print(f"Number of missing edges: {len(missing_edges)}")

    # timing execution
    t2 = time.perf_counter()
    print()
    print(f"Execution time: {round(t2 - t1, 3)} second(s)")
