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


def full_comparison(graph_path):
    
    # create dicts with different metrics
    runtime_dict = {}
    crossing_dict = {}
    edge_length_dict = {}
    min_area_dict = {}
    symmetry_dict = {}
    compactness_dict = {}
    clustering_dict = {}

    ## compare algorithm runtimes
    
    # test Eades
    t0_Eades = time.time() 
    G_Eades = force_direct_figure(graph_path=graph_path, type='Eades').graph
    
    runtime_dict['fd: Eades'] = time.time() - t0_Eades
    crossing_dict['fd: Eades'] = c.calculate_edge_length(G_Eades)
    edge_length_dict['fd: Eades'] = c.calculate_edge_length(G_Eades)
    min_area_dict['fd: Eades'] = c.calculate_minimum_area(G_Eades)
    #symmetry_dict['fd: Eades'] = c.is_symmetric(G_Eades)
    compactness_dict['fd: Eades'] = c.calculate_compactness(G_Eades)
    #clustering_dict['fd: Eades'] = c.calculate_clustering(G_Eades)


    # test FR
    t0_FR = time.time() 
    G_FR = force_direct_figure(graph_path=graph_path, type='FR').graph
   
    runtime_dict['fd: FR'] = time.time() - t0_FR
    crossing_dict['fd: FR'] = c.calculate_edge_length(G_FR)
    edge_length_dict['fd: FR'] = c.calculate_edge_length(G_FR)
    min_area_dict['fd: FR'] = c.calculate_minimum_area(G_FR)
    #symmetry_dict['fd: FR'] = c.is_symmetric(G_FR)
    compactness_dict['fd: FR'] = c.calculate_compactness(G_FR)
    #clustering_dict['fd: FR'] = c.calculate_clustering(G_FR)


    # test DMP
    G = Graph(graph_path)
    t0_DMP = time.time()
    G_DMP = dmp_planar_embedding(G)

    runtime_dict['DMP'] = time.time() - t0_DMP
    crossing_dict['DMP'] = c.calculate_edge_length(G_DMP)
    edge_length_dict['DMP'] = c.calculate_edge_length(G_DMP)
    min_area_dict['DMP'] = c.calculate_minimum_area(G_DMP)
    #symmetry_dict['DMP'] = c.is_symmetric(G_DMP)
    compactness_dict['DMP'] = c.calculate_compactness(G_DMP)
    #clustering_dict['DMP'] = c.calculate_clustering(G_DMP)
    '''
    t0_Grid = time.time()
    grid_layout(graph_path=graph_path)
    runtime_dict['Grid'] = time.time() - t0_Grid
    '''

    print(runtime_dict)
    print(crossing_dict)
    print(edge_length_dict)
    print(min_area_dict)
    print(symmetry_dict)
    print(compactness_dict)
    print(clustering_dict)