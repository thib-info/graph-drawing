import os
import json
import random
import networkx as nx


def generate_cycle_graph(n=10, seed=None):
    """
    Generates a simple cycle graph with n nodes.
    """
    if seed:
        random.seed(seed)
    G = nx.cycle_graph(n)
    data = nx.node_link_data(G)
    return data


def save_graph(graph_data, filename):
    """
    Saves the graph data to a JSON file with the specified filename.
    """
    if not os.path.exists('stocked-graph'):
        os.mkdir('stocked-graph')
    with open(os.path.join('stocked-graph', filename), 'w') as f:
        json.dump(graph_data, f)


def load_graph(filename):
    """
    Loads a graph from a JSON file with the specified filename.
    """
    with open(os.path.join('stocked-graph', filename), 'r') as f:
        data = json.load(f)
    return nx.node_link_graph(data)
