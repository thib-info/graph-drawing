def is_planar_DMP(graph):
    # Make a copy of the graph so that we can modify it without changing the original
    H = graph.copy()

    # While the graph has more than 3 vertices
    while len(H) > 3:
        # Find a vertex of degree <= 2
        v = None
        for node in H.nodes():
            if H.degree(node) <= 2:
                v = node
                break

        # If no such vertex exists, the graph is not planar
        if v is None:
            return False

        # Remove the vertex and its incident edges
        H.remove_node(v)

    # If the resulting graph has at most 3 vertices, it is planar
    return True
