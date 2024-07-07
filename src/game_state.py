import pygame

from src import shared
from src.background import Background
from src.camera import Camera
from src.mothership import MotherShip


class GameState:
    def __init__(self) -> None:
        self.next_state = None
        shared.camera = Camera()
        self.mothership = MotherShip()
        self.background = Background()

    def update(self):
        self.background.update()
        self.mothership.update()
        if self.mothership.spawned_player:
            shared.player.update()

    def draw(self):
        self.background.draw()
        self.mothership.draw()
        if self.mothership.spawned_player:
            shared.player.draw()
