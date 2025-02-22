from __future__ import annotations

import typing as t

import pygame

if t.TYPE_CHECKING:
    from src.arcangel import ArcAngelManager
    from src.camera import Camera
    from src.game_state import MotherShip
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
mothership: MotherShip
arcangel_manager: ArcAngelManager

# Flags
game_over: bool
won: bool
pausing: bool
