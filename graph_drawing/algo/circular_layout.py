import math


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
