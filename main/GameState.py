from enum import Enum


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    LOST = 3
    WON = 4
    CUSTOM = 5
    CUSTOM_MINES = 6
