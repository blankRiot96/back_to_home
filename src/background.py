import itertools

import pygame

from src import shared, utils


class Border:
    N_FRAMES = 360

    def __init__(self) -> None:
        self.original_image = pygame.image.load(
            "assets/images/level_1/border.png"
        ).convert_alpha()
        self.original_image = self.original_image.subsurface(
            self.original_image.get_bounding_rect()
        ).copy()
        self.image = self.original_image.copy()
        self.original_rect = self.original_image.get_rect()
        self.rect = self.original_rect.copy()

        self.rotate_cooldown = utils.Time(0.1)
        self.load_frames()

    def load_frames(self):
        self.frames = []
        angle = 0.0
        step = 360 / Border.N_FRAMES
        for _ in range(Border.N_FRAMES):
            angle += step
            image = pygame.transform.rotate(self.original_image, angle)
            self.frames.append(image)

        self.frames = itertools.cycle(self.frames)

    def update(self):
        if self.rotate_cooldown.tick():
            self.image = next(self.frames)

        if not hasattr(shared, "player"):
            return

        if (
            shared.player.pos.distance_to(self.original_rect.center)
            > self.original_rect.width / 2
        ):
            print("DEATH")

    def draw(self):
        self.rect = self.image.get_rect(center=self.original_rect.center)
        shared.screen.blit(self.image, shared.camera.transform(self.rect))


class Background:
    def __init__(self) -> None:
        self.original_image = pygame.image.load(
            "assets/images/level_1/bloom_1.png"
        ).convert_alpha()
        self.image = self.original_image.copy()
        self.color_cycle = itertools.cycle((pygame.Color("red"), pygame.Color("blue")))
        self.color = pygame.Color(next(self.color_cycle))
        self.target_color = pygame.Color(next(self.color_cycle))
        self.trans_cooldown = utils.Time(0.05)

        self.border = Border()

    def update(self):
        if self.trans_cooldown.tick():
            self.color = utils.lerp_color(self.color[:3], self.target_color[:3])

        if self.color == self.target_color:
            self.target_color = pygame.Color(next(self.color_cycle))

        self.image = self.original_image.copy()
        self.image.fill(self.color, special_flags=pygame.BLEND_RGBA_MIN)

        self.border.update()

    def draw(self):
        shared.screen.blit(self.image, shared.camera.transform((0, 0)))
        self.border.draw()
