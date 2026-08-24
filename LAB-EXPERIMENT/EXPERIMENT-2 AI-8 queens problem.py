def print_board(board):
    """Print the chessboard with Q for queens and . for empty squares."""
    for row in board:
        line = " ".join("Q" if col == 1 else "." for col in row)
        print(line)
    print()   # blank line after each board


def is_safe(board, row, col):
    """Check if placing a queen at (row, col) is safe."""
    # check this row on left side
    for c in range(col):
        if board[row][c] == 1:
            return False

    # check upper diagonal on left side
    r, c = row, col
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return False
        r -= 1
        c -= 1

    # check lower diagonal on left side
    r, c = row, col
    while r < 8 and c >= 0:
        if board[r][c] == 1:
            return False
        r += 1
        c -= 1

    return True


def solve_queens(board, col):
    """Recursive back‑tracking to place queens column by column."""
    # base case: all queens are placed
    if col >= 8:
        return True

    # try placing queen in each row of this column
    for r in range(8):
        if is_safe(board, r, col):
            board[r][col] = 1               # place queen
            if solve_queens(board, col + 1): # recur for next column
                return True
            board[r][col] = 0               # backtrack

    return False   # no placement worked in this column


def main():
    # create an empty 8x8 board (0 = empty, 1 = queen)
    board = [[0 for _ in range(8)] for _ in range(8)]

    if solve_queens(board, 0):
        print("One solution for the 8‑Queens problem:")
        print_board(board)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
