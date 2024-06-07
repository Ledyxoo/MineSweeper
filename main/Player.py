def remove_flag(game_board, row, col):
    cell = game_board.get_cell()[row][col]
    if not cell.is_revealed and cell.is_flagged:
        cell.set_flagged(False)
        print(f"Flag removed from ({row}, {col})")
    else:
        print("No flag to remove or cell is revealed.")


def put_flag(game_board, row, col):
    if not game_board.get_cell()[row][col].is_revealed:
        game_board.get_cell()[row][col].set_flagged(True)
        print(f"Flag placed at ({row}, {col})")
    else:
        print("Cannot put a flag on a revealed cell.")
