import networkx as nx
from noisy_graphs.noisy_graph import NoisyGraph


def create_data_path_file(data_path: str):
    header = "exp_name,sigma_mean,sigma_variance,uncertainty_mean,uncertainty_variance,dc_distance," \
             "dc_correlation,dc_mean_change,bc_distance,bc_correlation,bc_mean_change,cc_distance," \
             "cc_correlation,cc_mean_change,ec_distance,ec_correlation,ec_mean_change\n"
    f = open(data_path, "w")
    f.write(header)
    f.close()


def perform_experiment(original_graph: nx.Graph, ftrp: float, exp_name: str, data_path: str):
    print(exp_name)

    # removing graph isolates
    # NoisyGraph is not intended to deal with isolated nodes
    original_graph.remove_nodes_from(list(nx.isolates(original_graph)))

    # constructing noisy graph
    noisy_graph = NoisyGraph(ftrp=ftrp)
    noisy_graph.construct_graph(original_graph)

    # algorithm compliance
    sigma_mean, sigma_variance = noisy_graph.get_sigmas_profile()

    # uncertainty
    uncertainty_mean, uncertainty_variance = noisy_graph.get_uncertainty_profile()

    # centrality_metrics
    dc_distance, dc_correlation, dc_mean_change = noisy_graph.degree_centrality_profile(original_graph)
    bc_distance, bc_correlation, bc_mean_change = noisy_graph.betweenness_profile(original_graph)
    cc_distance, cc_correlation, cc_mean_change = noisy_graph.closeness_profile(original_graph)
    ec_distance, ec_correlation, ec_mean_change = noisy_graph.eigenvector_centrality_profile(original_graph)

    # create raw file with original edges and noisy edges
    f = open(f"raw_data/{exp_name[:2]}.txt", "a")
    f.write(f"Experimental conditions: {exp_name}\n")
    f.write(f"Real edges: {noisy_graph.edges_if(real=True)}\n")
    f.write(f"Fake edges: {noisy_graph.edges_if(real=False)}\n\n")
    f.close()

    # add result to csv
    result = f"{exp_name},{sigma_mean},{sigma_variance},{uncertainty_mean},{uncertainty_variance},"
    result += f"{dc_distance},{dc_correlation},{dc_mean_change},"
    result += f"{bc_distance},{bc_correlation},{bc_mean_change},"
    result += f"{cc_distance},{cc_correlation},{cc_mean_change},"
    result += f"{ec_distance},{ec_correlation},{ec_mean_change}"
    result += "\n"

    f = open(data_path, "a")
    f.write(result)
    f.close()
