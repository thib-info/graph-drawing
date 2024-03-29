import os
import json
import random
import networkx as nx
from inspect import signature


def addPosition(graph):
    for node, data in graph.nodes(data=True):
        x = random.random()
        y = random.random()
        data['pos'] = (x, y)


def addWeight(graph):
    for u, v in graph.edges():
        graph.edges[u, v]['weight'] = random.randint(1, 10)


def generate_goldner_harary_graph():
    """
    Generates a Goldner Hararay graph.
    """
    G= nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_node(8)
    G.add_node(9)
    G.add_node(10)

    G.add_edge(0,1)
    G.add_edge(0,2)
    G.add_edge(0,3)
    G.add_edge(0,4)
    G.add_edge(0,5)
    G.add_edge(0,6)
    G.add_edge(0,7)
    G.add_edge(0,10)

    G.add_edge(1,4)
    G.add_edge(1,5)
    G.add_edge(8,4)
    G.add_edge(8,5)

    G.add_edge(2,5)
    G.add_edge(2,6)
    G.add_edge(9,5)
    G.add_edge(9,6)

    G.add_edge(10,3)
    G.add_edge(10,4)
    G.add_edge(10,5)
    G.add_edge(10,6)
    G.add_edge(10,7)
    G.add_edge(10,8)
    G.add_edge(10,9)

    G.add_edge(3,4)
    G.add_edge(4,5)
    G.add_edge(5,6)
    G.add_edge(6,7)
    addPosition(G)

    data = nx.node_link_data(G)
    save_graph(data, 'goldner_harary_graph.json')

    return G

def generate_course_graph():
    
    G = nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)

    G.add_edge(0,1)
    G.add_edge(0,2)
    G.add_edge(0,3)
    G.add_edge(0,4)
    G.add_edge(0,5)
    G.add_edge(0,6)
    G.add_edge(0,7)
    G.add_edge(0,8)
    G.add_edge(0,9)
    G.add_edge(0,10)
    G.add_edge(0,11)

    G.add_edge(2,1)
    G.add_edge(3,1)
    G.add_edge(4,1)
    G.add_edge(5,1)
    G.add_edge(6,1)
    G.add_edge(7,1)
    G.add_edge(8,1)
    G.add_edge(9,1)
    G.add_edge(10,1)
    G.add_edge(11,1)
    addPosition(G)

    data = nx.node_link_data(G)
    save_graph(data, 'course_graph.json')

    return G

def generate_binary_tree():
    G= nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_node(8)
    G.add_node(9)
    G.add_node(10)

    G.add_edge(0,1)
    G.add_edge(1,2)
    G.add_edge(1,3)
    G.add_edge(2,4)
    G.add_edge(4,7)
    G.add_edge(4,8)
    G.add_edge(1,3)
    G.add_edge(3,5)
    G.add_edge(3,6)
    G.add_edge(5,9)
    G.add_edge(5,10)
    addPosition(G)

    data = nx.node_link_data(G)
    save_graph(data, 'binary_tree_graph.json')

    return G    

def generate_tertiary_tree():
    G= nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_node(8)
    G.add_node(9)

    G.add_edge(0,1)
    G.add_edge(0,2)
    G.add_edge(0,3)
    G.add_edge(1,4)
    G.add_edge(1,5)
    G.add_edge(1,6)
    G.add_edge(3,7)
    G.add_edge(3,8)
    G.add_edge(6,9)
    addPosition(G)

    data = nx.node_link_data(G)
    save_graph(data, 'tertiary_tree.json')

    return G

def generate_dodecahedral_graph():

    graph = nx.dodecahedral_graph()
    addPosition(graph)

    data = nx.node_link_data(graph)
    save_graph(data, 'dodecahedral_graph.json')

    return graph

def generate_cycle_graph(n=3, seed=None, weight=False, direction=False):
    """
    Generates a simple cycle graph with n nodes.
    """
    if seed is not None:
        random.seed(seed)

    if direction:
        graph = nx.cycle_graph(n, create_using=nx.DiGraph)
    else:
        graph = nx.cycle_graph(n, seed)

    addPosition(graph)
    if weight:
        addWeight(graph)

    data = nx.node_link_data(graph)
    save_graph(data, 'cycle_graph.json')

    return graph


def generate_tree_graph(n=3, seed=None, weight=False, direction=False):
    """
    Generates a simple tree graph with n nodes.
    """
    if seed is not None:
        random.seed(seed)

    if direction:
        graph = nx.random_tree(n, seed, create_using=nx.DiGraph)
    else:
        graph = nx.random_tree(n, seed)

    addPosition(graph)
    if weight:
        addWeight(graph)

    data = nx.readwrite.json_graph.node_link_data(graph)
    save_graph(data, 'tree_graph.json')

    return graph


def generate_bipartite_graph(num_vertices=3, num_edges=3, seed=None, weight=False, direction=False):
    """
    Generates a bipartite graph with given number of vertices and edges.
    """
    if seed is not None:
        random.seed(seed)

    num_left = num_vertices // 2
    left_nodes = range(num_left)
    right_nodes = range(num_left, num_vertices)
    edges = [(random.choice(left_nodes), random.choice(right_nodes)) for _ in range(num_edges)]

    if direction:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    graph.add_nodes_from(left_nodes, bipartite=0)
    graph.add_nodes_from(right_nodes, bipartite=1)
    graph.add_edges_from(edges)

    addPosition(graph)
    if weight:
        addWeight(graph)

    data = nx.readwrite.json_graph.node_link_data(graph)
    save_graph(data, 'bipartite_graph.json')

    return graph


def generate_outerplanar_graph(num_vertices=3, seed=None, weight=False, direction=False):
    """
    Generates an outerplanar graph with given number of vertices.
    """
    if seed is not None:
        random.seed(seed)

    if num_vertices <= 2:
        raise ValueError("Number of vertices must be greater than 2.")

    # Create a cycle graph with n-2 vertices
    if direction:
        graph = nx.cycle_graph(num_vertices - 2, create_using=nx.DiGraph)
    else:
        graph = nx.cycle_graph(num_vertices - 2, seed)

    # Add two new vertices connected to all previous vertices
    graph.add_node(num_vertices - 2)
    graph.add_node(num_vertices - 1)
    for i in range(num_vertices - 2):
        graph.add_edge(i, num_vertices - 2)
        graph.add_edge(i, num_vertices - 1)

    addPosition(graph)
    if weight:
        addWeight(graph)

    data = nx.readwrite.json_graph.node_link_data(graph)
    save_graph(data, 'outerplanar_graph.json')

    return graph


def generate_grid_graph(num_rows=2, num_cols=2, seed=None, weight=False, direction=False):
    """
    Generates a grid graph with given number of rows and columns.
    """
    if seed is not None:
        random.seed(seed)

    if direction:
        graph = nx.grid_2d_graph(num_rows, num_cols, create_using=nx.DiGraph)
    else:
        graph = nx.grid_2d_graph(num_rows, num_cols)

    # Rename nodes to have consecutive integers
    mapping = {(i, j): i * num_cols + j for i, j in graph.nodes()}
    graph = nx.relabel_nodes(graph, mapping)

    addPosition(graph)
    if weight:
        addWeight(graph)

    data = nx.readwrite.json_graph.node_link_data(graph)
    save_graph(data, 'grid_graph.json')

    return graph


def generate_complete_graph(n=3, seed=None, weight=False, direction=False):
    """
    Generates a simple complete graph with n nodes.
    """
    if seed is not None:
        random.seed(seed)

    if direction:
        graph = nx.complete_graph(n, create_using=nx.DiGraph)
    else:
        graph = nx.complete_graph(n, seed)

    addPosition(graph)
    if weight:
        addWeight(graph)

    data = nx.node_link_data(graph)
    save_graph(data, 'complete_graph.json')

    return graph


def generate_complex_graph(num_vertices=3, num_edges=2, num_graph_types=3, seed=None, weight=False, direction=False):
    """
    Generates a complex graph by combining multiple types of graphs.
    """
    if seed is not None:
        random.seed(seed)

    # Choose num_graph_types different graph generation functions randomly
    graph_funcs = []
    while len(graph_funcs) < num_graph_types:
        graph_func = random.choice([
            generate_cycle_graph, generate_tree_graph, generate_bipartite_graph, generate_outerplanar_graph,
            generate_grid_graph
        ])
        if graph_func not in graph_funcs:
            graph_funcs.append(graph_func)

    # Generate graphs using the chosen functions
    graphs = []
    for i in range(num_graph_types):
        num_args = len(signature(graph_funcs[i]).parameters)
        print("Type of graph selected: " + graph_funcs[i].__name__)

        # Pass the correct number of arguments to the function
        if num_args == 4:
            graph = graph_funcs[i](num_vertices, seed, weight, direction)
        elif num_args == 5:
            graph = graph_funcs[i](num_vertices, num_edges, seed, weight, direction)
        else:
            raise ValueError(f"Invalid number of arguments for graph function {graph_funcs[i].__name__}")

        graphs.append(graph)

    # Combine the generated graphs into one complex graph
    complex_graph = nx.disjoint_union_all(graphs)

    # Save the complex graph as JSON
    data = nx.readwrite.json_graph.node_link_data(complex_graph)

    save_graph(data, 'complex_graph.json')

    return complex_graph


def generate_atlas_graph(index=-1, weight=False):
    """
    Generation of a graph coming form the atlas: https://global.oup.com/academic/product/an-atlas-of-graphs-9780198526506?cc=fr&lang=en&
    Number of available graph: 1253

    !!! If you want a random graph specify -n -1 during the generation of the graph !!!
    """
    correct = True
    max_length = 1253
    if index <= -1 or index > 1253:
        print(
            "Your index is invalid and will be generated randomly\nRules to follow:\n1. Positive number\n2. Less than "
            "1253")
        correct = False

    if not correct:
        index = random.randint(1, max_length)

    graph = nx.classes.graph.Graph(nx.graph_atlas(index))

    addPosition(graph)
    if weight:
        addWeight(graph)

    # Save the complex graph as JSON
    data = nx.readwrite.json_graph.node_link_data(graph)
    save_graph(data, "atlas_graph.json")

    return graph


def save_graph(graph_data, filename):
    """
    Saves the graph data to a JSON file with the specified filename.
    """
    if not os.path.exists('./graph_drawing/stocked-graph'):
        os.mkdir('./graph_drawing/stocked-graph')
    with open(os.path.join('./graph_drawing/stocked-graph', filename), 'w') as f:
        json.dump(graph_data, f)


def load_graph(filename):
    """
    Loads a graph from a JSON file with the specified filename.
    """
    with open(os.path.join('./graph_drawing/stocked-graph', filename), 'r') as f:
        data = json.load(f)
    return nx.node_link_graph(data)
