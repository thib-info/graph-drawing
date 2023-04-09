
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

| Parameter               | Possible value          | Description                						                 |
|:------------------------|:------------------------|:--------------------------------------------------|
| `--generated` or `-n`   | `None`   			            | Ask to generate the graphs  					                 |
| `--graph-type` or `-gt` | Check *list(typeGraph)* | Specifie the type of graph to generate  		        |
| `--file-name` or `-o`   | `string`.json 		        | Specifie the name where the graph has to be saved |
| `--num-nodes` or `-n`   | multiple `int`  	       | Use to specifie the number of vertices / edges    |
| `--complex` or `-c`     | `int` => **Max 5**      | Combine different type of graphs in one           |
| `--seed` or `s`         | `int`  	                | Specify the seed to use                           |
| `--clean`               | `None`  	               | Reset the cache of the project                    |

Here is the **list of typeGraph**: 
- Cycle graphs
- Tree graphs
- Bipartite graphs
- Outer planar graphs
- Grid graphs
- Complete graph

## Run Locally

To start using the project you have to generate at least one graph

```bash
  # Let's generate all the graph to start
  python3 main.py --generate -gt all
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

3. Clean the cache of the project
```bash
  python3 graph_drawing/main.py --clean
```

3. Generate all the graph with the same seed
```bash
  python3 graph_drawing/main.py --generate -gt all --seed 10
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

The implemented algorithms are:
- The DMP planar algorithm in *dmp_algo.py*

The implemented drawing algorithms are:
- None


## Authors

- [@thib-info](https://www.github.com/thib-info)
- [@TomasVdS](https://github.com/TomasVdS)

