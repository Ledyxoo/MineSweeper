def remove_flag(game_board, row, col):
    if game_board.board[row][col].is_flagged:
        game_board.board[row][col].is_flagged = False


def put_flag(game_board, row, col):
    if not game_board.board[row][col].is_revealed:
        game_board.board[row][col].is_flagged = True
