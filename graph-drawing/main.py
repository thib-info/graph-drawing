import argparse
import graph.graph as graph
import networkx as nx
import matplotlib.pyplot as plt


def parse_args():
    """
    Parses the command-line arguments for the program.
    """
    parser = argparse.ArgumentParser(description='Generate and visualize graphs.')
    parser.add_argument('-g', '--generate', action='store_true', help='generate a new graph')
    parser.add_argument('-o', '--filename', type=str, default='cycle_graph.json', help='filename for the graph data')
    parser.add_argument('-gt', '--graph-type', type=str, default="cycle", choices=["all", "cycle", "tree", "bipartite", "outerplanar", "grid"], help="Type of graph to generate")
    parser.add_argument('-n', '--num-nodes', nargs='+', type=int, help='Number of nodes in the graph')
    return parser.parse_args()


def main():
    args = parse_args()

    if args.generate:
        if args.graph_type == 'cycle' or args.graph_type == 'all':
            # generate a new cycle graph and save it to a file
            graph_data = graph.generate_cycle_graph()
            graph.save_graph(graph_data, 'cycle_graph.json')
        elif args.graph_type == 'tree' or args.graph_type == 'all':
            graph_data = graph.generate_tree_graph(args.n)
            graph.save_graph(graph_data, 'tree_graph.json')
        elif args.graph_type == 'bipartite' or args.graph_type == 'all':
            if len(args.num_nodes) > 1:
                graph_data = graph.generate_bipartite_graph(args.num_nodes[0], args.num_nodes[1])
            else:
                graph_data = graph.generate_bipartite_graph()
            graph.save_graph(graph_data, 'bipartite_graph.json')
        elif args.graph_type == 'outerplanar' or args.graph_type == 'all':
            graph_data = graph.generate_outerplanar_graph(args.num_nodes[0])
            graph.save_graph(graph_data, 'outerplanar_graph.json')
        elif args.graph_type == 'grid' or args.graph_type == 'all':
            graph_data = graph.generate_grid_graph(args.num_nodes[0], args.num_nodes[1])
            graph.save_graph(graph_data, 'grid_graph.json')

    # load the graph data from the file
    G = graph.load_graph(args.filename)

    # visualize the graph using networkx
    pos = nx.circular_layout(G)
    nx.draw(G, pos=pos, with_labels=True)

    # show the plot
    plt.show()


if __name__ == '__main__':
    main()
