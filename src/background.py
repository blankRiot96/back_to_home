import math
import random
import typing as t

import pygame

from src import shared, utils


class BorderSegment:
    WIDTH = 5
    HEIGHT = 75
    SPACING = 25
    IMG: pygame.Surface
    ROTAT_SPEED = 1.0
    N = 0

    def __init__(self) -> None:
        if not hasattr(BorderSegment, "IMG"):
            BorderSegment.IMG = pygame.Surface(
                (BorderSegment.WIDTH, BorderSegment.HEIGHT), pygame.SRCALPHA
            )
            BorderSegment.IMG.fill("red")

        self.image = BorderSegment.IMG.copy()
        self.n = BorderSegment.N
        BorderSegment.N += 1
        self.angle = self.n * 360 / Border.N_SEGMENTS
        self.pos = pygame.Vector2()

    def update(self):
        self.angle += BorderSegment.ROTAT_SPEED * shared.dt
        self.pos.x = math.cos(math.radians(self.angle)) * Border.RADIUS
        self.pos.y = math.sin(math.radians(-self.angle)) * Border.RADIUS

        self.pos += shared.srect.center
        self.angle %= 360

    def draw(self):
        self.image = pygame.transform.rotate(BorderSegment.IMG.copy(), self.angle)
        shared.screen.blit(self.image, shared.camera.transform(self.pos))


class Border:
    RADIUS = 2150
    CIRCUM = 2 * math.pi * RADIUS
    N_SEGMENTS = int(CIRCUM / (BorderSegment.HEIGHT + BorderSegment.SPACING))

    def __init__(self) -> None:
        self.segements = [BorderSegment() for _ in range(Border.N_SEGMENTS)]
        self.font = pygame.Font(None, 32)
        self.color_cycle = utils.ColorCycle(["red", "#db9a00"], 0.001)

    def update(self):
        self.color_cycle.update()
        BorderSegment.IMG.fill(self.color_cycle.color)
        for segment in self.segements:
            segment.update()

        if not hasattr(shared, "player"):
            return

        if shared.player.pos.distance_to(shared.srect.center) > Border.RADIUS:
            print(f"DEATH {random.randrange(10)}")

    def draw(self):
        for segment in self.segements:
            if not shared.srect.collidepoint(*shared.camera.transform(segment.pos)):
                continue
            segment.draw()


class BloomLayer:
    def __init__(self, n: int, colors: t.Sequence, cooldown: float) -> None:
        self.original_image = pygame.image.load(
            f"assets/images/level_1/bloom_{n}.png"
        ).convert_alpha()
        self.orect = self.original_image.get_rect()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = shared.srect.center
        self.color_cycle = utils.ColorCycle(colors, cooldown)

    def update(self):
        self.color_cycle.update()

        center_vec = pygame.Vector2(self.rect.width // 2, self.rect.height // 2)
        rect = shared.srect.copy()
        rect.center = center_vec + shared.camera.offset
        if not self.orect.contains(rect):
            rect.clamp_ip(self.orect)

        self.image = self.original_image.subsurface(rect).copy()
        self.image.fill(self.color_cycle.color, special_flags=pygame.BLEND_RGBA_MIN)

    def draw(self):
        shared.screen.blit(self.image, (0, 0))


class Star:
    pass


class StarManager:
    pass


class Background:
    def __init__(self) -> None:
        self.blooms = [
            # BloomLayer(1, ["red", "blue"], 0.05),
            BloomLayer(2, ["#0a205a", "#040c24"], 0.0),
            BloomLayer(3, ["#e303fc", "#0362fc"], 0.0),
        ]
        self.border = Border()

    def update(self):
        for bloom in self.blooms:
            bloom.update()
        self.border.update()

    def draw(self):
        for bloom in self.blooms:
            bloom.draw()
        self.border.draw()
