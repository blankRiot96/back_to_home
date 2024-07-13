import functools
import itertools
import time
import typing as t

import pygame


@functools.lru_cache
def load_image(
    path: str,
    alpha: bool,
    bound: bool = False,
    scale: float = 1.0,
    smooth: bool = False,
) -> pygame.Surface:
    img = pygame.image.load(path)
    if scale != 1.0:
        if smooth:
            img = pygame.transform.smoothscale_by(img, scale)
        else:
            img = pygame.transform.scale_by(img, scale)
    if bound:
        img = img.subsurface(img.get_bounding_rect()).copy()
    if alpha:
        return img.convert_alpha()
    return img.convert()


@functools.lru_cache
def load_font(name: str | None, size: int) -> pygame.Font:
    return pygame.Font(name, size)


def circle_surf(radius: int, color) -> pygame.Surface:
    temp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(temp, color, (radius, radius), radius)

    return temp


def oval_surf(width, height, color) -> pygame.Surface:
    temp = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(temp, color, (0, 0, width, height))

    return temp


class Animation:
    def __init__(self, frames: list[pygame.Surface], speed: float):
        self.frames = frames
        self.speed = speed

        self.f_len = len(frames)
        self.index = 0
        self.image = self.frames[self.index]

    def update(self, dt):
        self.index += self.speed * dt
        if self.index > self.f_len - 1:
            self.index = 0

        self.image = self.frames[int(self.index)]

    def draw(self, screen: pygame.Surface, pos: tuple[int, int]):
        screen.blit(self.image, pos)

    def play(self, screen, pos, dt):
        self.update(dt)
        self.draw(screen, pos)


class Time:
    """
    Class to check if time has passed.
    """

    def __init__(self, time_to_pass: float):
        self.time_to_pass = time_to_pass
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def tick(self) -> bool:
        if time.perf_counter() - self.start > self.time_to_pass:
            self.start = time.perf_counter()
            return True
        return False


class ColorCycle:
    """Cycle through some colors"""

    def __init__(self, colors: t.Sequence, cooldown: float, loops: int = 1) -> None:
        self.colors = itertools.cycle(colors)
        self.color = self._get()
        self.target_color = self._get()
        self.cooldown = cooldown
        self.timer = Time(cooldown) if cooldown else None
        self.loops = loops

    def _get(self) -> pygame.Color:
        return pygame.Color(next(self.colors))

    def update(self):
        if not self.cooldown or self.timer.tick():
            for _ in range(self.loops):
                self.color = lerp_color(self.color[:3], self.target_color[:3])

                if self.color == self.target_color:
                    self.target_color = self._get()


def lerp_color(color_1: t.Sequence, color_2: t.Sequence) -> tuple[int, int, int]:
    r, g, b = color_1
    target_r, target_g, target_b = color_2

    r += 0 if r == target_r else [-1, 1][r < target_r]
    g += 0 if g == target_g else [-1, 1][g < target_g]
    b += 0 if b == target_b else [-1, 1][b < target_b]

    return r, g, b
