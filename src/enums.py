from enum import Enum, auto


class State(Enum):
    MAIN_MENU = auto()
    INTRO = auto()
    GAME = auto()
    VICTORY = auto()
