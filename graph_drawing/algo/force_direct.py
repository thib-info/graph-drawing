from graph.Graph import Graph   
import graph.factory as f
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from math import log10, sqrt, log

def get_pos(G):

    list = G.graph.nodes(data=True)
    pos = {}
    for node, data in G.graph.nodes(data=True):
        pos[node] = data['pos']
        #pos[i[0]] = [i[1]['pos'][0], i[1]['pos'][1]]

    return pos

    
def force_direct(G,M=1000):

    #c1, c2, c3, c4, M = 2,1,0.1,0.1,1000
    c1, c2, c3, c4, M = 2, 0.005, 0.01, 0.1, M
    print(G)

    # configure subplots
    width = 4
    length = 1

    # make sure width = length for each subplot
    width_size = 8
    plt.figure(figsize=(width_size,width_size/width*length))

    subax1 = plt.subplot(141)
    nx.draw(G.graph, pos = get_pos(G), with_labels=True, font_weight='bold')

    pos = get_pos(G)
    print(pos)

    for i in range(M):

        forcex = np.zeros(G.num_vertices)
        forcey = np.zeros(G.num_vertices)

        # calculate attractive forces
        for u, v in G.graph.edges():
            
            x_distance = pos[v][0] - pos[u][0]
            y_distance = pos[v][1] - pos[u][1]
            #total_distance = (x_distance**2 + y_distance**2)*G.graph.edges[u,v].get('weight', 1.0)
            total_distance = sqrt(x_distance**2 + y_distance**2)

            if total_distance != 0:
                total_force = c1*max(log10(total_distance/c2),0)

                if i == M-1:
                    print('u', u, 'v', v, 'total_force att', total_force, 'total_dist', total_distance, x_distance, y_distance, 'posvx', pos[v][0], 'posvy', pos[v][1])
 
                forcex[u] += total_force*x_distance/total_distance
                forcex[v] += -total_force*x_distance/total_distance

                forcey[u] += total_force*y_distance/total_distance
                forcey[v] += -total_force*y_distance/total_distance

        #if i == 0:
            #print('u:', u, ' v:', v, 'x0:', pos[u][0], 'y0', pos[u][1], ' x:', x_distance, ' y:', y_distance, ' tot:',total_distance, ' tot_force:', total_force, '\nforcexu:', forcex[u], ' forceyu', forcey[u], 'forcexv:', forcex[v], ' forceyv', forcey[u])

        # calculate repulsive forces
        for u in G.graph.nodes():
            for v in G.graph.nodes():
                if (u, v) not in G.graph.edges() and u > v:

                    x_distance = pos[v][0] - pos[u][0]
                    y_distance = pos[v][1] - pos[u][1]
                    total_distance = sqrt(x_distance**2 + y_distance**2)

                    total_force = c3/total_distance**2

                    if i == M-1:
                        print('u', u, 'v', v, 'total_force rep', total_force, 'total_dist', total_distance)

                    forcex[u] -= total_force*x_distance/total_distance
                    forcex[v] += total_force*x_distance/total_distance

                    forcey[u] -= total_force*y_distance/total_distance
                    forcey[v] += total_force*y_distance/total_distance
        
        for u in G.graph.nodes():
            pos[u][0] += forcex[u]*c4 
            pos[u][1] += forcey[u]*c4
        
        if i == 0:

            print(forcex)
            print(forcey)

        if i == 10:
            # draw graphs with different layouts
            subax2 = plt.subplot(142)
            nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')

        elif i == 20:
            subax3 = plt.subplot(143)
            nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')

        elif i == 30:
            print(forcex)
            print(forcey)
            subax4 = plt.subplot(144)
            nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')
            plt.show()

    '''
    # normalize the node positions        
    max_x = 0
    max_y = 0

    for u in G.graph.nodes():
        if abs(pos[u][0]) > max_x: 
            max_x = abs(pos[u][0]) 
        if abs(pos[u][1]) > max_y: 
            max_y = abs(pos[u][1])

    print('max',max_x, max_y)

    # normalize the node positions 
    for u in G.graph.nodes():
        pos[u][0]/=max_x
        pos[u][1]/=max_y
    '''
    return G

def force_direct_figure(graph_path,M):

    if graph_path is None:
        f.generate_cycle_graph(10)
        f.generate_outerplanar_graph(5)
        str1 = "cycle_graph.json"
        str2 = "outerplanar_graph.json"

        graph_path = str1
    
    G = Graph(graph_path)
    force_direct(G,M)
    
    nx.draw(G.graph, pos=get_pos(G), with_labels=True, font_weight='bold')
    plt.show()