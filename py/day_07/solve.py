import re
from collections import defaultdict

def parse_line(line):
    subjectRegex = r"(?P<color>\w+ \w+) bags contain"
    dependencyRegex = r"(?P<number>\d) (?P<color>\w+ \w+) bags?"

    subject = re.match(subjectRegex, line)["color"]
    dependencyMatches = [(m["number"], m["color"]) for m in re.finditer(dependencyRegex, line)]
    return (subject, dependencyMatches)


def parse_input(filename):
    with open(filename) as file:
        lines = file.readlines()
    return dict([parse_line(line) for line in lines])

def reverse_graph(dependencies):
    g = defaultdict(lambda : set())
    for k, deps in dependencies.items():
        for _, dep in deps:
            g[dep].add(k)
    return g

def explore_parents(graph, initial_node):
    visited = set()
    to_explore = [ initial_node ]
    while to_explore:
        current = to_explore.pop(0)
        for node in graph[current]:
            if node not in visited:
                to_explore.append(node)
        visited.add(current)
    
    return visited - set([initial_node])
    
def number_nested_bags(initial, graph):
    deps = graph[initial]
    if deps:
        res = 1
        for count, dep in deps:
            res += int(count) * number_nested_bags(dep, graph)
        return res
    else:
        return 1


def main():
    dependencies = parse_input("input.txt")
    reversed_g = reverse_graph(dependencies)
    possible_parents = explore_parents(reversed_g, "shiny gold")
    print(len(possible_parents))
    c = number_nested_bags("shiny gold", dependencies)
    print(c-1)

if __name__ == '__main__':
    main()