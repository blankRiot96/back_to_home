from __future__ import annotations

import typing as t

import pygame

if t.TYPE_CHECKING:
    from src.camera import Camera
    from src.player import Player


# Canvas
screen: pygame.Surface
srect: pygame.Rect
camera: Camera

# Events
events: list[pygame.event.Event]
mouse_pos: pygame.Vector2
mouse_press: tuple[int, ...]
keys: list[bool]
kp: list[bool]
kr: list[bool]
dt: float
clock: pygame.Clock

# Entities
player: Player
