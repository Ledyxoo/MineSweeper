import random
import time
import pygame

from Cell import Cell
from GameState import GameState
import Player

pygame.init()

font = pygame.font.Font(None, 60)
win_text = font.render("WIN", True, (0, 255, 0))
lose_text = font.render("LOSE", True, (255, 0, 0))


def put_flag_action(game_board, row, col):
    if game_board.validate_coordinates(row, col) and game_board.validate_flag_action(row, col):
        Player.put_flag(game_board, row, col)
        game_board.nb_flags -= 1


def remove_flag_action(game_board, row, col):
    if game_board.validate_coordinates(row, col):
        Player.remove_flag(game_board, row, col)
        game_board.nb_flags += 1


def resize_menu_window():
    pygame.display.set_mode((800, 600))


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
        self.screen = None  # Initialize screen later
        self.cell_size = 40  # Default cell size
        self.first_click = True  # To track if the first click has been made

        # Load images
        self.images = {
            "unrevealed": pygame.image.load('images/unrevealed.png'),
            "empty": pygame.image.load('images/empty.png'),
            "flag": pygame.image.load('images/flag.png'),
            "mine": pygame.image.load('images/mine.png'),
            "bar": pygame.image.load('images/bar.png'),
        }

        for i in range(1, 9):  # Load images for numbers 1 to 8
            self.images[str(i)] = pygame.image.load(f'images/{i}.png')

    def place_mines(self, initial_row, initial_col):
        while self.mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            # Ensure mines are not placed on the first clicked cell or its adjacent cells*
            if (row, col) != (initial_row, initial_col) and not self.board[row][col].is_mine:
                if self.mines > ((68 / 100) * (self.rows * self.cols)) or (self.rows * self.cols) <= 9:
                    self.board[row][col].set_mine(True)
                    self.mines_placed += 1
                else:
                    if not (initial_row - 1 <= row <= initial_row + 1 and initial_col - 1 <= col <= initial_col + 1):
                        self.board[row][col].set_mine(True)
                        self.mines_placed += 1

    def resize_window(self):
        min_window_size = 600
        max_dimension = max(self.rows, self.cols)
        self.cell_size = max(min_window_size // max_dimension, 40)
        width = self.cols * self.cell_size
        height = self.rows * self.cell_size + 50
        self.screen = pygame.display.set_mode((width, height))

    def game_logic(self):
        self.resize_window()
        while self.state == GameState.PLAYING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = self.get_cell(mouse_pos)
                    if pygame.mouse.get_pressed()[0]:  # Left click
                        if self.first_click:
                            self.place_mines(row, col)
                            self.place_numbers()
                            self.first_click = False
                        self.reveal_action(row, col)
                    elif pygame.mouse.get_pressed()[2]:  # Right click
                        if self.board[row][col].is_flagged:
                            remove_flag_action(self, row, col)
                        else:
                            put_flag_action(self, row, col)

            self.is_lost()
            self.is_won()
            self.draw_board()
            pygame.display.flip()

        self.state = GameState.MENU
        resize_menu_window()

    def customize_mines(self):
        self.resize_window()
        self.reveal_all_board()
        while self.mines_placed < self.mines:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = self.get_cell(mouse_pos)
                    if pygame.mouse.get_pressed()[0]:  # Left click to place a mine
                        if not self.board[row][col].is_mine:
                            self.board[row][col].set_mine(True)
                            self.mines_placed += 1
                    elif pygame.mouse.get_pressed()[2]:  # Right click to remove a mine
                        if self.board[row][col].is_mine:
                            self.board[row][col].set_mine(False)
                            self.mines_placed -= 1
            self.draw_board()
            pygame.display.flip()
        self.no_reveal_all_board()
        resize_menu_window()
        return self

    def start(self):
        self.game_logic()

    def start_for_custom(self):
        self.place_numbers()
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
                    self.draw_board()
                    self.screen.blit(lose_text, (self.screen.get_width() // 2 - lose_text.get_width() // 2,
                                                 self.screen.get_height() // 2 - lose_text.get_height() // 2))
                    pygame.display.flip()
                    self.state = GameState.LOST
                    time.sleep(5)
                    return

    def is_won(self):
        revealed_cells = sum(cell.is_revealed for row in self.board for cell in row)
        if revealed_cells == self.rows * self.cols - self.mines:
            print("You won!")
            self.reveal_all_board()
            self.draw_board()
            self.screen.blit(win_text, (self.screen.get_width() // 2 - win_text.get_width() // 2,
                                        self.screen.get_height() // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            self.state = GameState.WON
            time.sleep(5)
            return

    def reveal_action(self, row, col):
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

    def no_reveal_all_board(self):
        for row in self.board:
            for cell in row:
                cell.set_revealed(False)

    def reveal_empty_cells(self, row, col):
        if not self.is_valid_cell(row, col) or self.board[row][col].is_revealed:
            return

        self.board[row][col].set_revealed(True)
        if self.board[row][col].adjacent_mines == 0:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if self.is_valid_cell(r, c) and (r != row or c != col):
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

    def get_cell(self, mouse_pos):
        row = (mouse_pos[1] - 50) // self.cell_size
        col = mouse_pos[0] // self.cell_size
        return row, col

    def draw_board(self):
        self.screen.blit(self.images["bar"], (0, 0))
        flag_text = font.render(f"Flags: {self.nb_flags}", True, (255, 255, 255))
        self.screen.blit(flag_text, (10, 10))
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                rect = pygame.Rect(col * self.cell_size, (row * self.cell_size) + 50, self.cell_size,
                                   self.cell_size)
                if cell.is_revealed:
                    if cell.is_mine:
                        image = pygame.transform.scale(self.images["mine"], (self.cell_size, self.cell_size))
                    else:
                        adjacent_mines = str(cell.adjacent_mines)
                        if adjacent_mines == "0":
                            image = pygame.transform.scale(self.images["empty"], (self.cell_size, self.cell_size))
                        else:
                            image = pygame.transform.scale(self.images[adjacent_mines],
                                                           (self.cell_size, self.cell_size))
                elif cell.is_flagged:
                    image = pygame.transform.scale(self.images["flag"], (self.cell_size, self.cell_size))
                else:
                    image = pygame.transform.scale(self.images["unrevealed"], (self.cell_size, self.cell_size))
                self.screen.blit(image, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
