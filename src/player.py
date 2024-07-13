import itertools
import math

import pygame

from src import shared, utils
from src.bars import BoostBar, HealthBar
from src.info_text import DamageTextManager, render_help_text
from src.sparks import MetalExplosion


class Bullet:
    COLOR = (200, 200, 170)
    WIDTH = 20.0
    HEIGHT = 4.0
    DISTANCE = 1000.0
    IMG = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    IMG.fill(COLOR)

    BLOOM = utils.oval_surf(WIDTH * 1.5, HEIGHT * 2, (100, 100, 100))

    def __init__(self) -> None:
        self.original_pos = pygame.Vector2(shared.player.rect.center)
        self.pos = self.original_pos.copy()
        self.rect = Bullet.IMG.get_rect(center=self.pos)
        self.degrees = shared.player.angle
        self.radians = math.radians(shared.player.angle)
        self.velocity = 500.0
        self.alive = True

    def update(self):
        self.pos.x += math.cos(self.radians) * self.velocity * shared.dt
        self.pos.y += math.sin(-self.radians) * self.velocity * shared.dt
        self.rect.center = self.pos

        if self.pos.distance_to(self.original_pos) > Bullet.DISTANCE:
            self.alive = False

    def draw(self):
        tmp = pygame.transform.rotate(Bullet.IMG, self.degrees)
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
    """The gun that shoots from the tip of the player's ship"""

    DAMAGE = 10

    def __init__(self) -> None:
        self.bullets: list[Bullet] = []
        self.bullet_cd = utils.Time(0.1)

    def update(self):
        if shared.keys[pygame.K_SPACE] and self.bullet_cd.tick():
            self.bullets.append(Bullet())

        for bullet in self.bullets[:]:
            bullet.update()

            if not bullet.alive:
                self.bullets.remove(bullet)

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()


class Player:
    MAX_VELOCITY = 75.0
    ROTATION_SPEED = 120.0

    def __init__(self) -> None:
        self.original_image = utils.load_image("assets/images/player.png", True)
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
        self.n_attached = 0
        self.alpha = 255

        self.velocity = 0.0
        self.accel = 5.0
        self.decel = 10.0
        self.angle = 0.0
        self.last_target_angle = 0.0
        self.spawning_sequence = True
        self.blink_timer = utils.Time(0.5)
        self.spawning_images = itertools.cycle(
            (pygame.Surface(self.rect.size, pygame.SRCALPHA), self.original_image)
        )
        self.boost = 1
        self.boost_animation = utils.Animation(
            [
                utils.load_image(f"assets/images/boost{n}.png", True, True)
                for n in range(1, 4)
            ],
            2.0,
        )
        self.alive = True
        self.metal_explosion = MetalExplosion()

        self.headgun = HeadGun()
        self.health_bar = HealthBar()
        self.boost_bar = BoostBar()

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

    def handle_arcangels(self):
        for bullet in self.headgun.bullets:
            for arcangel in shared.arcangel_manager.arcangels:
                if arcangel.idling:
                    continue
                if not bullet.alive:
                    continue
                if arcangel.rect.colliderect(bullet.rect):
                    arcangel.take_damage(HeadGun.DAMAGE)

                    shared.arcangel_manager.hit_animation.spawn(
                        bullet.rect.center, math.radians(self.angle)
                    )
                    bullet.alive = False

    def update(self):
        if shared.won:
            self.pos.move_towards_ip(
                shared.mothership.rect.center, (Player.MAX_VELOCITY / 2) * shared.dt
            )
            if self.pos == shared.mothership.rect.center:
                shared.mothership.take_off = True
            self.rect.topleft = self.pos
            if self.alpha > 100:
                self.alpha -= 20 * shared.dt
            else:
                self.alpha = 100
            self.original_image.set_alpha(self.alpha)
            shared.camera.attach_to(self.rect.center)
            return
        if self.spawning_sequence:
            self.perform_spawning_sequence()
            return
        dx, dy = 0, 0
        moving = False
        self.boost = 1
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

        if shared.keys[pygame.K_LSHIFT] and self.boost_bar.amount > 0:
            self.boost = 2

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

        gradient = 1.5 / (self.n_attached + 1)
        dx = (
            gradient
            * self.velocity
            * self.boost
            * math.cos(math.radians(self.angle))
            * shared.dt
        )
        dy = (
            gradient
            * self.velocity
            * self.boost
            * math.sin(math.radians(-self.angle))
            * shared.dt
        )
        self.pos.x += dx
        self.pos.y += dy
        self.last_target_angle = target_angle
        shared.camera.attach_to(self.rect.center)
        self.headgun.update()
        self.handle_arcangels()

        self.health_bar.update()
        self.boost_bar.update()
        if self.boost > 1:
            self.boost_bar.amount -= 10 * shared.dt
            self.boost_animation.update(shared.dt)

    def draw(self):
        if shared.game_over:
            self.metal_explosion.update()
            self.metal_explosion.draw()
            return

        if not self.spawning_sequence:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.original_rect.center + self.pos)
        render_help_text(
            "Player's Ship",
            "The ship you need to control to get the collectables",
            self.rect,
            self.image,
        )
        self.headgun.draw()
        shared.screen.blit(self.image, shared.camera.transform(self.rect))
        self.health_bar.draw()
        self.boost_bar.draw()

        if self.boost > 1:
            img = self.boost_animation.image.copy()
            img = pygame.transform.rotate(img, self.angle)
            rect = img.get_rect()
            rect.center = self.rect.center
            shared.screen.blit(img, shared.camera.transform(rect))
