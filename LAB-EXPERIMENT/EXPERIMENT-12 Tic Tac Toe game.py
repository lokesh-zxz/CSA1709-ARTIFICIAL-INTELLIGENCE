# Tic Tac Toe using Minimax Algorithm

import math

# Display the board
def print_board(board):
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("-" * 9)

# Check winner
def check_winner(board):
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    # Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None

# Check if board is full
def is_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Minimax Algorithm
def minimax(board, is_max):
    winner = check_winner(board)

    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_full(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = max(best, minimax(board, False))
                    board[i][j] = ' '
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = min(best, minimax(board, True))
                    board[i][j] = ' '
        return best

# Find the best move
def best_move(board):
    best_score = -math.inf
    move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, False)
                board[i][j] = ' '

                if score > best_score:
                    best_score = score
                    move = (i, j)

    return move

# Main Game
board = [[' ' for _ in range(3)] for _ in range(3)]

print("Tic Tac Toe")
print("You are X")
print("Computer is O\n")

while True:
    print_board(board)

    # Player Move
    while True:
        row = int(input("\nEnter row (0-2): "))
        col = int(input("Enter column (0-2): "))

        if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == ' ':
            board[row][col] = 'X'
            break
        else:
            print("Invalid move. Try again.")

    if check_winner(board) == 'X':
        print_board(board)
        print("\nYou Win!")
        break

    if is_full(board):
        print_board(board)
        print("\nMatch Draw!")
        break

    # Computer Move
    row, col = best_move(board)
    board[row][col] = 'O'

    print("\nComputer played...\n")

    if check_winner(board) == 'O':
        print_board(board)
        print("\nComputer Wins!")
        break

    if is_full(board):
        print_board(board)
        print("\nMatch Draw!")
        break
