import networkx as nx
import graph.save as sv
from . import circular_layout as cl


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
    new_position = cl.circular_layout(complete_G)

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

