from enum import Enum


class GameState(Enum):
    MENU = 1
    EXIT = 2
    PLAYING = 3
    LOST = 4
    WON = 5
