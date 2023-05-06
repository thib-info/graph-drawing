import argparse
import graph.factory as graph
import networkx as nx
import matplotlib.pyplot as plt
import shutil
from graph.Graph import Graph
import algo.Grid
from algo.force_direct import force_direct_figure
from algo import dmp_algo


def parse_args():
    """
    Parses the command-line arguments for the program.
    """
    parser = argparse.ArgumentParser(description='Generate and visualize graphs.')
    parser.add_argument('-g', '--generate', action='store_true', help='generate a new graph')
    parser.add_argument('-o', '--filename', type=str, default=None, help='filename for the graph data')
    parser.add_argument('-n', '--num-nodes', nargs='+', default=[10, 10], type=int, help='Number of nodes in the graph')
    parser.add_argument('-gt', '--graph-type', type=str, default="cycle",
                        choices=["all", "cycle", "tree", "bipartite", "outerplanar", "grid", "atlas", "complete"],
                        help="Type of graph to generate")
    parser.add_argument('-s', '--seed', type=int, default=None, help='Define the seed you want to apply')
    parser.add_argument('-c', '--complex', type=int, default=argparse.SUPPRESS,
                        help='Define the number of graph to generate and combine into a commun graph')
    parser.add_argument('--clean', action='store_true', help='Delete all the generated graphs')
    parser.add_argument('-e', '--evaluate', type=str, default='', help='Delete all the generated graphs')
    parser.add_argument('-w', '--weight', action='store_true',
                        help='Define if you want your graph to be weighted or not')
    parser.add_argument('-d', '--direction', action='store_true',
                        help='Define if you want your graph to be directive or not')
    parser.add_argument('-r', '--report', type=str, default='',
                        help='Save screenshot of the given graph into the pdf you specified')
    parser.add_argument('-grid', action= 'store_true')
    parser.add_argument('-fd', '--force-direct', action='store_true', help='activates the force direct algorithm for the chosen graph type')
    parser.add_argument('-fdt', '--force-direct type', type=str, default='Eades', choices=["Eades", "FR"], help='Define the specific type of force direct algorithm')
    parser.add_argument('-it', '--iterations', type=int, default=1000, help='Define the amount of iterations used by the (force direct) algorithm')
    parser.add_argument('-a', '--algo', type=str, default='',
                        choices=["complete", "dmp"],
                        help='Select the algo you want to apply to your graph')

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
    pos = {int(n): data['pos'] for n, data in G.nodes(data=True)}
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

        if args.graph_type == 'complete' or args.graph_type == 'all':
            graph.generate_complete_graph(args.num_nodes[0], args.seed, args.weight, args.direction)
            graph_to_print = 'complete_graph.json'

        if args.graph_type == 'grid' or args.graph_type == 'all':
            graph.generate_grid_graph(args.num_nodes[0], args.num_nodes[1], args.seed, args.weight, args.direction)
            graph_to_print = 'grid_graph.json'

        if args.graph_type == 'atlas' or args.graph_type == 'all':
            graph.generate_atlas_graph(args.num_nodes[0], args.weight)
            graph_to_print = 'atlas_graph.json'

    if hasattr(args, 'complex'):
        if args.complex is not None:
            if args.complex > nbr_graph:
                print("The number of graph types exceed the ones available. The maximum possible value is " + str(
                    nbr_graph))
                return -1
            else:
                graph.generate_complex_graph(args.num_nodes[0], args.num_nodes[1], args.complex, args.seed, args.weight,
                                             args.direction)

        graph_to_print = 'complex_graph.json'

    visualizeGraph(graph_to_print)


def evaluateGraph():
    args = parse_args()
    if args.evaluate == '':
        return -1

    if args.evaluate != '':
        if args.report != '':
            G = Graph('../stocked-graph/' + args.evaluate, args.report, args.algo)
        else:
            G = Graph('../stocked-graph/' + args.evaluate, None, args.algo)
        print(G)

    if args.algo == '':
        visualizeGraph(args.evaluate)


def plot_graph(graph, name):
    plt.subplots(1, 3)  # set subplot position
    pos = {int(n): data['pos'] for n, data in graph.nodes(data=True)}
    nx.draw(graph, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.title(name)  # set subplot title


def presentation():

    G1 = graph.load_graph('cycle_graph.json')
    G2 = graph.load_graph('complete_graph.json')
    G3 = graph.load_graph('tree_graph.json')

    # create a grid of 1 row and 3 columns of subplots
    fig, axs = plt.subplots(1, 3)

    # plot the first graph on the first subplot
    pos = {int(n): data['pos'] for n, data in G1.nodes(data=True)}
    nx.draw(G1, pos=pos, with_labels=True, ax=axs[0])
    axs[0].set_title("Cycle graph")

    # plot the second graph on the second subplot
    pos = {int(n): data['pos'] for n, data in G2.nodes(data=True)}
    nx.draw(G2, pos=pos, with_labels=True, ax=axs[1])
    axs[1].set_title("Complete graph")

    # plot the third graph on the third subplot
    pos = {int(n): data['pos'] for n, data in G3.nodes(data=True)}
    nx.draw(G3, pos=pos, with_labels=True, ax=axs[2])
    axs[2].set_title("Tree graph")

    # adjust the spacing between the subplots
    plt.subplots_adjust(wspace=1.5)

    # show the plot
    plt.show()

def force_direct():
    args = parse_args()
    if args.force_direct:
        force_direct_figure(args.graph_type + '_graph.json', args.iterations)

def grid():
    args = parse_args()
    if args.grid:
        algo.Grid.grid_figure(args.graph_type + '_graph.json')


def main():
    generateGraph()
    evaluateGraph()
    grid()
    force_direct()
    #presentation()

if __name__ == '__main__':
    main()    

