from graph.Graph import Graph   
import graph.factory as f
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from math import log10, sqrt, log, inf
import graph.save as sv

def get_pos(G):
    '''
    Get the position of the nodes in graph G
    '''
    list = G.graph.nodes(data=True)
    pos = {}
    for node, data in G.graph.nodes(data=True):
        pos[node] = data['pos']

    return pos

def fa_Eades(c1, c2, total_distance):
    '''
    Calculate the total attractive force according to the Eades algorithm
    '''
    
    total_force = c1*log10(total_distance/c2)
    return total_force

def fr_Eades(c3, total_distance):
    '''
    Calculate the total repulsive force according to the Eades algorithm
    '''
    
    total_force = c3/total_distance**2
    return total_force

def fa_FR(k, total_distance):
    '''
    Calculate the total attractive force according to the Fruchterman and Reingold algorithm
    '''

    total_force = total_distance**2/k
    return total_force

def fr_FR(k, total_distance):
    '''
    Calculate the total repulsive force according to the Fruchterman and Reingold algorithm
    '''
    if total_distance == 0:
        return 0
    total_force = k**2/total_distance
    return total_force


def force_direct_figure(graph_path, M=1000, type="Eades"):
    '''
    Run the force direct algorithm on graph G for M iterations.
    The type is either 'Eades' (type=0) or 'Fruchterman and Reingold' (type=1) 
    '''

    G = Graph(graph_path)

    #configure fd-Eades variables
    c1, c2, c3, c4, M = 2,1,1,0.1,M

    #configure fd-FR variable
    area, C = 1, 0.5
    k, t0 = 1/sqrt(G.num_vertices), 0.1

    #choose plotting instances
    p1, p2, p3 = 1, 10, 50 

    # configure subplots
    width = 5
    length = 1

    # make sure width = length for each subplot
    width_size = 10
    plt.figure(figsize=(width_size,width_size/width*length))

    # draw the first subplot
    subax1 = plt.subplot(151)
    nx.draw(G.graph, pos = get_pos(G), with_labels=True, font_weight='bold')
    subax1.set_title('initial graph')
    
    # get the position of G
    pos = get_pos(G)

    # initialize the gif
    sv.init_gif('Force_direct')

    # iterate
    for i in range(M):

        forcex = np.zeros(G.num_vertices)
        forcey = np.zeros(G.num_vertices)

        if type == "FR":  
            # cool temperature t
            t = t0/(i+1)


        # calculate attractive forces
        for u, v in G.graph.edges():

            x_distance = pos[v][0] - pos[u][0]
            y_distance = pos[v][1] - pos[u][1]
            #total_distance = (x_distance**2 + y_distance**2)*G.graph.edges[u,v].get('weight', 1.0)
            total_distance = sqrt(x_distance**2 + y_distance**2)

            if total_distance != 0:

                if type == "Eades":
                    total_force = fa_Eades(c1, c2, total_distance)
                elif type == "FR":
                    total_force = fa_FR(k, total_distance)
                else:
                    raise ValueError

                #if i == M-1:
                #    print('u', u, 'v', v, 'total_force att', total_force, 'total_dist', total_distance, x_distance, y_distance, 'posvx', pos[v][0], 'posvy', pos[v][1])

                forcex[u] += total_force*x_distance/total_distance
                forcex[v] += -total_force*x_distance/total_distance

                forcey[u] += total_force*y_distance/total_distance
                forcey[v] += -total_force*y_distance/total_distance

        # calculate repulsive forces
        for u in G.graph.nodes():
            for v in G.graph.nodes():
                if (u, v) not in G.graph.edges() and u > v:

                    x_distance = pos[v][0] - pos[u][0]
                    y_distance = pos[v][1] - pos[u][1]
                    total_distance = sqrt(x_distance**2 + y_distance**2)

                    if type == "Eades":
                        total_force = fr_Eades(c3, total_distance)
                    elif type == "FR":
                        total_force = fr_FR(k, total_distance)

                    else:
                        raise ValueError

                    #if i == M-1:
                    #    print('u', u, 'v', v, 'total_force rep', total_force, 'total_dist', total_distance)

                    forcex[u] -= total_force*x_distance/total_distance
                    forcex[v] += total_force*x_distance/total_distance

                    forcey[u] -= total_force*y_distance/total_distance
                    forcey[v] += total_force*y_distance/total_distance
        
        for u in G.graph.nodes():
            if type == "Eades":        
                pos[u][0] += forcex[u]*c4 
                pos[u][1] += forcey[u]*c4
            '''
            else:
        
                pos[u][0] += forcex[u]*c4 
                pos[u][1] += forcey[u]*c4
            '''
            if type == "FR":
                total_force = sqrt(forcex[u]**2 + forcey[u]**2)

                # limit max movement to temperature t
                if forcex[u] > 0:
                    pos[u][0] += min(forcex[u], forcex[u]/total_force*t)  
                else:
                    pos[u][0] += max(forcex[u], forcex[u]/total_force*t)
                if forcey[u] > 0: 
                    pos[u][1] += min(forcey[u], forcey[u]/total_force*t)
                else:
                    pos[u][1] += max(forcey[u], forcey[u]/total_force*t)

                # limit movement to remain in the frame
                pos[u][0] = min(1, max(0, pos[u][0]))
                pos[u][1] = min(1, max(0, pos[u][1]))
                
        
        # draw graph at different stages
        if i == p1:
            subax2 = plt.subplot(152)
            nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')
            subax2.set_title('i = '+ str(p1))

        elif i == p2:
            subax3 = plt.subplot(153)
            nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')
            subax3.set_title('i = ' + str(p2))

        elif i == p3:
            subax4 = plt.subplot(154)
            nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')
            subax4.set_title('i = ' + str(p3))
        #TODO: gif implementation

        if i%5 == 0:
            sv.save_screenshot(G.graph, 'Force_Direct')
    
    subax5 = plt.subplot(155)
    nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')
    subax5.set_title('i = ' + str(M))
    plt.show()

    # normalize the node positions        
    xmax = -inf
    ymax = -inf
    xmin = inf
    ymin = inf

    for u in G.graph.nodes():
        if pos[u][0] > xmax: 
            xmax = pos[u][0]
        if pos[u][1] > ymax: 
            ymax = pos[u][1] 
        if pos[u][0] < xmin: 
            xmin = pos[u][0]
        if pos[u][1] < xmin: 
            ymin = pos[u][1]

    #plt.figure(figsize=(5,5*(ymax-ymin)/(xmax-xmin)))
    nx.draw(G.graph, pos = pos, with_labels=True, font_weight='bold')
    plt.show()


    print(type, ' edge length: ', G.edge_length)
    print(type, ' compactness: ', G.compactness)
    print(type, ' crossing number: ', G.crossing_number)
    print(type, ' clustering: ', G.clustering)
    print(type, ' minimum area: ', G.minimum_area)

    sv.create_gif_from_images('Force_Direct')
    return G

