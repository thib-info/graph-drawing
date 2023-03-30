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
