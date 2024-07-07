import pygame

from src import shared
from src.enums import State


class MainMenu:
    def __init__(self) -> None:
        self.next_state = None

    def update(self):
        if shared.kp[pygame.K_TAB]:
            self.next_state = State.GAME

    def draw(self):
        pass
