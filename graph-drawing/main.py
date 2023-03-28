import argparse
import graph.graph as graph
import networkx as nx
import matplotlib.pyplot as plt


def parse_args():
    """
    Parses the command-line arguments for the program.
    """
    parser = argparse.ArgumentParser(description='Generate and visualize graphs.')
    parser.add_argument('--generate', action='store_true', help='generate a new graph')
    parser.add_argument('--filename', type=str, default='cycle_graph.json', help='filename for the graph data')
    return parser.parse_args()


def main():
    args = parse_args()

    if args.generate:
        # generate a new cycle graph and save it to a file
        graph_data = graph.generate_cycle_graph()
        graph.save_graph(graph_data, args.filename)

    # load the graph data from the file
    G = graph.load_graph(args.filename)

    # visualize the graph using networkx
    pos = nx.circular_layout(G)
    nx.draw(G, pos=pos, with_labels=True)

    # show the plot
    plt.show()


if __name__ == '__main__':
    print("It worked")
    main()
