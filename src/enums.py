from enum import Enum, auto


class State(Enum):
    MAIN_MENU = auto()
    LEVEL_PICKER = auto()
    GAME = auto()
