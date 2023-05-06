import networkx as nx
import math
import matplotlib.pyplot as plt
import graph.Graph 
from algo.dmp_algo import dmp_planar_embedding
import graph.factory as f


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
    print(ext)
    ext.remove(w)

    
    print(w, [n for n in H.neighbors(w)])
    for u in H.neighbors(w):
        if u not in ext:
            ext.append(u)

    nx.draw(H, pos = get_posH(H), with_labels=True, font_weight='bold')                  
    plt.show()
    H.remove_node(w)
    nx.draw(H, pos = get_posH(H), with_labels=True, font_weight='bold')                  
    plt.show()
    


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
                    nx.draw(H, pos = get_posH(H), with_labels=True, font_weight='bold')                  
                    plt.show()

                    break
    
    return order

def grid_figure(graph_path):

    G1 = nx.Graph()
    G1.add_nodes_from([(1),(2),(3),(4),(5),(6)])
    G1.add_edges_from([(1,2),(1,4),(1,5),(2,3),(2,4),(2,5),(2,6),(3,4),(3,6),(4,5),(4,6)])
    
    f.addPosition(G1)

    #nx.draw(G1, with_labels=True, font_weight='bold')   
    #plt.show()

    data = nx.readwrite.json_graph.node_link_data(G1)
    f.save_graph(data, 'G1.json')
    
    G1 = graph.Graph.Graph('G1.json')

    G = graph.Graph.Graph(graph_path)
    G = dmp_planar_embedding(G)
    G1 = dmp_planar_embedding(G1)
    #pos = nx.planar_layout(G)
    print(canonical(G))

