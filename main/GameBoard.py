import random
import time

from main.Cell import Cell
from main.GameState import GameState
import Player


def put_flag_action(game_board):
    row = int(input("Enter row: "))
    col = int(input("Enter column: "))
    if game_board.validate_coordinates(row, col) and game_board.validate_flag_action(row, col):
        Player.put_flag(game_board, row, col)
        game_board.nb_flags -= 1


def remove_flag_action(game_board):
    row = int(input("Enter row: "))
    col = int(input("Enter column: "))
    if game_board.validate_coordinates(row, col):
        Player.remove_flag(game_board, row, col)
        game_board.nb_flags += 1


class GameBoard:
    def __init__(self, rows=None, cols=None, mines=None, player=None):
        self.rows = rows
        self.cols = cols
        if mines > rows * cols:
            print("Too many mines")
            exit(0)
        self.mines = mines
        self.nb_flags = mines
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.player = player
        self.state = GameState.PLAYING
        self.mines_placed = 0
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def initialize_board(self):
        self.board = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    def place_mines(self):
        while self.mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.board[row][col].is_mine:
                self.board[row][col].set_mine(True)
                self.mines_placed += 1

    def place_mines_custom(self):
        print("Enter the coordinates of the mines (row col), one per line.")
        mines_to_place = self.mines

        while mines_to_place > 0:
            print(f"Mines left to place {mines_to_place}: ", end="")
            input_line = input().strip()

            coordinates = input_line.split()
            if len(coordinates) == 2:
                try:
                    row = int(coordinates[0])
                    col = int(coordinates[1])

                    if self.is_valid_cell(row, col) and not self.board[row][col].is_mine:
                        self.board[row][col].set_mine(True)
                        mines_to_place -= 1
                    else:
                        print("Invalid coordinates or mine already placed at this location. Try again.")
                except ValueError:
                    print("Invalid input. Please enter valid integers for row and column.")
            else:
                print("Invalid input. Please enter coordinates as 'row col'.")

    def print_board(self):
        for row in self.board:
            for cell in row:
                if cell.is_revealed:
                    if cell.is_mine:
                        print("💣", end=" ")
                    else:
                        adjacent_mines = cell.adjacent_mines
                        print(f"{adjacent_mines}️⃣" if adjacent_mines > 0 else "0️⃣", end=" ")
                elif cell.is_flagged:
                    print("🚩", end=" ")
                else:
                    print("⬛", end=" ")
            print()

    def game_logic(self):
        while self.state == GameState.PLAYING:
            print(f"Flags left: {self.nb_flags}")
            self.print_board()
            print("What do you want to do?\n 1. Put Flag\n 2. Remove Flag\n 3. Reveal \n 4. Save")
            action = input()
            if action == "1":
                put_flag_action(self)
            elif action == "2":
                remove_flag_action(self)
            elif action == "3":
                self.reveal_action()
            else:
                print("Invalid command")

            self.is_lost()
            self.is_won()

        self.end_time = int(time.time() * 1000)
        self.elapsed_time += self.end_time - self.start_time
        print(f"Time elapsed: {self.elapsed_time / 1000} seconds")
        game_result = (self.state == GameState.WON)
        self.print_board()
        self.state = GameState.MENU

    def start(self):
        self.initialize_board()
        self.place_mines()
        self.place_numbers()
        self.start_time = int(time.time() * 1000)
        self.game_logic()

    def start_for_custom(self):
        self.place_numbers()
        self.start_time = int(time.time() * 1000)
        self.game_logic()

    def continue_game(self):
        self.game_logic()

    def is_valid_cell(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_lost(self):
        for row in self.board:
            for cell in row:
                if cell.is_mine and cell.is_revealed:
                    print("You lost!")
                    self.reveal_all_board()
                    self.state = GameState.LOST
                    return

    def is_won(self):
        revealed_cells = sum(cell.is_revealed for row in self.board for cell in row)
        if revealed_cells == self.rows * self.cols - self.mines:
            print("You won!")
            self.reveal_all_board()
            self.state = GameState.WON

    def reveal_action(self):
        row = int(input("Enter row: "))
        col = int(input("Enter column: "))

        if self.validate_coordinates(row, col) and self.validate_reveal_action(row, col):
            self.reveal_empty_cells(row, col)

    def validate_coordinates(self, row, col):
        if not self.is_valid_cell(row, col):
            print("Invalid coordinates")
            return False
        return True

    def validate_flag_action(self, row, col):
        if self.board[row][col].is_revealed:
            print("Cannot put a flag on a revealed cell.")
            return False
        if self.board[row][col].is_flagged:
            print("Cell already flagged.")
            return False
        if self.nb_flags <= 0:
            print("No more flags available.")
            return False
        return True

    def validate_reveal_action(self, row, col):
        if self.board[row][col].is_revealed:
            print("Cell already revealed.")
            return False
        if self.board[row][col].is_flagged:
            print("Cannot reveal a flagged cell.")
            return False
        return True

    def reveal_all_board(self):
        for row in self.board:
            for cell in row:
                cell.set_revealed(True)

    def reveal_empty_cells(self, row, col):
        if not self.is_valid_cell(row, col) or self.board[row][col].is_revealed:
            return

        self.board[row][col].set_revealed(True)
        if self.board[row][col].adjacent_mines == 0:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if r != row or c != col:
                        self.reveal_empty_cells(r, c)

    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if self.is_valid_cell(i, j) and self.board[i][j].is_mine:
                    count += 1
        return count

    def place_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.board[row][col].is_mine:
                    count = self.count_adjacent_mines(row, col)
                    self.board[row][col].set_adjacent_mines(count)

    def get_cell(self):
        return self.board
