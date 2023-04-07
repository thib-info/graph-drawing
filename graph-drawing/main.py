import argparse
import graph.factory as graph
import networkx as nx
import matplotlib.pyplot as plt
import shutil
from graph.Graph import Graph


def parse_args():
    """
    Parses the command-line arguments for the program.
    """
    parser = argparse.ArgumentParser(description='Generate and visualize graphs.')
    parser.add_argument('-g', '--generate', action='store_true', help='generate a new graph')
    parser.add_argument('-o', '--filename', type=str, default=None, help='filename for the graph data')
    parser.add_argument('-gt', '--graph-type', type=str, default="cycle", choices=["all", "cycle", "tree", "bipartite", "outerplanar", "grid", "atlas"], help="Type of graph to generate")
    parser.add_argument('-n', '--num-nodes', nargs='+', default=[10, 10], type=int, help='Number of nodes in the graph')
    parser.add_argument('-s', '--seed', type=int, default=None, help='Define the seed you want to apply')
    parser.add_argument('-c', '--complex', type=int, default=argparse.SUPPRESS, help='Define the number of graph to generate and combine into a commun graph')
    parser.add_argument('--clean', action='store_true', help='Delete all the generated graphs')
    parser.add_argument('-e', '--evaluate', type=str, default='', help='Delete all the generated graphs')
    parser.add_argument('-w', '--weight', action='store_true', help='Define if you want your graph to be weighted or not')
    parser.add_argument('-d', '--direction', action='store_true', help='Define if you want your graph to be directive or not')
    return parser.parse_args()


def visualizeGraph(graph_to_print):
    args = parse_args()

    # load the graph data from the file
    if args.filename is not None:
        G = graph.load_graph(args.filename)
    elif graph_to_print != '':
        G = graph.load_graph(graph_to_print)
    else:
        print("You have to generate at least one graph OR specify the graph that you want to print")
        return -1

    # visualize the graph using networkx
    pos = nx.spring_layout(G, seed=10)
    nx.draw(G, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # show the plot
    plt.show()


def generateGraph():
    args = parse_args()
    graph_to_print = ''
    nbr_graph = 5

    if args.clean:
        try:
            shutil.rmtree('stocked-graph')
            print('Successfully cleaned the "stocked-graph" folder')
            return 1
        except FileNotFoundError:
            print('The cache has already be cleaned')
            return 2

    if args.generate:
        if args.graph_type == 'cycle' or args.graph_type == 'all':
            graph.generate_cycle_graph(args.num_nodes[0], args.seed, args.weight, args.direction)
            graph_to_print = 'cycle_graph.json'

        if args.graph_type == 'tree' or args.graph_type == 'all':
            graph.generate_tree_graph(args.num_nodes[0], args.seed, args.weight, args.direction)
            graph_to_print = 'tree_graph.json'

        if args.graph_type == 'bipartite' or args.graph_type == 'all':
            graph.generate_bipartite_graph(args.num_nodes[0], args.num_nodes[1], args.seed, args.weight, args.direction)
            graph_to_print = 'bipartite_graph.json'

        if args.graph_type == 'outerplanar' or args.graph_type == 'all':
            graph.generate_outerplanar_graph(args.num_nodes[0], args.seed, args.weight, args.direction)
            graph_to_print = 'outerplanar_graph.json'

        if args.graph_type == 'grid' or args.graph_type == 'all':
            graph.generate_grid_graph(args.num_nodes[0], args.num_nodes[1], args.seed, args.weight, args.direction)
            graph_to_print = 'grid_graph.json'

        if args.graph_type == 'atlas' or args.graph_type == 'all':
            graph.generate_atlas_graph(args.weight)
            graph_to_print = 'atlas_graph.json'

    if hasattr(args, 'complex'):
        if args.complex is not None:
            if args.complex > nbr_graph:
                print("The number of graph types exceed the ones available. The maximum possible value is " + str(nbr_graph))
                return -1
            else:
                graph.generate_complex_graph(args.num_nodes[0], args.num_nodes[1], args.complex, args.seed, args.weight, args.direction)

        graph_to_print = 'complex_graph.json'

    visualizeGraph(graph_to_print)


def evaluateGraph():
    args = parse_args()
    if args.evaluate == '':
        return -1

    G = Graph('../stocked-graph/' + args.evaluate)
    print(G)

    visualizeGraph(args.evaluate)


def main():
    generateGraph()
    evaluateGraph()


if __name__ == '__main__':
    main()
