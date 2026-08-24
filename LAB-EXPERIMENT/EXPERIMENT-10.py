Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import heapq
import sys
from typing import Callable, Dict, Hashable, List, Tuple, Optional

def astar(
    start: Hashable,
    goal: Hashable,
    neighbors: Callable[[Hashable], List[Tuple[Hashable, float]]],
    heuristic: Callable[[Hashable, Hashable], float],
    weight: Callable[[Hashable, Hashable], float] = lambda u, v: 1.0,
) -> Optional[List[Hashable]]:

    open_set: List[Tuple[float, Hashable]] = []
    heapq.heappush(open_set, (heuristic(start, goal), start))

    came_from: Dict[Hashable, Hashable] = {}
    g_score: Dict[Hashable, float] = {start: 0.0}
    open_set_hash: set[Hashable] = {start}

    while open_set:
        _, current = heapq.heappop(open_set)
        open_set_hash.remove(current)

        if current == goal:
            # reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor, edge_cost in neighbors(current):
            tentative_g = g_score[current] + weight(current, neighbor)
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score, neighbor))
                    open_set_hash.add(neighbor)
    return None


def main() -> None:

    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    try:
        R = int(next(it))
        C = int(next(it))
    except StopIteration:
        return

    grid = []
    for _ in range(R):
        row = []
        for _ in range(C):
            try:
                val = int(next(it))
            except StopIteration:
                val = 0
            row.append(val)
        grid.append(row)

    try:
        sr = int(next(it))
        sc = int(next(it))
        gr = int(next(it))
        gc = int(next(it))
    except StopIteration:
        sr = sc = gr = gc = 0

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < R and 0 <= c < C

    def passable(r: int, c: int) -> bool:
        return grid[r][c] == 0

    def neighbors(node: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        r, c = node
        res = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):  
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and passable(nr, nc):
                res.append(((nr, nc), 1.0))
        return res

    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  

    start = (sr, sc)
    goal = (gr, gc)

    if not (in_bounds(*start) and in_bounds(*goal) and passable(*start) and passable(*goal)):
        print("Invalid start/goal (out of bounds or on obstacle)")
        return

    path = astar(start, goal, neighbors, heuristic)

    if path is None:
        print("No path found.")
    else:
        print("Path length:", len(path) - 1)
        print(" -> ".join(str(p) for p in path))

        # Optional visualisation of the grid with the path
        visual = [list(row) for row in grid]
        for r, c in path:
            if visual[r][c] == 0:
                visual[r][c] = '*'
        visual[sr][sc] = 'S'
        visual[gr][gc] = 'G'
        for row in visual:
            print(' '.join(str(cell) for cell in row))


if __name__ == "__main__":
    main()
