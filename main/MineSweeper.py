import time

import pygame
from GameBoard import GameBoard
from GameState import GameState

# pygame setup
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Define game state
state = GameState.MENU

# Define game board
game_board = None

# Define game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
font = pygame.font.Font(None, 30)
# Define text input boxes
input_box_width, input_box_height = 200, 40
grid_size_input_box = pygame.Rect(300, 200, input_box_width, input_box_height)
mines_input_box = pygame.Rect(300, 300, input_box_width, input_box_height)
grid_size_text = font.render("Grid Size (rows x cols):", True, WHITE)
mines_text = font.render("Number of Mines:", True, WHITE)
grid_size_active = False
mines_active = False
grid_size = ""
mines = ""

# Definition of buttons
start_button = pygame.Rect(300, 400, 200, 50)
start_text = font.render("Start Game", True, WHITE)

# Back to menu button
menu_button = pygame.Rect(300, 450, 200, 50)
menu_text = font.render("Back to menu", True, WHITE)

# place mine button
place_mine_button = pygame.Rect(300, 500, 200, 50)
place_mine_text = font.render("Place mines", True, WHITE)


# Definition of the menu background function
def menu_background():
    menu_image = pygame.image.load("images/menu.png")
    menu_image_rect = menu_image.get_rect(center=(800 // 2, 600 // 2))
    screen.blit(menu_image, menu_image_rect)


# Draw the menu
def draw_menu():
    menu_background()
    menu_font = pygame.font.Font(None, 50)

    text_play = menu_font.render("1. Play", True, WHITE)
    text_play_rect = text_play.get_rect(center=(800 // 2, 600 // 2 + 50))
    screen.blit(text_play, text_play_rect)

    text_exit = menu_font.render("2. Exit", True, WHITE)
    text_exit_rect = text_exit.get_rect(center=(800 // 2, 600 // 2 + 100))
    screen.blit(text_exit, text_exit_rect)

    return text_play_rect, text_exit_rect


# Draw the game options
def draw_menu_play():
    menu_background()

    menu_font = pygame.font.Font(None, 50)
    options = ["1. Easy", "2. Medium", "3. Hard", "4. Custom", "5. Custom with mines", "6. Go back to menu"]
    rects = []
    for i, option in enumerate(options):
        text_play = menu_font.render(option, True, WHITE)
        text_play_rect = text_play.get_rect(center=(800 // 2, 500 // 2 + i * 50))
        screen.blit(text_play, text_play_rect)
        rects.append(text_play_rect)

    return rects


# Main game loop
def enter_grid_size_text():
    error_text_grid = input_font.render("Please enter grid size and number of mines.", True, RED)
    error_rect_grid = error_text_grid.get_rect(center=(800 // 2, 600 // 2 - 25))
    screen.blit(error_text_grid, error_rect_grid)
    pygame.display.update()
    time.sleep(3)


def draw_custom_input_and_buttons():
    pygame.draw.rect(screen, WHITE, grid_size_input_box, 2)
    pygame.draw.rect(screen, WHITE, mines_input_box, 2)

    # Calculate text positions for alignment
    grid_text_x = grid_size_input_box.x - grid_size_text.get_width() - 10
    mines_text_x = mines_input_box.x - mines_text.get_width() - 10

    screen.blit(grid_size_text, (grid_text_x, grid_size_input_box.y))
    screen.blit(mines_text, (mines_text_x, mines_input_box.y))
    screen.blit(start_text, start_button)
    screen.blit(menu_text, menu_button)


def draw_current_input_values(font_func):
    grid_surface = font_func.render(grid_size, True, WHITE)
    mines_surface = font_func.render(mines, True, WHITE)
    screen.blit(grid_surface, (grid_size_input_box.x + 5, grid_size_input_box.y + 5))
    screen.blit(mines_surface, (mines_input_box.x + 5, mines_input_box.y + 5))

    pygame.display.update()


def check_error_input():
    if rows > 18 or cols > 30 or rows < 3 or cols < 3:
        input_font_func = pygame.font.Font(None, 20)
        error_text_func = input_font_func.render("rows must be < 19 and > 2 and columns must be < 31 and > 2",
                                                 True, RED)
        error_rect_func = error_text_func.get_rect(center=(800 // 2, 600 // 2 - 25))
        screen.blit(error_text_func, error_rect_func)
        pygame.display.update()
        time.sleep(3)
        return False
    elif mines_count > (rows * cols):
        input_font_func = pygame.font.Font(None, 20)
        error_text_func = input_font_func.render("mines must be < rows * cols", True, RED)
        error_rect_func = error_text.get_rect(center=(800 // 2, 600 // 2 - 25))
        screen.blit(error_text_func, error_rect_func)
        pygame.display.update()
        time.sleep(3)
        return False
    return True


def event_type():
    global grid_size_active
    global mines_active
    global grid_size
    global mines

    if event.type == pygame.KEYDOWN:
        if grid_size_active:
            if event.key == pygame.K_RETURN:
                grid_size_active = False
            elif event.key == pygame.K_BACKSPACE:
                grid_size = grid_size[:-1]
            else:
                grid_size += event.unicode
        elif mines_active:
            if event.key == pygame.K_RETURN:
                mines_active = False
            elif event.key == pygame.K_BACKSPACE:
                mines = mines[:-1]
            else:
                mines += event.unicode
    if event.type == pygame.MOUSEBUTTONDOWN:
        if grid_size_input_box.collidepoint(event.pos):
            # Toggle active state of grid size input box
            grid_size_active = not grid_size_active
            mines_active = False
        elif mines_input_box.collidepoint(event.pos):
            # Toggle active state of mines input box
            mines_active = not mines_active
            grid_size_active = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == GameState.MENU and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            play_rect, exit_rect = draw_menu()
            if play_rect.collidepoint(mouse_pos):
                state = GameState.PLAYING
            elif exit_rect.collidepoint(mouse_pos):
                running = False
        elif state == GameState.PLAYING and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            option_rects = draw_menu_play()
            for idx, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    if idx == 0:
                        game = GameBoard(4, 4, 2)
                        GameBoard.start(game)
                    elif idx == 1:
                        game = GameBoard(8, 10, 15)
                        GameBoard.start(game)
                    elif idx == 2:
                        game = GameBoard(15, 20, 50)
                        GameBoard.start(game)
                    elif idx == 3:
                        state = GameState.CUSTOM
                    elif idx == 4:
                        state = GameState.CUSTOM_MINES
                    elif idx == 5:
                        state = GameState.MENU

    menu_background()

    if state == GameState.MENU:
        play_rect, exit_rect = draw_menu()
    elif state == GameState.PLAYING:
        option_rects = draw_menu_play()
    elif state == GameState.CUSTOM:
        # Draw custom input boxes and start button
        draw_custom_input_and_buttons()
        # Draw current input values
        draw_current_input_values(font)

        # Handle input events for custom settings
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    # Start button clicked, retrieve grid size and number of mines and start the game
                    if not grid_size or not mines:
                        # If either box is empty, display an error message
                        input_font = pygame.font.Font(None, 20)
                        enter_grid_size_text()
                    else:
                        rows, cols = map(int, grid_size.split('x'))
                        mines_count = int(mines)
                        if check_error_input() is False:
                            break
                        game = GameBoard(rows, cols, mines_count)
                        GameBoard.start(game)
                elif menu_button.collidepoint(mouse_pos):
                    state = GameState.MENU

            event_type()

        pygame.display.flip()
    elif state == GameState.CUSTOM_MINES:
        # Draw custom input boxes and start button
        draw_custom_input_and_buttons()
        screen.blit(place_mine_text, place_mine_button)

        # Draw current input values
        draw_current_input_values(font)

        # Handle input events for custom settings
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    if game_board is None:
                        error_text = font.render("place mines before", True, RED)
                        error_rect = error_text.get_rect(center=(800 // 2, 600 // 2 - 25))
                        screen.blit(error_text, error_rect)
                        pygame.display.update()
                        time.sleep(3)
                        break
                    GameBoard.start_for_custom(game_board)
                elif menu_button.collidepoint(mouse_pos):
                    state = GameState.MENU
                elif place_mine_button.collidepoint(mouse_pos):
                    # continue button clicked, retrieve grid size and number of mines and start the game
                    if not grid_size or not mines:
                        # If either box is empty, display an error message
                        enter_grid_size_text()
                    else:
                        rows, cols = map(int, grid_size.split('x'))
                        mines_count = int(mines)
                        if check_error_input() is False:
                            break
                        game_board = GameBoard(rows, cols, mines_count)
                        game_board.customize_mines()
            event_type()
        pygame.display.flip()

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
