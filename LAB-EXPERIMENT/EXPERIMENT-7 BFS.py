
from collections import deque

def bfs(graph, start):
    """Perform breadth‑first search on a graph.
       graph: dict where key is a node and value is a list of neighbours.
       start: node to begin the search from.
    """
    visited = set()          # keep track of visited nodes
    queue = deque()          # queue for BFS
    order = []               # order in which nodes are visited

    visited.add(start)
    queue.append(start)

    while queue:
        node = queue.popleft()
        order.append(node)   # record the visit

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return order


if __name__ == "__main__":
    # Example graph (undirected)
    example_graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    start_node = 'A'
    visit_order = bfs(example_graph, start_node)

    print("BFS traversal starting from", start_node, ":")
    print(" -> ".join(visit_order))
