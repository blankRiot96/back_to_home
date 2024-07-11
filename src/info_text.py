import random

import pygame

from src import shared, utils


class DamageText:
    ALPHA_REDUCTION = 50.5
    SIZE_REDUCTION = 0.1

    def __init__(self, damage: int, pos: tuple[int, int]) -> None:
        self.damage = damage
        self.font = utils.load_font(None, 30)
        self.original_surf = self.font.render(f"-{damage}", True, "red")
        self.surf = self.original_surf.copy()
        self.pos = pygame.Vector2(pos)
        self.rect = self.surf.get_rect(topleft=self.pos)
        self.size_factor = 1.0
        self.alpha = 255
        self.alive = True

        self.dx = random.uniform(50.0, 100.0) * random.choice((-1, 1))

    def update(self):
        self.alpha -= DamageText.ALPHA_REDUCTION * shared.dt
        self.size_factor -= DamageText.SIZE_REDUCTION * shared.dt
        self.pos.x += self.dx * shared.dt
        self.pos.y -= 10.7 * shared.dt

        if self.alpha <= 10:
            self.alive = False

        self.surf = pygame.transform.scale_by(self.original_surf, self.size_factor)
        self.surf.set_alpha(self.alpha)
        self.rect = self.surf.get_rect(topleft=self.pos)

    def draw(self):
        shared.screen.blit(self.surf, shared.camera.transform(self.rect))


class DamageTextManager:
    def __init__(self) -> None:
        self.texts: list[DamageText] = []

    def spawn(self, damage: int, pos: tuple[int, int]):
        self.texts.append(DamageText(damage, pos))

    def update(self):
        for text in self.texts[:]:
            text.update()

            if not text.alive:
                self.texts.remove(text)

    def draw(self):
        for text in self.texts:
            text.draw()
