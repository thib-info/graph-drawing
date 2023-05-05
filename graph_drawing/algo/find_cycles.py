
def find_cycle(G, source=None):
    """Find a cycle in the given graph G and return it as a list of nodes.

    If the graph is acyclic, return an empty list.

    If `source` is given, start the search at the specified node.
    """
    visited = set()
    path = []
    cycle = []

    def dfs(node):
        nonlocal cycle
        visited.add(node)
        path.append(node)

        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor == source or neighbor in path:
                # backtrack along the path to find the cycle
                index = path.index(neighbor)
                cycle = path[index:]
                cycle.append(neighbor)

        path.pop()

    if source is None:
        source = next(iter(G))

    dfs(source)

    return cycle


def find_all_cycles(graph):
    cycles = []
    for node in graph.nodes():
        cycle = find_cycle(graph, node)
        if cycle is not None:
            cycles.append(cycle)
    return cycles