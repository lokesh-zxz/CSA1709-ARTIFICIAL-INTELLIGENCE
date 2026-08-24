def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if ' ' not in board:
        return 0
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(best_score, score)

        return best_score
def check_winner(board, player):
    winning_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] == player:
            return True
    return False
def find_best_move(board):
    best_score = -float('inf')
    best_move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move
def display_board(board):
    print()
    for i in range(0, 9, 3):
        print(board[i], '|', board[i+1], '|', board[i+2])
        if i < 6:
            print('--+---+--')
    print()
board = [' '] * 9
print("Tic-Tac-Toe using Minimax Algorithm")
print("You are X, Computer is O")
print("Positions are numbered 1 to 9")
while True:
    display_board(board)
    move = int(input("Enter your move (1-9): ")) - 1
    if move < 0 or move > 8 or board[move] != ' ':
        print("Invalid move! Try again.")
        continue
    board[move] = 'X'
    if check_winner(board, 'X'):
        display_board(board)
        print("You Win!")
        break
    if ' ' not in board:
        display_board(board)
        print("It's a Draw!")
        break
    computer_move = find_best_move(board)
    board[computer_move] = 'O'
    print("Computer chose position:", computer_move + 1)
    if check_winner(board, 'O'):
        display_board(board)
        print("Computer Wins!")
        break
    if ' ' not in board:
        display_board(board)
        print("It's a Draw!")
        break
