import pygame

from src import shared
from src.info_text import render_help_text
from src.player import Player


class MotherShip:
    SPEED = 100.0

    def __init__(self) -> None:
        self.original_image = pygame.image.load(
            "assets/images/mothership.png"
        ).convert_alpha()
        self.original_image = pygame.transform.scale_by(
            self.original_image.subsurface(
                self.original_image.get_bounding_rect()
            ).copy(),
            0.5,
        )

        self.out_image = pygame.image.load(
            "assets/images/mothership-split.png"
        ).convert_alpha()
        self.out_image = pygame.transform.scale_by(
            self.out_image.subsurface(self.out_image.get_bounding_rect()).copy(),
            0.5,
        )
        self.image = self.original_image.copy()
        self.pos = pygame.Vector2()
        self.rect = self.image.get_rect()
        self.speed = MotherShip.SPEED
        self.decel = 10.0
        self.spawned_player = False

    def spawn_player(self, skip=False):
        shared.player = Player()
        self.spawned_player = True
        self.image = self.out_image.copy()
        if skip:
            shared.player.pos.y = shared.srect.height // 2
        shared.player.pos.x = shared.srect.width // 2 - (shared.player.rect.width // 2)
        shared.player.pos.y += 60
        shared.player.blink_timer.reset()

    def update(self):
        if self.speed > 10.0:
            self.speed -= self.decel * shared.dt
        else:
            self.speed = 10.0

        if self.rect.midtop[0] < shared.srect.width // 2:
            self.pos.x += self.speed * shared.dt
            if shared.kp[pygame.K_TAB]:
                self.spawn_player(skip=True)
                self.pos.x = shared.srect.width // 2
        if self.pos.x > shared.srect.width // 2:
            self.spawn_player()
            self.pos.x = shared.srect.width // 2

        self.rect.midtop = self.pos

    def draw(self):
        render_help_text("Mothership", "The ship to be fixed", self.rect, self.image)
        shared.screen.blit(self.image, shared.camera.transform(self.rect))
