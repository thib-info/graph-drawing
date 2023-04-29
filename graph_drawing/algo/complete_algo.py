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

    # Load the new position for a circular layout
    new_position = circular_layout(complete_G)

    # Change one by one the position of each nodes to get a nice visualization of the process
    transition_pos = {}
    ind = 0
    for node in complete_G.nodes():
        x, y = complete_G.nodes[node]['pos']
        transition_pos[ind] = (x, y)
        ind += 1

    i = 0
    for pos in new_position:
        transition_pos[i] = new_position[pos]
        nx.set_node_attributes(complete_G, transition_pos, 'pos')
        sv.save_screenshot(complete_G, name)
        i += 1

    nx.set_node_attributes(complete_G, new_position, 'pos')
    sv.save_screenshot(complete_G, name)

    # Save the gif
    sv.create_gif_from_images(name)

    return complete_G


def circular_layout(G, center=None, scale=1):
    # Compute the center point of the graph
    x_sum = 0
    y_sum = 0
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        x_sum += x
        y_sum += y
    center = [x_sum / len(G), y_sum / len(G)]

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

