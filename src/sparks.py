import math
import random

import pygame

from src import shared

RIGHT_ANGLE = math.pi / 2
COLOR = (200, 200, 170)


def entities_updater(entities: list) -> None:
    for entity in entities[:]:
        entity.update()
        if not entity.alive:
            entities.remove(entity)


def entities_renderer(entities: list) -> None:
    for entity in entities:
        entity.draw()


class Particle:
    def __init__(
        self,
        pos: tuple[int, int],
        seconds: float,
        radius: float,
        radians: float,
        size: int,
        color=COLOR,
    ) -> None:
        self.pos = pygame.Vector2(pos)
        self.seconds = seconds
        self.radius = radius
        self.radians = radians
        self.size = size
        self.color = color

        # Kinematic variables
        self.target_pos = self.pos + pygame.Vector2(
            math.cos(self.radians) * self.radius, math.sin(self.radians) * self.radius
        )
        self.acc_dt = 0.0  # Accumalated delta time
        self.s1 = self.s2 = 0.0  # Distance travelled
        self.distance = 0.0
        self.speed = 0.0

        self.initial_velocity = (2 * self.radius) / self.seconds
        self.acceleration = -self.initial_velocity / self.seconds

        # Rendering attributes
        self.delta = pygame.Vector2()
        self.create_points()
        self.alive = True

    @classmethod
    def random(cls, pos: pygame.Vector2):
        radians = random.uniform(0, 2 * math.pi)

        return cls(
            pos=pos,
            seconds=random.uniform(1.0, 2.0),
            radius=random.uniform(80, 140),
            radians=radians,
            size=1.5,
        )

    def create_points(self):
        points = [
            self.pos + self.get_delta(self.radians),
            self.pos + self.get_delta(self.radians + RIGHT_ANGLE) * 0.3,
            self.pos - self.get_delta(self.radians) * 3.5,
            pygame.Vector2(
                self.pos.x + self.get_delta(self.radians - RIGHT_ANGLE).x * 0.3,
                self.pos.y - self.get_delta(self.radians + RIGHT_ANGLE).y * 0.3,
            ),
        ]

        self.points = [shared.camera.transform(point) for point in points]

    def get_delta(self, radians: float):
        return pygame.Vector2(
            math.cos(radians) * self.speed * self.size,
            math.sin(radians) * self.speed * self.size,
        )

    def on_death(self):
        if self.speed > 0:
            return
        self.alive = False

    def update(self):
        """(kinematics)
        s = ut + (1/2)a(t^2)
        """

        self.acc_dt += shared.dt
        self.s1 = (self.initial_velocity * self.acc_dt) + (
            0.5 * self.acceleration * (self.acc_dt**2)
        )
        self.speed = self.s1 - self.s2

        # Updating attributes
        self.pos.move_towards_ip(self.target_pos, self.speed)
        self.create_points()
        self.on_death()

        self.s2 = self.s1

    def draw(self):
        pygame.draw.polygon(shared.screen, self.color, self.points)


class Spark:
    def __init__(self, center_pos: tuple[int, int], density: int) -> None:
        self.density = density
        self.particles: Particle = [Particle.random(center_pos) for _ in range(density)]
        self.radius = max(particle.radius for particle in self.particles)
        self.center = pygame.mouse.get_pos()
        self.alive = True

    def update(self):
        entities_updater(self.particles)
        self.alive = bool(self.particles)

    def draw(self):
        entities_renderer(self.particles)


class ShockWave:
    def __init__(
        self,
        pos: tuple[int, int],
        duration: float,
        max_radius: float,
        starting_width: float,
        color=COLOR,
    ) -> None:
        self.pos = pygame.Vector2(pos)
        self.duration = duration
        self.max_radius = max_radius
        self.max_width = starting_width

        self.radius = 0
        self.width = self.max_width
        self.color = color
        self.alive = True
        self.acc_dt = 0.0

    def update(self):
        self.alive = self.width > 0
        self.acc_dt += shared.dt

        time_ratio = self.acc_dt / self.duration
        self.radius = self.max_radius * time_ratio
        self.width = self.max_width * (1 - time_ratio)

    def draw(self):
        if int(self.width) <= 0:
            return
        pygame.draw.circle(
            shared.screen,
            self.color,
            shared.camera.transform(self.pos),
            self.radius,
            int(self.width),
        )


class MetalExplosion:
    def __init__(self) -> None:
        self.sparks: list[Spark] = []
        self.shockwaves: list[ShockWave] = []

    def spawn(self, pos: pygame.Vector2):
        self.sparks.append(Spark(pos, density=15))
        self.shockwaves.append(
            ShockWave(
                pos=pos,
                duration=2.0,
                max_radius=100,
                starting_width=20,
            )
        )

    def check_spawn(self):
        for event in shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.spawn(pygame.mouse.get_pos())

    def update(self):
        # self.check_spawn()
        entities_updater(self.shockwaves)
        entities_updater(self.sparks)

    def draw(self):
        entities_renderer(self.shockwaves)
        entities_renderer(self.sparks)
