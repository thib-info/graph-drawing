import networkx as nx
from . import factory
from . import charateristics as char


class Graph:
    def __init__(self, path):
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

        # self.number_bends = char.calculate_edge_bends(self) --> No need to print number of bends for now

        if self.is_directed:
            # Don't take into account the direction, but only check if each edges are connected
            self.is_connected = nx.is_strongly_connected(self.graph)
        else:
            self.is_connected = nx.is_connected(self.graph)

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
        output = ""
        output += f"Graph Path: {self.path}\n"
        output += f"Number of Vertices: {self.num_vertices}\n"
        output += f"Number of Edges: {self.num_edges}\n"
        output += f"Is Directed: {self.is_directed}\n"
        output += f"Is Weighted: {self.is_weighted}\n"
        output += f"Is Connected: {self.is_connected}\n"
        output += f"Is Planar: {self.is_planar}\n"
        output += f"Edge Length: {self.edge_length}\n"
        output += f"Crossing Number: {self.crossing_number}\n"
        output += f"Minimum area: {self.minimum_area}\n"
        output += f"Is symmetric: {self.is_symmetric}\n"
        output += f"Compacness of the graph: {self.compactness}\n"
        output += f"Clustering of the graph: {self.clustering}\n"

        # output += f"Number of bends per edges: {self.number_bends}\n"

        return output
