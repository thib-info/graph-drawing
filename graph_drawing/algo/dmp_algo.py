import os

import networkx
import numpy
from matplotlib import pyplot as plt

import graph.save as sv
import networkx as nx
import graph.factory as factory


def is_planar_DMP(graph, save):
    """
    DMP algorithm implementation to check if a given graph is planar or not.
    The save option is the name of the pdf where to save each iteration of the algo.
    If save = None, then we don't want to save. Otherwise, we save it.
    """
    # Make a copy of the graph so that we can modify it without changing the original
    H = graph.copy()
    name = "dmp-gif"

    # Create the pdf if the save if defined
    pdf = None
    if save is not None:
        pdf = sv.create_pdf_page(save + '-dmpAlgo')

    # Init the gif
    sv.init_gif(name)

    # While the graph has more than 3 vertices
    while len(H) > 3:
        # Save the screenshot of the current graph
        sv.save_screenshot(H, name)

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

    # Create the GIF
    sv.create_gif_from_images(name)

    # If the resulting graph has at most 3 vertices, it is planar
    return True


def select_cycle_graph(graph):
    cycles = nx.cycle_basis(graph)
    cycle = None
    for i, c in enumerate(cycles):
        if c[0] == 2 and c[1] == 3:
            cycle = c

    # cycle = cycles[0]  # Choose the first cycle found
    G_prime = graph.subgraph(cycle).copy()
    nx.set_node_attributes(G_prime, nx.get_node_attributes(graph, 'pos'), 'pos')

    return G_prime


def get_face_cycle(subGraph):
    D = nx.DiGraph(subGraph)
    for u, v in subGraph.edges():
        D.add_edge(u, v)
        D.add_edge(v, u)

    cycles = nx.simple_cycles(D)

    faces = []
    max_length = 3
    for c in cycles:
        if len(c) == 3:
            c.sort()
            if c not in faces:
                faces.append(c)
        elif len(c) > 3:
            max_length = len(c)

    if max_length == 3:
        faces.insert(0, faces[0])
        return faces

    cycles = nx.simple_cycles(D)
    for c in cycles:
        if len(c) == max_length:
            c.sort()
            if c not in faces:
                faces.insert(0, c)

    return faces


def get_face(subGraph):
    nodes = [-1]
    for n in subGraph.nodes:
        nodes.append(n)
    nodes.sort()

    faces = [nodes]
    for node in subGraph.nodes:
        face = [node]
        links = subGraph.edges(node)
        stop = False
        for link in links:
            if stop:
                break
            node_des = link[1]
            edges_des = subGraph.edges(node_des)
            for inter_link in edges_des:
                inter_des = inter_link[1]
                if (node_des, inter_des) in edges_des and inter_des != node:
                    if link[1] not in face:
                        face.append(link[1])
                    if len(face) == 3:
                        stop = True
        face.sort()
        if face not in faces:
            faces.append(face)

    faces[0].pop(0)

    return faces


def get_fragment(graph, subgraph):
    sub_nodes = subgraph.nodes
    subg_edge = subgraph.edges

    # Get all the edges to use to form our fragments
    links = set()
    for sub_node in sub_nodes:
        for graph_edge in graph.edges:
            if graph_edge not in subg_edge:
                links.add(graph_edge)
                if graph_edge[0] == sub_node or graph_edge[1] == sub_node:
                    if graph_edge not in links:
                        links.add(graph_edge)

    # Get the nodes not in the subgraph
    n_not_in_subg = set()
    for node in graph.nodes:
        if node not in sub_nodes:
            n_not_in_subg.add(node)

    # Get the links between the nodes exclude from the graph
    groups = []
    for node_src in n_not_in_subg:
        sub_group = []
        for node_dst in n_not_in_subg:
            for edge in graph.edges:
                if edge[0] == node_src and edge[1] == node_dst:
                    sub_group.append(node_src)
                    sub_group.append(node_dst)

        for group in groups:
            if node_src in group:
                break
            elif len(sub_group) == 0:
                sub_group.append(node_src)

        if len(groups) == 0:
            if len(sub_group) == 0:
                sub_group.append(node_src)

        if len(sub_group) != 0:
            groups.append(sub_group)

    # Now we need to create the fragments
    fragments = []
    for group in groups:
        sub_frag = []
        for node in group:
            for edges in links:
                if node in edges:
                    sub_frag.append(edges)
        fragments.append(sub_frag)

    # Get the single edges fragment
    for link in links:
        add = True
        for nNot in n_not_in_subg:
            if link[0] == nNot or link[1] == nNot:
                add = False
        if add:
            fragments.append([link])

    # Create all the fragments now
    frag_graph = []
    for frag in fragments:
        F = nx.Graph()
        for e in frag:
            F.add_edge(e[0], e[1])
        frag_graph.append(F)

    return frag_graph


def admissible_face(subGraph, faces, fragments):
    nodes = []
    for node in subGraph.nodes:
        nodes.append(node)

    adm_face = []
    for fragment in fragments:
        inter_adm_face = []
        for face in faces:
            if not isinstance(face, networkx.classes.reportviews.NodeView):
                f_nodes = []
                for n in fragment.nodes:
                    f_nodes.append(n)

                inter = set(nodes).intersection(f_nodes)
                inter2 = set(inter).intersection(face)

                if len(inter) == len(inter2):
                    inter_adm_face.append(face)

        adm_face.append(inter_adm_face)

    return adm_face


def print_fragment(frag):
    nbr_frag = len(frag)
    if nbr_frag == 1:
        fig, axs = plt.subplots(1, 3)
    elif nbr_frag == 2:
        fig, axs = plt.subplots(1, 2)
    elif nbr_frag == 3:
        fig, axs = plt.subplots(1, 3)
    else:
        fig, axs = plt.subplots(1, 2)

    if nbr_frag >= 1:
        nx.draw(frag[0], with_labels=True, ax=axs[0])
        axs[0].set_title("Fragment n°" + str(0))
        if nbr_frag >= 2:
            nx.draw(frag[1], with_labels=True, ax=axs[1])
            axs[1].set_title("Fragment n°" + str(1))
            if nbr_frag >= 3:
                nx.draw(frag[2], with_labels=True, ax=axs[2])
                axs[2].set_title("Fragment n°" + str(2))

    # adjust the spacing between the subplots
    plt.subplots_adjust(wspace=1.5)
    name_frag = "dmp-algo-planar-embedding-frag"
    nbrElem = len(os.listdir("./graph_drawing/stocked-graph/" + name_frag))
    fig.savefig("./graph_drawing/stocked-graph/" + name_frag + "/screenshot-" + str(nbrElem))
    plt.close(fig)

    # show the plot
    # plt.show()


def get_alpha_path(subGraph, fragment):
    subGraph_nodes = list(subGraph.nodes)
    frag_nodes = list(fragment.nodes)

    dif = []
    for fn in frag_nodes:
        is_in = False
        for sbn in subGraph_nodes:
            if sbn == fn:
                is_in = True
        if not is_in:
            dif.append(fn)

    return dif


def apply_pos(graph):
    pos = nx.spring_layout(graph)
    for n in graph.nodes:
        for p in pos:
            if n == p:
                if isinstance(pos[p], numpy.ndarray):
                    graph.nodes[n]['pos'] = [pos[p][0], pos[p][1]]
                else:
                    graph.nodes[n]['pos'] = pos[p]

    pos = nx.planar_layout(graph)
    for n in graph.nodes:
        for p in pos:
            if n == p:
                if isinstance(pos[p], numpy.ndarray):
                    graph.nodes[n]['pos'] = [pos[p][0], pos[p][1]]
                else:
                    graph.nodes[n]['pos'] = pos[p]

    return graph


def plot_subgraph(graph):
    pos = {int(n): data['pos'] for n, data in graph.nodes(data=True)}
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightblue', edge_color='black', width=2, alpha=0.8)

    #nx.draw(graph, with_labels=True, connectionstyle="arc3,rad=0.4", pos=pos)

    # plot the first graph on the first subplot
    # nx.draw(graph, with_labels=True)

    plt.show()


def dmp_planar_embedding(graph):
    # Copy of the given graph to make all the modifications
    H = graph.copy()

    name = "dmp-algo-planar-embedding"
    sv.init_gif(name)

    name_frag = "dmp-algo-planar-embedding-frag"
    sv.init_gif(name_frag)

    # Step 1: Choose a cycle of G to get a planar graph G'
    subGraph = select_cycle_graph(H)
    sv.save_screenshot(subGraph, name)

    # Add the position to the node of the subGraph
    for n in H.nodes():
        for ns in subGraph.nodes:
            if n == ns:
                subGraph.nodes[ns]['pos'] = H.nodes[n]['pos']

    nbr_turn = 0
    while True:
        # Step 2: Get all the faces of the cycle
        faces = get_face_cycle(subGraph)

        # Step 3: Get the fragments of the current cycle
        fragment = get_fragment(graph, subGraph)

        if len(fragment) == 0:
            if nbr_turn == 0:
                print("The given graph contains only one cycle")
                print("Here is a planar embedding of the graph")
                return apply_pos(subGraph)

            print("Dmp algo well implemented")
            # Save the gif
            sv.create_gif_from_images(name)
            break

        # Step 4: Compute the valid faces
        adm_faces = admissible_face(subGraph, faces, fragment)

        ind = 0
        restart = False
        for adm_face in adm_faces:
            if len(adm_face) == 0:
                print("The graph is not planar")
                return False
            if len(adm_face) == 1:
                if len(fragment[ind].edges()) == 1:
                    n_to_add = list(fragment[ind].nodes)
                    subGraph.add_edge(n_to_add[0], n_to_add[1])
                    restart = True
                    subGraph = apply_pos(subGraph)
                    sv.save_screenshot(subGraph, name)
                    continue
            ind += 1

        if restart:
            continue

        # Step 5: Choose a fragment
        picked_frag_ind = 0
        picked_frag = fragment[picked_frag_ind]

        # Get the alpha-path
        alpha_path = get_alpha_path(subGraph, picked_frag)
        alpha_path = alpha_path[0]

        # Add it to the graph
        picked_face = adm_faces[picked_frag_ind][1]

        subGraph.add_edge(alpha_path, picked_face[1])
        subGraph.add_edge(alpha_path, picked_face[2])

        # Step where we determined the new position for planar embedding
        subGraph = apply_pos(subGraph)
        sv.save_screenshot(subGraph, name)
        nbr_turn += 1

    data = nx.node_link_data(subGraph)
    factory.save_graph(data, 'dmp_graph_algo.json')

    sv.create_gif_from_images(name_frag)

    return subGraph
