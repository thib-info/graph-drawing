import os
import json
import random
import networkx as nx


def generate_cycle_graph(n=10, seed=None):
    """
    Generates a simple cycle graph with n nodes.
    """
    if seed is not None:
        random.seed(seed)

    graph = nx.cycle_graph(n)
    data = nx.node_link_data(graph)

    return data


def generate_tree_graph(n=10, seed=None):
    """
    Generates a simple tree graph with n nodes.
    """
    if seed is not None:
        random.seed(seed)

    graph = nx.random_tree(n)
    data = nx.readwrite.json_graph.node_link_data(graph)

    return data


def generate_bipartite_graph(num_vertices=10, num_edges=10, seed=None):
    """
    Generates a bipartite graph with given number of vertices and edges.
    """
    if seed is not None:
        random.seed(seed)

    num_left = num_vertices // 2
    left_nodes = range(num_left)
    right_nodes = range(num_left, num_vertices)
    edges = [(random.choice(left_nodes), random.choice(right_nodes)) for _ in range(num_edges)]

    graph = nx.Graph()
    graph.add_nodes_from(left_nodes, bipartite=0)
    graph.add_nodes_from(right_nodes, bipartite=1)
    graph.add_edges_from(edges)

    data = nx.readwrite.json_graph.node_link_data(graph)

    return data


def generate_outerplanar_graph(num_vertices=10, seed=None):
    """
    Generates an outerplanar graph with given number of vertices.
    """
    if seed is not None:
        random.seed(seed)

    if num_vertices <= 2:
        raise ValueError("Number of vertices must be greater than 2.")

    # Create a cycle graph with n-2 vertices
    graph = nx.cycle_graph(num_vertices - 2)

    # Add two new vertices connected to all previous vertices
    graph.add_node(num_vertices - 2)
    graph.add_node(num_vertices - 1)
    for i in range(num_vertices - 2):
        graph.add_edge(i, num_vertices - 2)
        graph.add_edge(i, num_vertices - 1)

    data = nx.readwrite.json_graph.node_link_data(graph)

    return data


def generate_grid_graph(num_rows=2, num_cols=5, seed=None):
    """
    Generates a grid graph with given number of rows and columns.
    """
    if seed is not None:
        random.seed(seed)

    graph = nx.grid_2d_graph(num_rows, num_cols)

    # Rename nodes to have consecutive integers
    mapping = {(i, j): i * num_cols + j for i, j in graph.nodes()}
    graph = nx.relabel_nodes(graph, mapping)

    data = nx.readwrite.json_graph.node_link_data(graph)

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
