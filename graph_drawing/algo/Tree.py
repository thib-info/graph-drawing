import networkx as nx
import math
import matplotlib.pyplot as plt
import graph.Graph
import numpy

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



def TreeRT1(graph_path, fathernode=0):
    G = graph.Graph.Graph(graph_path)
    G = G.graph.copy()

    G1 = nx.Graph()
    G1.add_nodes_from([(0),(1),(2),(3),(4),(5),(6),(7),(8)])
    G1.add_edges_from([(0,1),(0,2),(1,3),(1,4),(2,5),(2,6),(2,7),(7,8)])
    G = G1

    k = G.number_of_nodes()
    depth = 1
    nodes = 1 + len([n for n in G.neighbors(fathernode)])
    levels = []
    levels.append([fathernode])
    levels.append([n for n in G.neighbors(fathernode)])
    while nodes < k:
        neighbours = []
        for u in levels[depth]:
            for v in G.neighbors(u):
                if v not in levels[depth-1]:
                    nodes += 1
                    neighbours.append(v)
        levels.append(neighbours)
        depth += 1

    
    offsets = []
    sets = []
    leftcontours = []
    rightcontours = []
    for u in levels[-2]:
        count = 0
        for v in G.neighbors(u):
            if len(levels) < 3:
                count += 1
            elif v not in levels[-3]:
                count += 1
        if count%2 == 1:
            set = [n for n in range(math.ceil(-count/2),math.ceil(count/2))]
        else:
            set = [n for n in range(math.ceil(-count/2),0)] + [m for m in range(1,math.floor(count/2+1))]
        if count > 0:
            leftcontours.append(min(set))
            rightcontours.append(max(set))
        sets = sets + set
    offsets.append(sets)    
    print(offsets)


    if len(levels) < 3:
        G.nodes[fathernode]['pos'] = [0,1]
        for u in G.neighbors(fathernode):
            G.nodes[u]['pos'][1] = [0]
            G.nodes[u]['pos'][0] = [offsets[u]]

    else:
        for level in levels[-2::-1]:
            for u in level:
                count = 0
                for v in G.neighbors(u):
                    if level == 0:
                        count += 1
                    elif v not in levels[level-1]:
                        count += 1
                if count%2 == 1:
                    set = [n for n in range(math.ceil(-count/2),math.ceil(count/2))]
                else:
                    set = [n for n in range(math.ceil(-count/2),0)] + [m for m in range(1,math.floor(count/2+1))]
                if count > 0:
                    leftcontours.append(min(set))
                    rightcontours.append(max(set))
                sets = sets + set
            offsets.append(sets)  
                

        #print([[1,2,4]]+offsets)





def TreeTR(graph_path, root = 0):
    G = graph.Graph.Graph(graph_path)
    G = G.graph.copy()

    G1 = nx.Graph()
    G1.add_nodes_from([(0),(1),(2),(3),(4),(5),(6),(7),(8)])
    G1.add_edges_from([(0,1),(0,2),(1,3),(1,4),(2,5),(2,6),(2,7),(7,8)])
    #G = G1
    k = G.number_of_nodes()
    postorder = []
    nodes = 0
    while nodes < k:
        H = G.copy()
        for u in postorder:
            H.remove_node(u)
        i = 0
        node = root
        while i < 1:
            neighbours = [n for n in H.neighbors(node)]
            if len(neighbours) >= 2:
                H.remove_node(node)
                node = neighbours[0]
            elif len(neighbours) == 1:
                node1 = neighbours[0]
                if len([n for n in H.neighbors(node1)]) == 1:
                    postorder.append(neighbours[0])
                    H.remove_node(neighbours[0])
                    nodes += 1
                else:
                    H.remove_node(node)
                    node = node1
            else:
                postorder.append(node)
                nodes += 1
                i += 1



    depth = 1
    nodes = 1 + len([n for n in G.neighbors(root)])
    levels = []
    levels.append([root])
    levels.append([n for n in G.neighbors(root)])
    while nodes < k:
        neighbours = []
        for u in levels[depth]:
            for v in G.neighbors(u):
                if v not in levels[depth-1]:
                    nodes += 1
                    neighbours.append(v)
        levels.append(neighbours)
        depth += 1


    ycoords = [None]*k
    for i in range(len(levels)):
        l = levels[i]
        y = depth - i
        for u in l:
            index = postorder.index(u)
            ycoords[index] = y


    nodes = 0
    xcoords = [0]
    while nodes < k-1:
        neighbours = [u for u in G.neighbors(postorder[nodes])]
        for u in neighbours:
            index = postorder.index(u)
            if ycoords[index] > ycoords[nodes]:
                neighbour = u
                index_neighbour = postorder.index(u)
        count = 0
        for u in G.neighbors(neighbour):
            index = postorder.index(u)
            if ycoords[index] < ycoords[index_neighbour]:
                count += 1
        if count == 1:
            nodes += 1
            xcoords.append(xcoords[nodes-1])
        else:
            under = 0
            done = 0
            for u in G.neighbors(neighbour):
                if done == 0:
                    index = postorder.index(u)
                    if ycoords[index] < ycoords[index_neighbour]:
                        under += 1
                        if len(xcoords) < index + 1:
                            if len([n for n in G.neighbors(u)]) == 1:
                                nodes += 1
                                xcoords.append(xcoords[nodes-1]+2)
                                under -= 1
                                done += 1
                            else:
                                nodes += 1
                                xcoords.append(max(xcoords)+2)
                                under -= 1
                                done += 1
            if (under == len([n for n in G.neighbors(neighbour)])-1 and neighbour != root) or (neighbour == root and under == len([n for n in G.neighbors(neighbour)]) ):
                nodes += 1
                left = math.inf
                right = -math.inf
                for u in G.neighbors(neighbour):
                    index = postorder.index(u)
                    if ycoords[index] < ycoords[index_neighbour]:
                        if xcoords[index] > right:
                            right = xcoords[index]
                        if xcoords[index] <left:
                            left = xcoords[index]
                xcoords.append((left+right)/2)
                
    
    G = apply_pos(G)
    for i in range(len(xcoords)):
        G.nodes[postorder[i]]['pos'][0] = xcoords[i]
        G.nodes[postorder[i]]['pos'][1] = ycoords[i]

    fig, ax = plt.subplots()
    nx.draw(G, pos = get_posH(G), with_labels=True, font_weight='bold') 
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.axis('on')
    plt.grid('on')                 
    plt.show()







        

    
            


