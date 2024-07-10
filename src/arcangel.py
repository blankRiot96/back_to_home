import math

import pygame

from src import shared, utils
from src.sparks import MetalExplosion


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
        self.taking_damage = False

    def take_damage(self, damage: int):
        self.taking_damage = True
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def update(self):
        self.pos.move_towards_ip(shared.player.pos, ArcAngel.SPEED * shared.dt)
        self.rect.topleft = self.pos

        tx, ty = shared.player.pos
        x, y = self.pos
        self.angle = -math.degrees(math.atan2(ty - y, tx - x))

    def draw(self):
        img = pygame.transform.rotate(self.image, self.angle)
        if self.taking_damage:
            img.fill((255, 0, 0, 150), special_flags=pygame.BLEND_RGBA_MIN)
            self.taking_damage = False
        rect = img.get_rect(center=self.orect.center + self.pos)
        shared.screen.blit(img, shared.camera.transform(rect))


class ArcAngelManager:
    def __init__(self) -> None:
        self.arcangels: list[ArcAngel] = [ArcAngel() for _ in range(5)]
        self.explosion = MetalExplosion()

    def update(self):
        for arcangel in self.arcangels[:]:
            arcangel.update()
            if not arcangel.alive:
                self.explosion.spawn(arcangel.rect.center)
                self.arcangels.remove(arcangel)

            for a2 in self.arcangels:
                if a2 is arcangel:
                    continue

                dist = arcangel.pos.distance_to(a2.pos)
                if dist < 50.0:
                    val = 50.0 - dist
                    angle = arcangel.angle + 90
                    arcangel.pos.x += math.cos(math.radians(angle)) * val
                    arcangel.pos.y += math.sin(math.radians(-angle)) * val
                    arcangel.rect.topleft = arcangel.pos
        self.explosion.update()

    def draw(self):
        for arcangel in self.arcangels:
            arcangel.draw()
        self.explosion.draw()
