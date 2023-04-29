import networkx as nx
import math
import graph.save as sv


def complete_graph(graph):
    # create a new graph to hold the complete graph with all the initial edges
    complete_G = graph.copy()

    # Init the gif
    name = "complete-algo"
    sv.init_gif(name)

    # iterate over all pairs of nodes
    for u in graph.nodes():
        for v in graph.nodes():
            if u != v and not graph.has_edge(u, v):
                # add an edge between the nodes if they are not already connected
                complete_G.add_edge(u, v)
                sv.save_screenshot(complete_G, name)

    #new_position = circular_layout(complete_G)
    #print(new_position)

    # Save the gif
    sv.create_gif_from_images(name)

    return complete_G


def circular_layout(G, center=None, scale=1):
    if center is None:
        # Compute the center point of the graph
        center = [sum([pos[0] for pos in G.nodes.values()]) / len(G),
                  sum([pos[1] for pos in G.nodes.values()]) / len(G)]

    positions = {}

    # Compute the polar coordinates of each node relative to the center point
    for node in G.nodes:
        x, y = G.nodes[node]['pos']
        dx, dy = x - center[0], y - center[1]
        r = math.sqrt(dx * dx + dy * dy)
        theta = math.atan2(dy, dx)
        positions[node] = (r, theta)

    # Sort the nodes based on their polar angle
    nodes_sorted = sorted(positions.keys(), key=lambda node: positions[node][1])

    # Assign new x and y coordinates to each node based on their polar coordinates
    for i, node in enumerate(nodes_sorted):
        r, theta = positions[node]
        positions[node] = (r * scale, 2 * math.pi * i / len(nodes_sorted))

    # Convert polar coordinates back to Cartesian coordinates
    for node in positions:
        r, theta = positions[node]
        x, y = center[0] + r * math.cos(theta), center[1] + r * math.sin(theta)
        positions[node] = (x, y)

    return positions


