def dfs_iterative(graph, start):
    if start not in graph:
        return [] 

    visited = set()
    stack = [start]
    visited.add(start)
    result = []

    while stack:
        node = stack.pop()
        result.append(node)
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return result


# Example usage:
if __name__ == "__main__":
    # Example graph (undirected)
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    print("DFS traversal starting from 'A':")
    traversal = dfs_iterative(graph, 'A')
    print(" -> ".join(traversal))
