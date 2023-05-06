import networkx as nx
import math
import matplotlib
import graph.Graph 
from algo.dmp_algo import dmp_planar_embedding


def get_pos(G):
    '''
    Get the position of the nodes in graph G
    '''

    print(G.graph)
    pos = {}
    for node, data in G.graph.nodes(data=True):
        pos[node] = data['pos']

    return pos

def canonical(G):
    H = G.graph.copy()

    k = H.number_of_nodes()
    pos = get_pos(G)
    #pos = nx.planar_layout(H)

    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf


    for node in G.graph.nodes():
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
    print(ext)
    ext.remove(w)

    
    print(w, [n for n in H.neighbors(w)])
    for u in H.neighbors(w):
        if u not in ext:
            ext.append(u)
    H.remove_node(w)
    
    


    for i in range(k-1, 2, -1):
        for j in ext:
            if j != u1 and j != u2:
                a = [n for n in H.neighbors(j)]
                print(j, a)
                if len(set(a).intersection(ext)) == 2:
                    order[i-1] = j
                    ext.remove(j)
                    for u in H.neighbors(j):
                        if u not in ext:
                            ext.append(u)
                    H.remove_node(j)
                    
                    break
    return order

def grid_figure(graph_path):
    G = graph.Graph.Graph(graph_path)
    #G = dmp_planar_embedding(G)
    print(G.num_vertices)
    pos = get_pos(G)
    #pos = nx.planar_layout(G)
    print(pos)
    print(canonical(G))

