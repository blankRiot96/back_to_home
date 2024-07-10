import pygame

from src import shared, utils


class DamageText:
    def __init__(self, damage: int) -> None:
        self.damage = damage
        self.font = utils.load_font(None, 20)
        self.original_surf = self.font.render(f"-{damage}", True, "red")
        self.surf = self.original_surf.copy()

    def update(self):
        pass

    def draw(self):
        pass
