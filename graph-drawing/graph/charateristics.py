import networkx as nx
import itertools
import math


def calculate_crossing_number(graph):
    """
    Calculates the crossing number of a graph with the Brute Force method.
    TODO: Implement a more optimize algorithm
    """

    # Iterate over all pairs of edges
    crossing_count = 0
    for (u1, v1), (u2, v2) in itertools.combinations(graph.edges(), 2):
        if u1 == u2 or u1 == v2 or v1 == u2 or v1 == v2:
            # Ignore adjacent edges
            continue
        if (u1, v1) == (u2, v2):
            # Ignore self-loops
            continue
        # Check for edge crossings
        if (u1 < u2 and v1 > v2 and (u1, v1) in graph[u2] and (u2, v2) in graph[v1]) \
                or (u2 < u1 and v2 > v1 and (u2, v2) in graph[u1] and (u1, v1) in graph[v2]):
            crossing_count += 1

    return crossing_count


def calculate_edge_length(graph):
    """
    Calculates the total edge length of a graph.
    """

    total_length = 0

    for u, v in graph.edges:
        edge_weight = graph.edges[u, v].get("weight", 1.0)  # default weight is 1.0
        total_length += edge_weight * math.sqrt(
            (graph.nodes[u]['x'] - graph.nodes[v]['x']) ** 2 + (graph.nodes[u]['y'] - graph.nodes[v]['y']) ** 2)
    return total_length


def calculate_minimum_area(graph):
    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf

    for node in graph.nodes():
        x = graph.nodes[node]['x']
        y = graph.nodes[node]['y']
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    width = max_x - min_x
    height = max_y - min_y
    return width * height


def is_symmetric(graph):
    """
    Check if a directed graph is symmetric.
    """
    if graph.is_directed:
        transpose = nx.reverse(graph.graph, copy=True)
        return nx.is_isomorphic(graph.graph, transpose)
    else:
        return False


def calculate_edge_bends(graph):
    """
    Calculates the number of bends or turns in each edge in the graph drawing.

    Args:
    - graph (networkx.DiGraph): The directed graph to analyze.

    Returns:
    - edge_bends (dict): A dictionary mapping each edge in the graph to the number of bends in the edge.
    """
    edge_bends = {}
    if graph.is_directed:
        for edge in graph.graph.edges():
            source = edge[0]
            target = edge[1]
            bends = 0
            path = nx.shortest_path(graph.graph, source=source, target=target)
            for i in range(len(path) - 2):
                u = path[i]
                v = path[i+1]
                w = path[i+2]
                if graph.graph.has_edge(u, w):
                    bends += 1
            edge_bends[edge] = bends

    return edge_bends


def calculate_compactness(graph):
    """
    Return a float between 0 and 1
    - 0 indicates the least compact (most spread out) layout
    - 1 indicates the most compact (most dense) layout
    """
    layout = nx.spring_layout(graph, seed=10)
    xs = [layout[node][0] for node in graph.nodes()]
    ys = [layout[node][1] for node in graph.nodes()]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    area = width * height
    perimeter = 2 * (width + height)
    compactness = area / math.pow(perimeter, 2)
    return compactness


def calculate_clustering(graph):
    # TODO: Check the correctness of the calculation here
    G = graph.graph

    if graph.is_directed is False:
        clustering_dict = nx.clustering(G)
        return sum(clustering_dict.values()) / len(clustering_dict)
    else:
        clustering_dict = nx.algorithms.cluster.clustering(G)
        clustering = sum(clustering_dict.values()) / len(G.nodes)
        return clustering

