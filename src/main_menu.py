import random

import pygame

from src import shared, utils
from src.enums import State


class Camera:
    offset = pygame.Vector2()


class Title:
    def __init__(self) -> None:
        self.image = utils.load_image("assets/images/title.png", True, True)
        self.rect = self.image.get_rect(
            midtop=shared.srect.midtop + pygame.Vector2(0, 100)
        )

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(self.image, self.rect)


class PlayButton:
    BASE_COLOR = pygame.Color(90, 101, 124)
    HOVER_COLOR = pygame.Color(108, 139, 136)

    def __init__(self) -> None:
        self.image = pygame.Surface((250, 70), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image,
            "white",
            self.image.get_rect(),
            border_top_left_radius=30,
            border_bottom_right_radius=30,
        )
        self.rect = self.image.get_rect(
            center=shared.srect.center + pygame.Vector2(0, 100)
        )
        self.clicked = False
        self.hovering = False
        self.color = PlayButton.BASE_COLOR
        self.text = utils.load_font("assets/fonts/yamaka.otf", 32).render(
            "PLAY", True, (189, 176, 159)
        )
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self):
        self.hovering = self.rect.collidepoint(shared.mouse_pos)
        self.clicked = False
        if self.hovering and shared.mouse_press[0]:
            self.clicked = True

        if self.hovering:
            self.color = utils.lerp_color(
                pygame.Color(self.color)[:3], PlayButton.HOVER_COLOR[:3]
            )
        else:
            self.color = utils.lerp_color(
                pygame.Color(self.color)[:3], PlayButton.BASE_COLOR[:3]
            )

    def draw(self):
        if self.clicked:
            move = (5, 5)
        else:
            move = (0, 0)
        pygame.draw.rect(
            shared.screen,
            "black",
            self.rect.move(5, 5),
            border_top_left_radius=30,
            border_bottom_right_radius=30,
        )
        pygame.draw.rect(
            shared.screen,
            self.color,
            self.rect.move(*move),
            border_top_left_radius=30,
            border_bottom_right_radius=30,
        )

        shared.screen.blit(self.text, self.text_rect.move(*move))


class Star:
    RADIUS = 10.0
    SPEED = 10.0

    def __init__(self, parallax_scale: int) -> None:
        self.radius = Star.RADIUS * parallax_scale
        self.parallax_scale = parallax_scale
        self.image = utils.load_image(
            "assets/images/star.png", True, False, parallax_scale
        ).copy()
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(
            random.randrange(0, shared.srect.width),
            random.randrange(0, shared.srect.height // 2),
        )
        self.rect.center = self.pos
        self.direction = 1

    def update(self):
        self.pos.x += Star.SPEED * self.parallax_scale * self.direction * shared.dt
        self.rect.center = self.pos

        if self.direction == -1 and self.pos.x + Star.RADIUS < 0:
            self.pos.x = shared.srect.width + (Star.RADIUS * 2)

        if self.direction == 1 and self.pos.x - Star.RADIUS > shared.srect.width:
            self.pos.x = -Star.RADIUS * 2

    def draw(self):
        img = self.image
        shared.screen.blit(img, self.pos)


class MovingStars:
    def __init__(self) -> None:
        self.layers = [
            [Star(0.3) for _ in range(50)],
            [Star(0.7) for _ in range(50)],
            [Star(1.0) for _ in range(50)],
        ]

    def update(self):
        for layer in self.layers:
            for star in layer:
                star.update()

    def draw(self):
        for layer in self.layers:
            for star in layer:
                star.draw()


class MainMenu:
    def __init__(self) -> None:
        self.next_state = None
        self.bg = utils.load_image("assets/images/bg.png", False)
        self.title = Title()
        self.play_button = PlayButton()
        self.moving_stars = MovingStars()

    def update(self):
        if shared.kp[pygame.K_TAB]:
            self.next_state = State.GAME

        self.title.update()
        self.play_button.update()
        self.moving_stars.update()

    def draw(self):
        shared.screen.blit(self.bg, (0, 0))
        self.moving_stars.draw()
        self.title.draw()
        self.play_button.draw()
