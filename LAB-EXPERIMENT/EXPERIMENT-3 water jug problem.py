from collections import deque

def pour(state, from_jug, to_jug, capacities):
    """
    Return the new state after pouring water from one jug to another.
    state: (x, y) – current amount in jug1 and jug2
    from_jug, to_jug: 0 for jug1, 1 for jug2
    capacities: (cap1, cap2)
    """
    x, y = state
    cap1, cap2 = capacities

    if from_jug == 0 and to_jug == 1:          
        transfer = min(x, cap2 - y)
        return (x - transfer, y + transfer)
    elif from_jug == 1 and to_jug == 0:        
        transfer = min(y, cap1 - x)
        return (x + transfer, y - transfer)
    else:
        return state   

def get_neighbors(state, capacities):
    """Generate all possible next states from the current state."""
    x, y = state
    cap1, cap2 = capacities
    neighbors = []

    neighbors.append((cap1, y))          
    neighbors.append((x, cap2))     
    neighbors.append((0, y))             
    neighbors.append((x, 0))             


    neighbors.append(pour(state, 0, 1, capacities))

    neighbors.append(pour(state, 1, 0, capacities))

    return neighbors

def bfs(start, goal, capacities):
    """Breadth‑first search to find a sequence of moves."""
    queue = deque()
    queue.append((start, []))   
    visited = {start}

    while queue:
        (cur_state, path) = queue.popleft()
        if cur_state == goal:
            return path + [cur_state]   

        for nxt in get_neighbors(cur_state, capacities):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [cur_state]))

    return None 

def main():

    capacities = (4, 3)
    start_state = (0, 0)    
    goal_state  = (2, 0)      

    print(f"Capacities: Jug1 = {capacities[0]} L, Jug2 = {capacities[1]} L")
    print(f"Start state: {start_state}")
    print(f"Goal state:  {goal_state}\n")

    solution = bfs(start_state, goal_state, capacities)

    if solution is None:
        print("No solution found.")
    else:
        print(f"Solution found in {len(solution)-1} steps:")
        for i, state in enumerate(solution):
            print(f"Step {i}: Jug1 = {state[0]} L, Jug2 = {state[1]} L")

if __name__ == "__main__":
    main()
