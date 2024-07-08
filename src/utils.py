import itertools
import time
import typing as t

import pygame


def circle_surf(radius: int, color) -> pygame.Surface:
    temp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(temp, color, (radius, radius), radius)

    return temp


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

    def __init__(self, colors: t.Sequence, cooldown: float) -> None:
        self.colors = itertools.cycle(colors)
        self.color = self._get()
        self.target_color = self._get()
        self.cooldown = cooldown
        self.timer = Time(cooldown)

    def _get(self) -> pygame.Color:
        return pygame.Color(next(self.colors))

    def update(self):
        if self.timer.tick():
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
