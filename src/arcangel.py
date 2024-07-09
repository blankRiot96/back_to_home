import math

import pygame

from src import shared, utils


class ArcAngel:
    SPEED = 30.0
    HP = 100

    def __init__(self) -> None:
        self.image = utils.load_image("assets/images/arcangel.png", True, True, 0.5)
        self.orect = self.image.get_rect()
        self.rect = self.orect.copy()
        self.pos = pygame.Vector2()
        self.angle = 0.0
        self.alive = True
        self.hp = ArcAngel.HP

    def update(self):
        self.pos.move_towards_ip(shared.player.pos, ArcAngel.SPEED * shared.dt)
        self.rect.topleft = self.pos

        if self.hp <= 0:
            self.alive = False

        tx, ty = shared.player.pos
        x, y = self.pos
        self.angle = -math.degrees(math.atan2(ty - y, tx - x))

    def draw(self):
        img = pygame.transform.rotate(self.image, self.angle)
        rect = img.get_rect(center=self.orect.center + self.pos)
        shared.screen.blit(img, shared.camera.transform(rect))


class ArcAngelManager:
    def __init__(self) -> None:
        self.arcangels: list[ArcAngel] = [ArcAngel()]

    def update(self):
        for arcangel in self.arcangels[:]:
            arcangel.update()
            if not arcangel.alive:
                self.arcangels.remove(arcangel)

    def draw(self):
        for arcangel in self.arcangels:
            arcangel.draw()
