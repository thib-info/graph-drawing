import time
from graph.Graph import Graph   
import graph.factory as f
import graph.charateristics as c
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import graph.save as sv
import graph.charateristics
from algo.force_direct import force_direct_figure
from algo.Grid import grid_layout
from algo.dmp_algo import dmp_planar_embedding
from algo.Tree import TreeTR
from main import plot_graph



def full_comparison(graph_path):
    
    # create dicts with different metrics
    runtime_dict = {}
    crossing_dict = {}
    edge_length_dict = {}
    min_area_dict = {}
    avg_el_dict = {}
    var_el_dict = {}
    symmetry_dict = {}
    compactness_dict = {}
    clustering_dict = {}

    ## compare algorithm runtimes

    '''
    # test Eades
    t0_Eades = time.time() 
    G_Eades = force_direct_figure(graph_path=graph_path, type='Eades', make_fig = True).graph
    
    runtime_dict['fd: Eades'] = time.time() - t0_Eades
    crossing_dict['fd: Eades'] = c.calculate_crossing_number(G_Eades)
    edge_length_dict['fd: Eades'] = c.calculate_edge_length(G_Eades)
    min_area_dict['fd: Eades'] = c.calculate_minimum_area(G_Eades)
    avg_el_dict['fd: Eades'], var_el_dict['fd: Eades'] = c.calculate_edge_length_metrics(G_Eades)
    #symmetry_dict['fd: Eades'] = c.is_symmetric(G_Eades)

    
    # test FR
    t0_FR = time.time() 
    G_FR = force_direct_figure(graph_path=graph_path, type='FR', make_fig=True).graph
   
    runtime_dict['fd: FR'] = time.time() - t0_FR
    crossing_dict['fd: FR'] = c.calculate_crossing_number(G_FR)
    edge_length_dict['fd: FR'] = c.calculate_edge_length(G_FR)
    min_area_dict['fd: FR'] = c.calculate_minimum_area(G_FR)
    avg_el_dict['fd: FR'], var_el_dict['fd: FR'] = c.calculate_edge_length_metrics(G_FR)
    #symmetry_dict['fd: FR'] = c.is_symmetric(G_FR)
    '''
    '''
    # test DMP
    G = Graph(graph_path)
    t0_DMP = time.time()
    G_DMP = dmp_planar_embedding(G)
    runtime_dict['DMP'] = time.time() - t0_DMP

    plt.show()
    pos = {int(n): data['pos'] for n, data in G_DMP.nodes(data=True)}
    nx.draw(G_DMP, pos, with_labels=True)    
    print('DMP')
    plt.show()
    crossing_dict['DMP'] = c.calculate_crossing_number(G_DMP)
    edge_length_dict['DMP'] = c.calculate_edge_length(G_DMP)
    min_area_dict['DMP'] = c.calculate_minimum_area(G_DMP)
    avg_el_dict['DMP'], var_el_dict['DMP'] = c.calculate_edge_length_metrics(G_DMP)
    #symmetry_dict['DMP'] = c.is_symmetric(G_DMP)   
    print('test')
    
    '''
    t0_Grid = time.time()
    G_Grid = grid_layout(graph_path=graph_path)


    plt.show()
    print('grid')
    pos = {int(n): data['pos'] for n, data in G_Grid.nodes(data=True)}
    nx.draw(G_Grid, pos,with_labels=True)    
    plt.show()

    
    runtime_dict['Grid'] = time.time() - t0_Grid
    #crossing_dict['Grid'] = c.calculate_crossing_number(G_Grid)
    #edge_length_dict['Grid'] = c.calculate_edge_length(G_Grid)
    #min_area_dict['Grid'] = c.calculate_minimum_area(G_Grid)
    #avg_el_dict['Grid'], var_el_dict['Grid'] = c.calculate_edge_length_metrics(G_Grid)
    
    
    t0_Tree = time.time()    
    G_Tree = TreeTR(graph_path)
    runtime_dict['Tree'] = time.time() - t0_Tree
    crossing_dict['Tree'] = c.calculate_crossing_number(G_Tree)
    edge_length_dict['Tree'] = c.calculate_edge_length(G_Tree)
    min_area_dict['Tree'] = c.calculate_minimum_area(G_Tree)
    avg_el_dict['Tree'], var_el_dict['Tree'] = c.calculate_edge_length_metrics(G_Tree)
    

    print('runtime', runtime_dict)
    print('crossing', crossing_dict)
    print('minimum area', min_area_dict)
    print('normalized avg edge length', avg_el_dict)
    print('normalized var edge length', var_el_dict)
    #print(symmetry_dict)


def comparison_growing_nodes():

    runtime = []
    times = [3,4,5,10,20,50,100]

    for i in times:

        name = 'tree'

        graph = nx.random_tree(n=i, seed=15)
        f.addPosition(graph)
        
        nx.draw(graph)
        plt.show()

        data = nx.node_link_data(graph)
        f.save_graph(data, name)

        t0_Eades = time.time() 
        G_Eades = force_direct_figure(name, type='Eades', make_fig=True).graph

        diff = time.time() - t0_Eades
        print('n =', i, ': ', diff)



