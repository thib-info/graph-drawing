
# Graph Drawing

Given a graph, where do you draw the nodes such that the graph looks ‘good’? What does it mean for a
graph to look visually nice in the first place? Several criteria exist, such as edge crossing, area needed,
symmetry, number of bends in edges, the smallest angle between two edges that share a node, etc

Various algorithms have been designed that try to optimize for different criteria. In this project, we will
investigate these algorithms, and implement them ourselves.

## Installation

Concerning the installation you just need to go on the root directory and run the following command

```bash
  pip install .
```
The project was build with the version of Python 3.7

## CLI Arguments
| Parameter               | Possible value                     | Description                						                        |
|:------------------------|:-----------------------------------|:---------------------------------------------------------|
| `--generated` or `-n`   | `None`   			                       | Ask to generate the graphs  					                        |
| `--graph-type` or `-gt` | Check *list(typeGraph)*            | Specifie the type of graph to generate  		               |
| `--file-name` or `-o`   | `string`.json 		                   | Specifie the name where the graph has to be saved        |
| `--num-nodes` or `-n`   | multiple `int`  	                  | Use to specifie the number of vertices / edges           |
| `--complex` or `-c`     | `int` => **Max 5**                 | Combine different type of graphs in one                  |
| `--seed` or `s`         | `int`  	                           | Specify the seed to use                                  |
| `--clean`               | `None`  	                          | Reset the cache of the project                           |
| `--weight` or `-w`      | `None`  	                          | Add weight to the edges of the graph                     |
| `--direction` or `-d`   | `None`  	                          | Add direction to the edges of the graph                  |
| `--evaluate` or `-e`    | `str` => name of the graph file  	 | Evaluate the graph with all the characteristics          |
| `--algo` or `-a`        | `str` => name of the algo to use   | Choose one drawing algorithm to apply to the given graph |
| `-grid`                 | `None`  	                         | Compute the canonical order, draw the steps of grid algorithm |

Here is the **list of typeGraph**:
- Cycle graphs (*cycle*)
- Tree graphs (*tree*)
- Bipartite graphs (*bipartite*)
- Outer planar graphs (*outerplanar*)
- Grid graphs (*grid*)
- Complete graph (*complete*)
- Complex graph (mixing the different types presented before)
- Graph from the atlas (*atlas*)

> :information_source: **The atlas graph is a list handled by *networkx library*.**: The number of graph available is 1253

## Run Locally

To start using the project you have to generate at least one graph

```bash
  # Let's generate all the graph to start
  python3 main.py --generate -gt all
```

After generating at least one graph, you can evaluate him and check all his characteristics with the following command

```bash
  # Evaluate one graph
  python3 main.py --evaluate <name of the graph>
```

## Usage examples

Here are some example to use the CLI arguments 

1. Generate a Bipartite graph 
```bash
  # Creation of bipartite graph with 10 vertices and 10 edges saved on the file bipartite_graph.json
  python3 graph_drawing/main.py --generate -gt bipartite -n 10 10
```

2. Create a complex graph that mix 3 distinct types of graph 
```bash
  python3 graph_drawing/main.py --complex 3
```

3. Check a specific previously generated graph
```bash
  python3 graph_drawing/main.py --o cycle_graph.json
```

4. Clean the cache of the project
```bash
  python3 graph_drawing/main.py --clean
```

5. Generate all the graph with the same seed
```bash
  python3 graph_drawing/main.py --generate -gt all --seed 10
```

6. Analyse a specific generated graph and save each iteration of algorithms inside a pdf
```bash
  python3 graph_drawing/main.py --generate -gt cycle -n 5 --evaluate cycle_graph.json --report cycle
```

7. Evaluate a graph to see all its characteristics
```bash
  # Evaluate the cycle graph previously generated
  python3 graph_drawing/main.py --evaluate cycle_graph.json
```

8. Apply the complete algo to a given graph 
```bash
  # Evaluate the cycle graph previously generated
  python3 graph_drawing/main.py --evaluate cycle_graph.json -a complete
```


## Features

Right now the program can generate the following type of graphs:
- Cycle graphs
- Tree graphs
- Bipartite graphs
- Outer planar graphs
- Grid graphs
- Complete graph
- Complex graph
- Atlas graph

The implemented algorithms are:
- The DMP planar algorithm in *dmp_algo.py*
- The complete graph drawing algorithm in *complete_algo.py*
- The circular layout drawing algorithm in *circular_layout.py*
- Grid drawing: shift method in *Grid.py*

To save and analyze iteration of an algorithm we can use the option *--report*
to save all of their plots inside a pdf.

We can also save our iterations inside an algorithm as a .gif format

The characteristics for a graph printed are:
- Number of vertices
- Number of edges
- Direction of the graph
- Weight of the graph
- If the graph is planar or not
- Edges length
- Crossing number
- Minimum area 
- If the graph is symmetric or not
- The compactness
- The clustering


## Authors

- [@thib-info](https://www.github.com/thib-info)
- [@TomasVdS](https://github.com/TomasVdS)
- [@TiboDeCock](https://github.com/TiboDeCock)

