from __future__ import annotations

import itertools
import math
import random

import pygame

from src import shared, utils
from src.info_text import DamageTextManager, render_help_text
from src.sparks import MetalExplosion, MetalHit


class Bullet:
    COLOR = "yellow"
    WIDTH = 20.0
    HEIGHT = 4.0
    DISTANCE = 900.0
    IMG = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    IMG.fill(COLOR)

    BLOOM = utils.oval_surf(WIDTH * 1.5, HEIGHT * 2, (100, 100, 100))

    def __init__(self, pos, angle) -> None:
        self.original_pos = pygame.Vector2(pos)
        self.pos = self.original_pos.copy()
        self.rect = Bullet.IMG.get_rect(center=self.pos)
        angle = int(angle)
        self.degrees = random.randint(angle - 15, angle + 15)
        self.radians = math.radians(self.degrees)
        self.velocity = 200.0
        self.alive = True
        self.dist = 0.0

    def update(self):
        self.pos.x += math.cos(self.radians) * self.velocity * shared.dt
        self.pos.y += math.sin(-self.radians) * self.velocity * shared.dt
        self.rect.center = self.pos

        self.dist = self.pos.distance_to(self.original_pos)
        if self.dist > Bullet.DISTANCE:
            self.alive = False

        if self.rect.colliderect(shared.player.rect):
            shared.player.metal_explosion.spawn(shared.player.pos)
            shared.player.health_bar.amount -= HeadGun.DAMAGE
            self.alive = False

    def draw(self):
        tmp = pygame.transform.rotate(Bullet.IMG, self.degrees)
        tmp.set_alpha((1 - self.dist / Bullet.DISTANCE) * 255)
        rect = tmp.get_rect(center=self.rect.center)
        shared.screen.blit(tmp, shared.camera.transform(rect))

        bloom = pygame.transform.rotate(Bullet.BLOOM, self.degrees)
        brect = bloom.get_rect(center=self.pos)
        shared.screen.blit(
            bloom,
            shared.camera.transform(brect),
            special_flags=pygame.BLEND_RGB_ADD,
        )


class HeadGun:
    """The gun that shoots from the tip of the arcangel's ship"""

    DAMAGE = 50

    def __init__(self, arcangel: ArcAngel) -> None:
        self.bullets: list[Bullet] = []
        self.bullet_cd = utils.Time(random.uniform(0.5, 1.5))
        self.arcangel = arcangel
        self.idling = True

    def update(self):
        within_shooting_range = self.arcangel.pos.distance_to(shared.player.pos) < 500
        if not within_shooting_range:
            self.bullet_cd.reset()
        if within_shooting_range and self.bullet_cd.tick():
            self.bullets.append(Bullet(self.arcangel.rect.center, self.arcangel.angle))
            self.bullet_cd.time_to_pass = 1.0

        for bullet in self.bullets[:]:
            bullet.update()

            if not bullet.alive:
                self.bullets.remove(bullet)

    def draw(self):
        if shared.pausing:
            self.bullet_cd.reset()
        for bullet in self.bullets:
            bullet.draw()


class ArcAngel:
    SPEED = 35.0
    HP = 50
    MAX_APPROACH_DISTANCE = 200
    IDLE_SPEED = 10.0

    def __init__(self, pos) -> None:
        self.image = utils.load_image("assets/images/arcangel.png", True, True, 0.5)
        self.orect = self.image.get_rect()
        self.rect = self.orect.copy()
        self.pos = pygame.Vector2(pos)
        self.angle = 0.0
        self.alive = True
        self.hp = ArcAngel.HP
        self.taking_damage = False
        self.original_overlay_color = (255, 255, 255)
        self.overlay_color = self.original_overlay_color
        self.dmg_text_manager = DamageTextManager()
        self.headgun = HeadGun(self)
        self.rng_and_idle_init()

    def rng_and_idle_init(self):
        self.idling = True
        self.pos = pygame.Vector2(
            random.uniform(self.pos.x - 400, self.pos.x + 400),
            random.uniform(self.pos.y - 400, self.pos.y + 400),
        )
        self.target_pos = pygame.Vector2(
            random.uniform(self.pos.x - 400, self.pos.x + 400),
            random.uniform(self.pos.y - 400, self.pos.y + 400),
        )
        self.walking_points = itertools.cycle((self.pos.copy(), self.target_pos.copy()))
        self.rect.topleft = self.pos

    def take_damage(self, damage: int):
        self.taking_damage = True
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            return

        self.dmg_text_manager.spawn(damage, self.rect.midtop)

    def update(self):
        if self.idling:
            self.pos.move_towards_ip(self.target_pos, ArcAngel.IDLE_SPEED * shared.dt)
            if self.pos == self.target_pos:
                self.target_pos = next(self.walking_points)
            self.angle = -math.degrees(
                math.atan2(
                    self.target_pos.y - self.pos.y, self.target_pos.x - self.pos.x
                )
            )

            if self.pos.distance_to(shared.player.rect.center) < 400:
                self.idling = False
            self.rect.topleft = self.pos
            return

        if self.rect.colliderect(shared.player.rect):
            if shared.player.boost > 1:
                self.take_damage(100)
        if self.overlay_color != self.original_overlay_color:
            for _ in range(10):
                self.overlay_color = utils.lerp_color(
                    self.overlay_color, self.original_overlay_color
                )

        if self.pos.distance_to(shared.player.pos) > ArcAngel.MAX_APPROACH_DISTANCE:
            self.pos.move_towards_ip(shared.player.pos, ArcAngel.SPEED * shared.dt)
        self.rect.topleft = self.pos

        tx, ty = shared.player.pos
        x, y = self.pos
        self.angle = -math.degrees(math.atan2(ty - y, tx - x))
        self.dmg_text_manager.update()
        self.headgun.update()

    def draw(self):

        render_help_text(
            "arcangel",
            "Protects the collectable items",
            self.rect,
            self.image,
            self.angle,
        )
        img = pygame.transform.rotate(self.image, self.angle)
        if self.taking_damage:
            self.overlay_color = (255, 0, 0)
            self.taking_damage = False
        img.fill(self.overlay_color, special_flags=pygame.BLEND_RGBA_MIN)
        rect = img.get_rect(center=self.orect.center + self.pos)

        self.headgun.draw()
        shared.screen.blit(img, shared.camera.transform(rect))
        self.dmg_text_manager.draw()


class ArcAngelManager:
    def __init__(self) -> None:
        positions = [(1200, -1200), (-500, -1200), (-500, 1200), (1500, 1400)]
        self.arcangels: list[ArcAngel] = [
            ArcAngel(pos) for pos in positions for _ in range(5)
        ]
        self.explosion = MetalExplosion()
        self.hit_animation = MetalHit()

    def update(self):
        for arcangel in self.arcangels[:]:
            arcangel.update()
            if not arcangel.alive:
                if shared.player.boost == 1:
                    shared.player.boost_bar.amount += 40
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

        self.hit_animation.update()
        self.explosion.update()

    def draw(self):
        for arcangel in self.arcangels:
            arcangel.draw()
        self.hit_animation.draw()
        self.explosion.draw()
