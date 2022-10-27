from graphviz import Digraph, Graph

def dict_to_dot(adj_dict, weighted=False, directed=False):
    """ Create graphviz graph based on adjancency list (dictionary) 
    
    # Input parameters:
    adj_dict     - Adjacency list as dictionary
                   key = node name
                   if weighted: adj_dict values are dicts with keys = neighbor node names,
                       values = neighbor node edge weights
                   if not weighted: value = iterable with neighbor node names
    weighted     - Boolean, True if adj_dict describes a weighted graph
    directed     - Boolean, True for directed graph, False for undirected.
    
    # Returns:
    graph_dot    - Graphviz graph object (Graph or Digraph)
    
    """ 
    
    if directed:
        graph_dot = Digraph(strict=True)
    else:
        graph_dot = Graph(strict=True)
    
    for from_vertex in adj_dict.keys():
        if weighted:
            for to_vertex in adj_dict[from_vertex].keys():    # Assume dict of dicts
                graph_dot.edge(head_name = from_vertex,
                           tail_name = to_vertex,
                           label = str(adj_dict[from_vertex][to_vertex]))
        else:
            for to_vertex in adj_dict[from_vertex]:           # Assume dict of iterables
                graph_dot.edge(head_name = from_vertex,
                           tail_name = to_vertex)
    
    return graph_dot
    