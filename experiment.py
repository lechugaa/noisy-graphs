import argparse
from noisy_graphs.noisy_graph import NoisyGraph


def parse_cl_arguments():
    description = "This script performs an experiment of the noisy graph construction algorithm."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--graph-type", help="Select a stochastic graph type: ER (Erdős-Rényi), WS (Watts–Strogatz) or BA (Barabási–Albert).")
    parser.add_argument("-n", "--graph-size", help="Set the number of nodes of the graph.")
    parser.add_argument("-r", "--ftrp", help="Set the real-to-fake edges proportion.")
    parser.add_argument("-p", "--probability", help="Set the probability for edge creation for ER or rewiring each edge for WS.")
    parser.add_argument("-k", "--ring-neighbors", help="For WS each node is joined with its k nearest neighbors in a ring topology.")
    parser.add_argument("-m", "--new-node-edges", help="For BA set the number of edges to attach from a new node to existing nodes.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_cl_arguments()
    print(args.graph_size)
