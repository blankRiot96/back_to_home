import time
import typing as t

import pygame


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


def lerp_color(color_1: t.Sequence, color_2: t.Sequence) -> tuple[int, int, int]:
    r, g, b = color_1
    target_r, target_g, target_b = color_2

    r += 0 if r == target_r else [-1, 1][r < target_r]
    g += 0 if g == target_g else [-1, 1][g < target_g]
    b += 0 if b == target_b else [-1, 1][b < target_b]

    return r, g, b
