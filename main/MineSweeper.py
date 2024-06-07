import pygame
from main.GameBoard import GameBoard
from main.GameState import GameState

# pygame setup
pygame.init()
screen_width, screen_height = 1280, 720
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


# Define game functions
def draw_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("MineSweeper", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text, text_rect)

    text_play = font.render("1. Play", True, WHITE)
    text_play_rect = text_play.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(text_play, text_play_rect)

    text_exit = font.render("2. Exit", True, WHITE)
    text_exit_rect = text_exit.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
    screen.blit(text_exit, text_exit_rect)

    return text_play_rect, text_exit_rect


def draw_menu_play():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)

    options = ["1. Easy", "2. Medium", "3. Hard", "4. Custom", "5. Custom with mines"]
    rects = []
    for i, option in enumerate(options):
        text_play = font.render(option, True, WHITE)
        text_play_rect = text_play.get_rect(center=(screen_width // 2, screen_height // 2 + 50 + i * 30))
        screen.blit(text_play, text_play_rect)
        rects.append(text_play_rect)

    return rects


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == GameState.MENU and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            play_button_rect, exit_button_rect = draw_menu()
            if play_button_rect.collidepoint(mouse_pos):
                state = GameState.PLAYING
            elif exit_button_rect.collidepoint(mouse_pos):
                running = False
        elif state == GameState.PLAYING and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            option_rects = draw_menu_play()
            for idx, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    if idx == 0:
                        game = GameBoard(8, 10, 10)
                        GameBoard.start(game)
                    # Here you can handle starting the game with the selected difficulty

    if state == GameState.MENU:
        play_button_rect, exit_button_rect = draw_menu()
    elif state == GameState.PLAYING:
        option_rects = draw_menu_play()

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
