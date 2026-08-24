import sys
import math
from typing import List, Tuple
def tsp_held_karp(dist: List[List[float]]) -> Tuple[float, List[int]]:
    n = len(dist)
    if n == 0:
        return 0.0, []
    if n == 1:
        return 0.0, [0]
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    dp[1][0] = 0.0                     

    for mask in range(1 << n):
        if not (mask & 1):          
            continue
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            cur = dp[mask][u]
            if cur == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue          
                nxt = mask | (1 << v)
                new_cost = cur + dist[u][v]
                if new_cost < dp[nxt][v]:
                    dp[nxt][v] = new_cost
                    parent[nxt][v] = u

    full_mask = (1 << n) - 1
    best_cost = INF
    last = -1
    for u in range(1, n):               
        cost = dp[full_mask][u] + dist[u][0]
        if cost < best_cost:
            best_cost = cost
            last = u
    if last == -1:                      
        return INF, []
    path = [0]
    mask = full_mask
    cur = last
    while cur != -1:
        path.append(cur)
        prev = parent[mask][cur]
        mask ^= (1 << cur)
        cur = prev
    path.reverse()
    path.append(0)                     
    return best_cost, path
def tsp_nearest_neighbor(dist: List[List[float]], start: int = 0) -> Tuple[float, List[int]]:
    n = len(dist)
    if n == 0:
        return 0.0, []
    visited = [False] * n
    tour = [start]
    visited[start] = True
    cur = start
    total = 0.0
    for _ in range(n - 1):
        nxt = -1
        best = float('inf')
        for v in range(n):
            if not visited[v] and dist[cur][v] < best:
                best = dist[cur][v]
                nxt = v
        if nxt == -1:                    
            break
        visited[nxt] = True
        tour.append(nxt)
        total += best
        cur = nxt

    total += dist[cur][start]           
    tour.append(start)
    return total, tour
if __name__ == "__main__":
    example_dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print("=== Held‑Karp (exact) ===")
    cost, path = tsp_held_karp(example_dist)
    print(f"Minimum cost: {cost}")
    print(f"Tour: {path}")
    print("\n=== Nearest Neighbor (heuristic) ===")
    cost2, path2 = tsp_nearest_neighbor(example_dist)
    print(f"Tour cost: {cost2}")
    print(f"Tour: {path2}")
