import networkx as nx
from matplotlib import pyplot as plt
from tabulate import tabulate

from . import factory
from . import charateristics as char
from algo import dmp_algo as dmp
from algo import Grid
from algo import complete_algo as complete



class Graph:

    def __init__(self, path, save=None, algo):

        self.path = path
        self.graph = factory.load_graph(self.path)
        self.num_vertices = self.graph.number_of_nodes()
        self.num_edges = self.graph.number_of_edges()
        self.is_directed = self.graph.is_directed()
        self.is_weighted = self.is_weighted_graph()
        self.is_planar = nx.check_planarity(self.graph)[0]
        self.edge_length = char.calculate_edge_length(self.graph)
        self.crossing_number = char.calculate_crossing_number(self.graph)
        self.minimum_area = char.calculate_minimum_area(self.graph)
        self.is_symmetric = char.is_symmetric(self)
        self.compactness = char.calculate_compactness(self.graph)
        self.clustering = char.calculate_clustering(self)
        self.is_planar_DMP = dmp.is_planar_DMP(self.graph, save)
        self.algo = None

        # self.number_bends = char.calculate_edge_bends(self) --> No need to print number of bends for now

        if self.is_directed:
            # Don't take into account the direction, but only check if each edges are connected
            self.is_connected = nx.is_strongly_connected(self.graph)
        else:
            self.is_connected = nx.is_connected(self.graph)

        # Apply the given algo to the graph
        if algo is not '':
            if algo == 'complete':
                self.algo = complete.complete_graph(self.graph)
            if algo == 'dmp':
                dmp.dmp_planar_embedding(self.graph)
                self.algo = Graph('../stocked-graph/dmp_graph_algo.json', None, None)

        # Compare the two graph
        if self.algo is not None:
            fig, axs = plt.subplots(1, 2)

            # Plot the first graph on the first subplot
            pos = {int(n): data['pos'] for n, data in self.graph.nodes(data=True)}
            nx.draw(self.graph, pos=pos, with_labels=True, ax=axs[0])
            axs[0].set_title("Original graph")

            # Plot the second graph on the second subplot
            pos = {int(n): data['pos'] for n, data in self.algo.graph.nodes(data=True)}
            nx.draw(self.algo.graph, pos=pos, with_labels=True, ax=axs[1])
            axs[1].set_title("After the algorithm being applied")

            # adjust the spacing between the subplots
            plt.subplots_adjust(wspace=1.5)

            # show the plot
            plt.show()

    def is_weighted_graph(self):
        for u, v in self.graph.edges():
            if 'weight' not in self.graph[u][v]:
                return False
        return True

    def calculate_edge_length(self):
        total_length = 0
        for u, v, d in self.graph.edges(data=True):
            if 'weight' in d:
                total_length += d['weight']
            else:
                x1, y1 = self.graph.nodes[u]['pos']
                x2, y2 = self.graph.nodes[v]['pos']
                total_length += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return total_length

    def __str__(self):
        if self.algo is None:
            table = [
                ['Graph Path:', self.path],
                ['Number of Vertices:', self.num_vertices],
                ['Number of Edges:', self.num_edges],
                ['Is Directed:', self.is_directed],
                ['Is Weighted:', self.is_weighted],
                ['Is Connected:', self.is_connected],
                ['Is Planar:', self.is_planar],
                ['Is Planar with DMP algo:', self.is_planar_DMP],
                #['Edge Length:', self.edge_length],
                ['Crossing Number:', self.crossing_number],
                #['Minimum area:', self.minimum_area],
                ['Is symmetric:', self.is_symmetric],
                ['Compacness of the graph:', self.compactness],
                ['Clustering of the graph:', self.clustering],
                # ['Number of bends per edges:', self.number_bends],
            ]
            return tabulate(table, headers=['Attribute', 'Original graph'], tablefmt='orgtbl')
        else:
            table = [
                ['Graph Path:', self.path, self.algo.path],
                ['Number of Vertices:', self.num_vertices, self.algo.num_vertices],
                ['Number of Edges:', self.num_edges, self.algo.num_edges],
                ['Is Directed:', self.is_directed, self.algo.is_directed],
                ['Is Weighted:', self.is_weighted, self.algo.is_weighted],
                ['Is Connected:', self.is_connected, self.algo.is_connected],
                ['Is Planar:', self.is_planar, self.algo.is_planar],
                ['Is Planar with DMP algo:', self.is_planar_DMP, self.algo.is_planar_DMP],
                # ['Edge Length:', self.edge_length],
                ['Crossing Number:', self.crossing_number, self.algo.crossing_number],
                # ['Minimum area:', self.minimum_area],
                ['Is symmetric:', self.is_symmetric, self.algo.is_symmetric],
                ['Compacness of the graph:', self.compactness, self.algo.compactness],
                ['Clustering of the graph:', self.clustering, self.algo.clustering],
                # ['Number of bends per edges:', self.number_bends],
            ]
            return tabulate(table, headers=['Attribute', 'Original graph', 'Graph after algo.'], tablefmt='orgtbl')