class TicTacToeBoard:
    def __init__(self):
        self.board = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]

    def print_board(self):
        for row in self.board:
            print(' | '.join([val if val else ' ' for val in row]))
            print('-' * 9)

    def do_move(self, row, col, player):
        assert 0 <= row <= 2 and 0 <= col <= 2, "Invalid row or column. Try again."
        assert self.board[row][col] is None, "The location is already taken. Try again."
        assert player == 1 or player == 2, "Invalid player number. Try again."
        self.board[row][col] = 'X' if player == 1 else 'O'

    def did_win(self):
        for player in ['X', 'O']:
            for i in range(3):
                # check rows
                if all(self.board[i][j] == player for j in range(3)):
                    return True
                # check columns
                if all(self.board[j][i] == player for j in range(3)):
                    return True

            # check diagonals
            if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
                return True

            if self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
                return True

        return False

    def is_tie(self):
        for row in self.board:
            if None in row:
                return False
        return True

def start_game():
    board = TicTacToeBoard()
    current_player = 1

    while not board.did_win() and not board.is_tie():
        board.print_board()
        print(f"Current Player: {current_player}")
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                board.do_move(row, col, current_player) 
                break
            except AssertionError as e:
                print(e)
                continue
        current_player = 2 if current_player == 1 else 1

    board.print_board()
    if board.did_win():
        print(f"Player {2 if current_player == 1 else 1} wins!")
    elif board.is_tie():
        print("It's a tie!")


if __name__ == "__main__":
    start_game()