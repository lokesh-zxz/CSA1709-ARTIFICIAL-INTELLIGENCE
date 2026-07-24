
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()  # blank line

def get_neighbors(state):
    neighbors = []
    blank_idx = state.index(0)  # position of the empty tile
    row, col = divmod(blank_idx, 3)

    # possible moves: up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_blank = new_r * 3 + new_c
            new_state = list(state)
            # swap blank with the tile
            new_state[blank_idx], new_state[new_blank] = new_state[new_blank], new_state[blank_idx]
            neighbors.append(tuple(new_state))

    return neighbors

def bfs(start, goal):
    from collections import deque

    queue = deque()
    queue.append(start)
    visited = {start: None}  

    while queue:
        current = queue.popleft()
        if current == goal:
           
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)

    return None  

def is_solvable(state):
    inv = 0
    flat = [x for x in state if x != 0]
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inv += 1
    return inv % 2 == 0
if __name__ == "__main__":
    start_state = (1, 2, 3,
                   4, 5, 6,
                   0, 7, 8)   

    goal_state = (1, 2, 3,
                  4, 5, 6,
                  7, 8, 0)

    print("Start state:")
    print_state(start_state)

    if not is_solvable(start_state):
        print("This puzzle configuration is not solvable.")
    else:
        print("Solving...")
        solution = bfs(start_state, goal_state)

        if solution is None:
            print("No solution found.")
        else:
            print(f"Solved in {len(solution)-1} moves:")
            for step, s in enumerate(solution):
                print(f"Step {step}:")
                print_state(s)
