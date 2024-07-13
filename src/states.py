import typing as t

from src.enums import State
from src.game_state import GameState
from src.main_menu import MainMenu
from src.victory_state import VictoryState


class StateLike(t.Protocol):
    next_state: State | None

    def update(self): ...

    def draw(self): ...


class StateManager:
    def __init__(self) -> None:
        self.state_dict: dict[State, StateLike] = {
            State.GAME: GameState,
            State.MAIN_MENU: MainMenu,
            State.VICTORY: VictoryState,
        }

        self.state_enum = State.MAIN_MENU
        self.state_obj: StateLike = self.state_dict.get(self.state_enum)()

    @property
    def state_enum(self) -> State:
        return self.__state_enum

    @state_enum.setter
    def state_enum(self, next_state: State) -> None:
        self.__state_enum = next_state
        self.state_obj: StateLike = self.state_dict.get(self.__state_enum)()

    def update(self):
        self.state_obj.update()
        if self.state_obj.next_state is not None:
            self.state_enum = self.state_obj.next_state

    def draw(self):
        self.state_obj.draw()
