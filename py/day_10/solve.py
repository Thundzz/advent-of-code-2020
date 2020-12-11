import numpy as np
from collections import Counter, defaultdict
from operator import itemgetter

def parse_file(filename):
    with open(filename) as file:
        return list(map(int, file.readlines()))

def find_unavoidable_edges(sorted_sequence, graph):
    edges = []
    for item in sorted_sequence:
        if len(graph[item]) == 1 and graph[item][0] - item == 3:
            edges.append((item, graph[item][0]))
    return edges

def build_graph(sorted_sequence):
    """
    Each node points to a list of the nodes that are reacheable from it.
    """
    elements = set(sorted_sequence)
    graph = defaultdict(lambda : [])
    for element in sorted_sequence:
        for i in [1, 2, 3]:
            if element + i in elements:
                graph[element].append(element + i)
    return graph

def count_routes_graph(graph, source_node, dest_node):
    """
    classic tree-like graph traversal
    """
    if dest_node == source_node or dest_node - source_node == 1:
        return 1
    else:
        routes = 0
        for child in graph[source_node]:
            routes += count_routes_graph(graph, child, dest_node)
        return routes

def count_routes(sorted_sequence):
    graph = build_graph(sorted_sequence)
    edges = find_unavoidable_edges(sorted_sequence, graph)

    ends = map(itemgetter(1), edges)
    starts = map(itemgetter(0), edges[1:])
    first_subgraph = (0, edges[0][0])
    subgraph_boundaries = [first_subgraph] + list(zip(ends, starts)) 

    total_routes = 1
    for start, end in subgraph_boundaries:
        route_count = count_routes_graph(graph, start, end)
        total_routes *= route_count
    return total_routes

def main():
    sequence = parse_file("input.txt")
    n = len(sequence)
    sorted_seq = [0] + sorted(sequence) 
    sorted_seq.append(sorted_seq[n] + 3)

    diffs =  [sorted_seq[i+1] - sorted_seq[i]  for i in range(n+1)] 
    c = Counter(diffs)
    print(c[1] * c[3])
    route_count = count_routes(sorted_seq)
    print(route_count)
        
    

if __name__ == '__main__':
    main()