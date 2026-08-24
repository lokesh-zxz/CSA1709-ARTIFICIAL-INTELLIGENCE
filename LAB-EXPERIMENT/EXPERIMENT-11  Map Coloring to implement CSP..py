def is_safe(node, color, assignment, graph):
    for neighbor in graph[node]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True
def map_coloring(graph, colors, assignment, nodes, index):
    if index == len(nodes):
        return True

    node = nodes[index]

    for color in colors:
        if is_safe(node, color, assignment, graph):
            assignment[node] = color

            if map_coloring(graph, colors, assignment, nodes, index + 1):
                return True
            del assignment[node]

    return False
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['A', 'B', 'D', 'E'],
    'D': ['A', 'C', 'E'],
    'E': ['B', 'C', 'D']
}
colors = ['Red', 'Green', 'Blue']

assignment = {}
nodes = list(graph.keys())

if map_coloring(graph, colors, assignment, nodes, 0):
    print("Map Coloring Solution:\n")
    for region in nodes:
        print(f"{region} --> {assignment[region]}")
else:
    print("No solution exists.")
