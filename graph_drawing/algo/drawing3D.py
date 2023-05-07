import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from math import log10, sqrt, log
from mpl_toolkits.mplot3d import Axes3D
from graph.Graph import Graph


def get_pos(G):
    '''
    Get the position of the nodes in graph G
    '''
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

    total_force = total_distance^2/k
    return total_force

def fr_FR(k, total_distance):
    '''
    Calculate the total repulsive force according to the Fruchterman and Reingold algorithm
    '''
    
    total_force = -k^2/total_distance
    return total_force

def figure_3D(graph_path, M=1000, type="Eades"):
    '''
    Run the force direct algorithm on graph G for M iterations.
    The type is either 'Eades' (type=0) or 'Fruchterman and Reingold' (type=1) 
    '''
    
    G = Graph(graph_path).graph
    
    # random layout
    pos = nx.random_layout(G, dim=3, seed=333)

    # node and edge positions
    nodes = np.array([pos[v] for v in G.nodes()])
    edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])

    fig = plt.figure()
    subax0 = fig.add_subplot(111, projection="3d")

    # plot the nodes
    subax0.scatter(*nodes.T, s=100, ec="w", color='blue')

    # plot the edges
    for edge in edges:
        subax0.plot(*edge.T, color='black')

    plt.show()


    #configure fd-Eades variables
    c1, c2, c3, c4, M = 2,1,1,0.1,M

    #configure fd-FR variable
    k, t0 = 1, 0.1

    #choose plotting instances
    p1, p2, p3 = 1, 5, 50 

    # configure subplots
    width = 4
    length = 1

    # make sure width = length for each subplot
    width_size = 8
    fig = plt.figure(figsize=(width_size,width_size/width*length))
    fig.tight_layout()

    # draw the first subplot
    subax1 = fig.add_subplot(141, projection='3d')
    subax1.set_title('initial figure')
    nodes = np.array([pos[v] for v in G.nodes()])
    edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])
    # plot the nodes
    subax1.scatter(*nodes.T, s=100, ec="w", color='blue')
    # plot the edges
    for edge in edges:
        subax1.plot(*edge.T, color='black')


    # iterate
    for i in range(M):

        forcex = np.zeros(G.number_of_nodes())
        forcey = np.zeros(G.number_of_nodes())
        forcez = np.zeros(G.number_of_nodes())

        if type == "FR":  
            # cool temperature t
            t = t0/(i+1)

        # calculate attractive forces
        for u, v in G.edges():

            x_distance = pos[v][0] - pos[u][0]
            y_distance = pos[v][1] - pos[u][1]
            z_distance = pos[v][2] - pos[u][2]
            #total_distance = (x_distance**2 + y_distance**2)*G.graph.edges[u,v].get('weight', 1.0)
            total_distance = sqrt(x_distance**2 + y_distance**2 + z_distance**2)

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

                forcez[u] += total_force*z_distance/total_distance
                forcez[v] += -total_force*z_distance/total_distance

        # calculate repulsive forces
        for u in G.nodes():
            for v in G.nodes():
                if (u, v) not in G.edges() and u > v:

                    x_distance = pos[v][0] - pos[u][0]
                    y_distance = pos[v][1] - pos[u][1]
                    z_distance = pos[v][2] - pos[u][2]
                    
                    total_distance = sqrt(x_distance**2 + y_distance**2 + z_distance**2)

                    total_force = c3/total_distance**2
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
                    
                    forcez[u] -= total_force*z_distance/total_distance
                    forcez[v] += total_force*z_distance/total_distance
        
        for u in G.nodes():
            if type == "Eades":        
                pos[u][0] += forcex[u]*c4 
                pos[u][1] += forcey[u]*c4
                pos[u][2] += forcez[u]*c4
            if type == "FR":
                total_force = sqrt(forcex[u]**2 + forcey[u]**2 + forcez[u]**2)

                # limit max movement to temperature t
                pos[u][0] += min(forcex[u], forcex[u]/total_force*t)    
                pos[u][1] += min(forcey[u], forcey[u]/total_force*t)
                pos[u][2] += min(forcez[u], forcez[u]/total_force*t)

                # limit movement to remain in the frame
                pos[u][0] = min(1, max(-1, pos[u][0]))
                pos[u][1] = min(1, max(-1, pos[u][1]))
                pos[u][2] = min(1, max(-1, pos[u][2]))

        # draw graph at different stages
        if i == p1:
            subax2 = fig.add_subplot(142, projection='3d')
            subax2.set_title('i = '+ str(p1))
            nodes = np.array([pos[v] for v in G.nodes()])
            edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])
            # plot the nodes
            subax2.scatter(*nodes.T, s=100, ec="w", color='blue')
            # plot the edges
            for edge in edges:
                subax2.plot(*edge.T, color='black')

        elif i == p2:
            subax3 = fig.add_subplot(143, projection='3d')
            subax3.set_title('i = '+ str(p2))
            nodes = np.array([pos[v] for v in G.nodes()])
            edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])
            # plot the nodes
            subax3.scatter(*nodes.T, s=100, ec="w", color='blue')
            # plot the edges
            for edge in edges:
                subax3.plot(*edge.T, color='black')

        elif i == p3:
            subax4 = fig.add_subplot(144, projection='3d')
            subax4.set_title('i = '+ str(p3))
            nodes = np.array([pos[v] for v in G.nodes()])
            edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])
            # plot the nodes
            subax4.scatter(*nodes.T, s=100, ec="w", color='blue')
            # plot the edges
            for edge in edges:
                subax4.plot(*edge.T, color='black')
    

        #TODO: gif implementation

    plt.show()
    '''
    # normalize the node positions        
    umax = 0

    for u in G.nodes():
        if max(abs(pos[u][0]), abs(pos[u][1]), abs(pos[u][2])) > umax: 
            umax = max(abs(pos[u][0]), abs(pos[u][1]), abs(pos[u][2]))
    
    for u in G.nodes():
        pos[u][0]/=umax
        pos[u][1]/=umax
        pos[u][2]/=umax
    
    nx.draw(G.graph, with_labels=True, font_weight='bold')
    plt.show()
    '''

    return G
