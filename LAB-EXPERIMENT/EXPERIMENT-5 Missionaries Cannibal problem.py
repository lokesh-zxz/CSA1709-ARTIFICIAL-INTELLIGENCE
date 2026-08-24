from collections import deque

def valid(m, c):
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False
    if m > 0 and m < c:
        return False
    if (3-m) > 0 and (3-m) < (3-c):
        return False
    return True

def neighbors(state):
    ml, cl, boat = state
    moves = [(1,0), (2,0), (0,1), (0,2), (1,1)]
    res = []
    for dm, dc in moves:
        if boat == 0:
            ns = (ml - dm, cl - dc, 1)
        else:
            ns = (ml + dm, cl + dc, 0)
        if valid(ns[0], ns[1]):
            res.append(ns)
    return res

def solve():
    start = (3, 3, 0)
    goal = (0, 0, 1)
    q = deque()
    q.append((start, []))
    seen = {start}
    while q:
        state, path = q.popleft()
        if state == goal:
            return path + [state]
        for ns in neighbors(state):
            if ns not in seen:
                seen.add(ns)
                q.append((ns, path + [state]))
    return None

if __name__ == "__main__":
    sol = solve()
    if sol:
        print("Steps:", len(sol)-1)
        for i, (ml, cl, b) in enumerate(sol):
            side = "left" if b == 0 else "right"
            print(f"Step {i}: {ml}M {cl}C left, boat {side}")
    else:
        print("No solution")
