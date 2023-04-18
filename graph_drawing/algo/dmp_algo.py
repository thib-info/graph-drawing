import graph.save as sv


def is_planar_DMP(graph, save):
    """
    DMP algorithm implementation to check if a given graph is planar or not.
    The save option is the name of the pdf where to save each iteration of the algo.
    If save = None, then we don't want to save. Otherwise, we save it.
    """
    # Make a copy of the graph so that we can modify it without changing the original
    H = graph.copy()

    # Create the pdf if the save if defined
    pdf = None
    if save is not None:
        pdf = sv.create_pdf_page(save + '-dmpAlgo')

    # While the graph has more than 3 vertices
    while len(H) > 3:
        # Find a vertex of degree <= 2
        v = None
        for node in H.nodes():
            if H.degree(node) <= 2:
                v = node
                break

        if save is not None:
            sv.save_pdf(H, pdf)

        # If no such vertex exists, the graph is not planar
        if v is None:
            return False

        # Remove the vertex and its incident edges
        H.remove_node(v)

    if pdf is not None:
        sv.close_pdf_page(pdf)

    # If the resulting graph has at most 3 vertices, it is planar
    return True
