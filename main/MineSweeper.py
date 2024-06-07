from typing import List

from main.GameBoard import GameBoard
from main.GameState import GameState


class MineSweeper:
    state = GameState.MENU

    @staticmethod
    def main():
        print("Hello Welcome to MineSweeper!")
        MineSweeper.state = GameState.MENU

        while MineSweeper.state != GameState.EXIT:
            if MineSweeper.state == GameState.MENU:
                MineSweeper.show_main_menu()
            elif MineSweeper.state == GameState.PLAYING:
                MineSweeper.state = GameState.MENU

    @staticmethod
    def show_main_menu():
        print("What do you want to do ?\n 1. Play\n 2. Exit")
        choice = input().strip()
        if choice == "1":
            print("Choose difficulty:\n 1. Easy\n 2. Medium\n 3. Hard\n 4. Custom\n 5. Custom with mines")
            MineSweeper.start_game()
        elif choice == "2":
            print("Exiting game...")
            MineSweeper.state = GameState.EXIT
        else:
            print("Invalid command")

    @staticmethod
    def start_game():
        choice = input().strip()
        if choice == "1":
            print("Starting game...Easy mode")
            game = GameBoard(2, 2, 1)
            GameBoard.start(game)
        elif choice == "2":
            print("Starting game...Medium mode")
            game2 = GameBoard(6, 6, 5)
            GameBoard.start(game2)
        elif choice == "3":
            print("Starting game...Hard mode")
            game3 = GameBoard(9, 9, 10)
            GameBoard.start(game3)
        elif choice == "4":
            rows = int(input("Enter number of rows: ").strip())
            cols = int(input("Enter number of columns: ").strip())
            mines = int(input("Enter number of mines: ").strip())
            game4 = GameBoard(rows, cols, mines)
            GameBoard.start(game4)
        elif choice == "5":
            rows2 = int(input("Enter number of rows: ").strip())
            cols2 = int(input("Enter number of columns: ").strip())
            total_mines = int(input("Enter total number of mines: ").strip())
            game5 = GameBoard(rows2, cols2, total_mines)
            GameBoard.initialize_board(game5)
            GameBoard.place_mines_custom(game5)
            GameBoard.start_for_custom(game5)
        else:
            print("Invalid command")


if __name__ == "__main__":
    MineSweeper.main()
