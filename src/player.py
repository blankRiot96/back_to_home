import itertools
import math

import pygame

from src import shared
from src.utils import Time


class Player:
    MAX_VELOCITY = 75.0
    ROTATION_SPEED = 120.0

    def __init__(self) -> None:
        self.original_image = pygame.image.load(
            "assets/images/player.png"
        ).convert_alpha()
        self.original_image = pygame.transform.scale_by(
            self.original_image.subsurface(
                self.original_image.get_bounding_rect()
            ).copy(),
            0.5,
        )
        self.image = self.original_image.copy()
        self.pos = pygame.Vector2()
        self.original_rect = self.original_image.get_rect(topleft=self.pos)
        self.rect = self.original_rect.copy()

        self.velocity = 0.0
        self.accel = 5.0
        self.decel = 10.0
        self.angle = 0.0
        self.last_target_angle = 0.0
        self.spawning_sequence = True
        self.blink_timer = Time(0.5)
        self.spawning_images = itertools.cycle(
            (pygame.Surface(self.rect.size, pygame.SRCALPHA), self.original_image)
        )

    def perform_spawning_sequence(self):
        if shared.kp[pygame.K_TAB]:
            self.pos.y = shared.srect.height // 2
            self.spawning_sequence = False
            return

        if self.blink_timer.tick():
            self.image = next(self.spawning_images).copy()

        if self.pos.y < shared.srect.height // 2:
            self.pos.y += (Player.MAX_VELOCITY / 5) * shared.dt
        else:
            self.spawning_sequence = False

    def update(self):
        if self.spawning_sequence:
            self.perform_spawning_sequence()
            return
        dx, dy = 0, 0
        moving = False
        angles = []
        if shared.keys[pygame.K_w]:
            moving = True
            angles.append(90)
        elif shared.keys[pygame.K_s]:
            moving = True
            angles.append(-90 if shared.keys[pygame.K_d] else 270)
        if shared.keys[pygame.K_d]:
            moving = True
            angles.append(0)
        elif shared.keys[pygame.K_a]:
            moving = True
            angles.append(180)

        if angles:
            target_angle = sum(angles) / len(angles)
        else:
            target_angle = self.angle

        self.angle = target_angle
        if moving:
            if self.velocity < Player.MAX_VELOCITY:
                self.velocity += self.accel * shared.dt
            else:
                self.velocity = Player.MAX_VELOCITY
        else:
            if self.velocity > 0.0:
                self.velocity -= self.decel * shared.dt
            else:
                self.velocity = 0

        dx = self.velocity * math.cos(math.radians(self.angle)) * shared.dt
        dy = self.velocity * math.sin(math.radians(-self.angle)) * shared.dt
        self.pos.x += dx
        self.pos.y += dy
        self.last_target_angle = target_angle
        shared.camera.attach_to(self.rect.center)

    def draw(self):
        if not self.spawning_sequence:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.original_rect.center + self.pos)
        shared.screen.blit(self.image, shared.camera.transform(self.rect))
