import typing as t

import pygame

from src import shared


class Camera:
    def __init__(self) -> None:
        self.offset = pygame.Vector2()

    def attach_to(self, pos: t.Sequence):
        self.offset.x += (pos[0] - self.offset.x - (shared.srect.width // 2)) * 0.08
        self.offset.y += (pos[1] - self.offset.y - (shared.srect.height // 2)) * 0.08

    def transform(self, pos: t.Sequence) -> pygame.Vector2:
        return pygame.Vector2(pos[0] - self.offset.x, pos[1] - self.offset.y)
