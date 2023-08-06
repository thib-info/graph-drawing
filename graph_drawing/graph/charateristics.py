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
        elif (u1, v1) == (u2, v2):
            # Ignore self-loops
            continue
        else:
            # Check for edge crossings
            x1, y1, x2, y2 = graph.nodes[u1]['pos'][0], graph.nodes[u1]['pos'][1], graph.nodes[v1]['pos'][0], graph.nodes[v1]['pos'][1]
            x1b, y1b, x2b, y2b = graph.nodes[u2]['pos'][0], graph.nodes[u2]['pos'][1], graph.nodes[v2]['pos'][0], graph.nodes[v2]['pos'][1]

            rico1 = (y2 - y1)/max((x2- x1), 0.000001)
            rico2 = (y2b - y1b)/max((x2b - x1b),0.000001)

            xcross = (y1b - y1 - rico2*x1b + rico1*x1)/max(rico1 - rico2, 0.0000001)

            if xcross < max(x1, x2) and xcross > min(x1, x2) and xcross < max(x1b, x2b) and xcross > min(x1b, x2b):
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
            (graph.nodes[u]['pos'][0] - graph.nodes[v]['pos'][0]) ** 2 + (graph.nodes[u]['pos'][1] - graph.nodes[v]['pos'][1]) ** 2)
    return total_length


    
def calculate_edge_length_metrics(graph):
    """
    Calculates the normalized avg edge lenght and normalized variance.
    """

    total_length, var = 0,0
    min_edge_length = math.inf
    num_of_edges = 0

    for u, v in graph.edges:
        edge_weight = graph.edges[u, v].get("weight", 1.0)  # default weight is 1.0
        edge_length = edge_weight * math.sqrt(
            (graph.nodes[u]['pos'][0] - graph.nodes[v]['pos'][0]) ** 2 + (graph.nodes[u]['pos'][1] - graph.nodes[v]['pos'][1]) ** 2)
        if edge_length < min_edge_length:
            min_edge_length = edge_length
        num_of_edges += 1
        
        total_length += edge_length
        var += edge_length**2

    ymax, ymin, xmax, xmin = 0, math.inf, 0, math.inf

    for u in graph.nodes:
        x = graph.nodes[u]['pos'][0]
        y = graph.nodes[u]['pos'][1]
        if x > xmax:
            xmax = x
        if x < xmin:
            xmin = x
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y

    frame_size = (xmax-xmin)*(ymax-ymin)
    frame_edge = math.sqrt(frame_size)

    return total_length/num_of_edges/frame_edge, var/num_of_edges/(frame_edge**2)
    #return total_length/num_of_edges/min_edge_length, var/num_of_edges/(min_edge_length**2)

def calculate_minimum_area(graph):
    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf

    for node in graph.nodes():
        x = graph.nodes[node]['pos'][0]
        y = graph.nodes[node]['pos'][1]
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

    #find min edge length
        
    min_el = math.inf
    for u,v in graph.edges():

        edge_length = math.sqrt((graph.nodes[u]['pos'][0] - graph.nodes[v]['pos'][0]) ** 2 + (graph.nodes[u]['pos'][1] - graph.nodes[v]['pos'][1]) ** 2)
        if edge_length < min_el:
            min_el = edge_length
    
    min_el = max(0.0000001, min_el)

    return width * height/(min_el**2)


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

    