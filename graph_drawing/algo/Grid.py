import networkx as nx
import math



def canonical(graph):
    H = graph.copy()

    k = H.number_of_nodes()

    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf

    for node in graph.nodes():
        x = graph.nodes[node]['pos'][0]
        y = graph.nodes[node]['pos'][1]
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
    H.remove_node(w)


    for i in range(k-1, 2, -1):
        for j in ext:
            if j != u1 and j != u2:
                a = H.neighbors(j)
                if set(a).intersection(ext) == 2:
                    order[i-1] = j
                    ext.remove(j)
                    for u in H.neighbors(j):
                        if u not in ext:
                            ext.append(u)
                    H.remove_node(j)
                    break
    return order


G = nx.cycle_graph(5)
print(canonical(G))

