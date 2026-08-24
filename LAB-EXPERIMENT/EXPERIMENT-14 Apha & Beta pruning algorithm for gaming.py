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


def alpha_beta(board, depth, alpha, beta, maximizing):
    # Terminal states
    if check_winner(board, 'O'):
        return 1

    if check_winner(board, 'X'):
        return -1

    if ' ' not in board:
        return 0

    # Maximizing player - Computer
    if maximizing:
        best_score = -float('inf')

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'

                score = alpha_beta(
                    board, depth + 1, alpha, beta, False
                )

                board[i] = ' '

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                # Alpha-Beta pruning
                if beta <= alpha:
                    break

        return best_score

    # Minimizing player - Human
    else:
        best_score = float('inf')

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'

                score = alpha_beta(
                    board, depth + 1, alpha, beta, True
                )

                board[i] = ' '

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                # Alpha-Beta pruning
                if beta <= alpha:
                    break

        return best_score


def find_best_move(board):
    best_score = -float('inf')
    best_move = -1

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'

            score = alpha_beta(
                board, 0, -float('inf'), float('inf'), False
            )

            board[i] = ' '

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


def display_board(board):
    print()
    for i in range(0, 9, 3):
        print(board[i], '|', board[i + 1], '|', board[i + 2])

        if i < 6:
            print("--+---+--")

    print()


# Main Program
board = [' '] * 9

print("TIC-TAC-TOE USING ALPHA-BETA PRUNING")
print("You are X")
print("Computer is O")
print("Enter positions from 1 to 9")

while True:

    display_board(board)

    # Human move
    move = int(input("Enter your move (1-9): ")) - 1

    if move < 0 or move > 8 or board[move] != ' ':
        print("Invalid move! Try again.")
        continue

    board[move] = 'X'

    # Check human win
    if check_winner(board, 'X'):
        display_board(board)
        print("You Win!")
        break

    # Check draw
    if ' ' not in board:
        display_board(board)
        print("Game Draw!")
        break

    # Computer move
    computer_move = find_best_move(board)
    board[computer_move] = 'O'

    print("Computer selected position:", computer_move + 1)

    # Check computer win
    if check_winner(board, 'O'):
        display_board(board)
        print("Computer Wins!")
        break

    # Check draw
    if ' ' not in board:
        display_board(board)
        print("Game Draw!")
        break
