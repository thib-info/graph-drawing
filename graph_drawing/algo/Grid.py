import networkx as nx
import math
import matplotlib.pyplot as plt
import graph.Graph 
from algo.dmp_algo import dmp_planar_embedding
import graph.factory as f
import numpy
import graph.charateristics as c


def get_pos(G):
    '''
    Get the position of the nodes in graph G
    '''

    print(G.graph)
    pos = {}
    for node, data in G.graph.nodes(data=True):
        pos[node] = data['pos']

    return pos

def get_posH(H):

    pos = {}
    for node, data in H.nodes(data=True):
        pos[node] = data['pos']

    return pos

def apply_pos(G):
    pos = nx.planar_layout(G)
    for n in G.nodes:
        for p in pos:
            if n == p:
                if isinstance(pos[p], numpy.ndarray):
                    G.nodes[n]['pos'] = [pos[p][0], pos[p][1]]
                else:
                    G.nodes[n]['pos'] = pos[p]
    return G


def canonical(G):
    H = G.copy()

    k = G.number_of_nodes()
    pos = get_posH(G)
    #pos = nx.planar_layout(H)

    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf


    for node in G.nodes():
        x = pos[node][0]
        y = pos[node][1]
        if x < min_x:
            min_x = x
            left = node
        if x > max_x:
            max_x = x
            right = node
        if y < min_y:
            min_y = y
            low = node
        if y > max_y:
            max_y = y
            high = node
        
    u1 = left
    if right == high:
        u2 = low
        w = right
    if left == high:
        u2 = low
        w = right
    if left != high and right != high:
        u2 = right
        w = high

    ext = [u1, u2, w]
    order = [None]*k
    order[0] = u1
    order[1] = u2
    order[k-1] = w
    ext.remove(w)

    
    for u in H.neighbors(w):
        if u not in ext:
            ext.append(u)

    fig, ax = plt.subplots()
    nx.draw(H, pos = get_posH(H), with_labels=True, font_weight='bold') 
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.axis('on')
    plt.grid('on')                 
    plt.show()
    H.remove_node(w)
    fig, ax = plt.subplots()
    nx.draw(H, pos = get_posH(H), with_labels=True, font_weight='bold')
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.axis('on')
    plt.grid('on')                  
    plt.show()
    


    for i in range(k-1, 2, -1):
        for j in ext:
            if j != u1 and j != u2:
                a = [n for n in H.neighbors(j)]
                if len(set(a).intersection(ext)) == 2:
                    order[i-1] = j
                    ext.remove(j)
                    for u in H.neighbors(j):
                        if u not in ext:
                            ext.append(u)
                    H.remove_node(j)
                    fig, ax = plt.subplots()
                    nx.draw(H, pos = get_posH(H), with_labels=True, font_weight='bold')
                    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True) 
                    plt.axis('on')
                    plt.grid('on')                 
                    plt.show()

                    break
    
    print(order)
    return order

def grid_canonical(graph_path):

    G1 = nx.Graph()
    G1.add_nodes_from([(1),(2),(3),(4),(5),(6)])
    G1.add_edges_from([(1,2),(1,4),(1,5),(2,3),(2,4),(2,5),(2,6),(3,4),(3,6),(4,5),(4,6)])
    
    G2 = nx.Graph()
    G2.add_nodes_from([(1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11)])
    G2.add_edges_from([(1,2),(1,11),(1,4),(2,4),(2,3),(2,5),(2,9),(2,11),(3,5),(3,4),(4,11),(4,5),(4,6),(4,7),(4,8),(5,6),(5,9),(5,10),(5,7),(5,11),(6,7),(7,8),(7,10),(7,11),(8,11),(9,11),(10,11)])

    f.addPosition(G1)

    #nx.draw(G2, with_labels=True, font_weight='bold')
    #plt.axis('on')
    #plt.grid('on')   
    #plt.show()

    data = nx.readwrite.json_graph.node_link_data(G1)
    f.save_graph(data, 'G1.json')
    
    G1 = graph.Graph.Graph('G1.json')

    #G = graph.Graph.Graph(graph_path)
    #G = dmp_planar_embedding(G)
    #G1 = dmp_planar_embedding(G1)
    G2 = apply_pos(G2)
    #print(canonical(G2))

def grid_layout(graph_path):

    #G1 = nx.Graph()
    #G1.add_nodes_from([(1),(2),(3),(4),(5),(6)])
    #G1.add_edges_from([(1,2),(1,4),(1,5),(2,3),(2,4),(2,5),(2,6),(3,4),(3,6),(4,5),(4,6)])
    G2 = nx.Graph()
    G2.add_nodes_from([(1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11)])
    G2.add_edges_from([(1,2),(1,11),(1,4),(2,4),(2,3),(2,5),(2,9),(2,11),(3,5),(3,4),(4,11),(4,5),(4,6),(4,7),(4,8),(5,6),(5,9),(5,10),(5,7),(5,11),(6,7),(7,8),(7,10),(7,11),(8,11),(9,11),(10,11)])
    G2 = apply_pos(G2)
    #f.addPosition(G1)
    #data = nx.readwrite.json_graph.node_link_data(G1)
    #f.save_graph(data, 'G1.json')
    #G1 = graph.Graph.Graph('G1.json')

    G = graph.Graph.Graph(graph_path)
    G = dmp_planar_embedding(G)
    #G = G2
    H = G.copy()
    order = canonical(H)
    v1 = order[0]
    v2 = order[1]
    v3 = order[2]
    k = len(order)
    H.nodes[v1]['pos'] = [0,0]
    H.nodes[v2]['pos'] = [2,0]
    H.nodes[v3]['pos'] = [1,1]
    border = [v1,v3,v2]
    M = [None]*3
    M[0] = [v1,v3,v2]
    M[1] = [v3,v2]
    M[2] = [v2]
    H2 = H.copy()
    for u in order[3:]:
        H2.remove_node(u)
    fig, ax = plt.subplots()
    nx.draw(H2, pos = get_posH(H2), with_labels=True, font_weight='bold') 
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.axis('on')
    plt.grid('on')                 
    plt.show()

    for i in range(3, k):
        L = []
        v = order[i]
        for u in border:
            if u in G.neighbors(v):
                L.append(u)
        wp = L[0]
        wq = L[len(L)-1]
        left = border.index(wp)
        right = border.index(wq)
        for u in M[left][1:]:
            H.nodes[u]['pos'][0] += 1
        for u in M[right][:]:
            H.nodes[u]['pos'][0] += 1
        

        H.nodes[v]['pos'][0] = (H.nodes[wq]['pos'][0] + H.nodes[wp]['pos'][0] + H.nodes[wq]['pos'][1] - H.nodes[wp]['pos'][1])/2
        H.nodes[v]['pos'][1] = (H.nodes[wq]['pos'][0] - H.nodes[wp]['pos'][0] + H.nodes[wq]['pos'][1] + H.nodes[wp]['pos'][1])/2
        
        del border[left+1:right]
        Mwp1 = M[left+1]
        del M[left+1:right]

        n = 0
        node = Mwp1[n]
        Mwp1 = Mwp1.copy()
        while H.nodes[v]['pos'][0] > H.nodes[node]['pos'][0]:
            n += 1
            node = Mwp1[n]
        Mwp1.insert(n,v)

        j = 0
        node = border[j]
        while H.nodes[v]['pos'][0] > H.nodes[node]['pos'][0]:
            j += 1
            node = border[j]
        border.insert(j,v)

        M.insert(j,Mwp1)

        for l in range(0,left+1):
            j = 0
            node = M[l][j]
            while H.nodes[v]['pos'][0] > H.nodes[node]['pos'][0]:
                j += 1
                node = M[l][j]
            M[l].insert(j,v)
        
        H2 = H.copy()
        for u in order[i+1:]:
            H2.remove_node(u)
        fig, ax = plt.subplots()
        nx.draw(H2, pos = get_posH(H2), with_labels=True, font_weight='bold') 
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.axis('on')
        plt.grid('on')                 
        plt.show()
    print(c.calculate_minimum_area(H))
    print((2*k-4)*(k-2))
    return H



