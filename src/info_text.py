import random
import typing as t

import pygame

from src import shared, utils

pygame.font.init()
help_text_font = utils.load_font("assets/fonts/yamaka.otf", 15)


def render_help_text(
    name: str,
    desc: str,
    rect: pygame.Rect,
    surface: pygame.Surface,
    angle: float = 0.0,
    transform: bool = True,
    render_offest: tuple[int, int] | None = None,
) -> None:
    """Render some help text for the entity"""

    trans_rect = rect.copy()
    if transform:
        trans_rect = rect.move(*-shared.camera.offset)
    if trans_rect.collidepoint(shared.mouse_pos):
        surf_highlight = surface.copy()
        mask = pygame.mask.from_surface(surf_highlight)
        surf_highlight = mask.to_surface(setcolor="yellow")
        surf_highlight.set_colorkey("black")
        surf_highlight = pygame.transform.scale_by(surf_highlight, 1.1)
        if angle:
            surf_highlight = pygame.transform.rotate(surf_highlight, angle)

        hrect = surf_highlight.get_rect(center=trans_rect.center)
        shared.screen.blit(surf_highlight, hrect)

        padding = 2
        txt_surf = help_text_font.render(name, True, "purple")
        desc_surf = help_text_font.render(desc, True, "white", wraplength=200)
        bg_surf = pygame.Surface(
            (
                desc_surf.get_width() + padding,
                desc_surf.get_height() + txt_surf.get_height() + padding,
            )
        )

        bg_surf.blit(txt_surf, (0, 0))
        bg_surf.blit(desc_surf, (0, txt_surf.get_height()))

        if render_offest is not None:
            offset = render_offest
        else:
            offset = trans_rect.move(rect.width, 0)
        shared.screen.blit(bg_surf, offset)


class DamageText:
    ALPHA_REDUCTION = 70.5
    SIZE_REDUCTION = 0.1

    def __init__(self, damage: int, pos: tuple[int, int]) -> None:
        self.damage = damage
        self.font = utils.load_font("assets/fonts/yamaka.otf", 20)
        self.original_surf = self.font.render(f"-{damage}", True, "red")
        self.surf = self.original_surf.copy()
        self.pos = pygame.Vector2(pos)
        self.rect = self.surf.get_rect(topleft=self.pos)
        self.size_factor = 1.0
        self.alpha = 255
        self.alive = True

        self.dx = random.uniform(10.0, 20.0) * random.choice((-1, 1))
        self.dy = -random.uniform(40.0, 80.0)

    def update(self):
        self.dy += 50.0 * shared.dt
        self.alpha -= DamageText.ALPHA_REDUCTION * shared.dt
        self.size_factor -= DamageText.SIZE_REDUCTION * shared.dt
        self.pos.x += self.dx * shared.dt
        self.pos.y += self.dy * shared.dt

        if self.alpha <= 10:
            self.alive = False

        self.surf = pygame.transform.scale_by(self.original_surf, self.size_factor)
        self.surf.set_alpha(self.alpha)
        self.rect = self.surf.get_rect(topleft=self.pos)

    def draw(self):
        shared.screen.blit(self.surf, shared.camera.transform(self.rect))


class DamageTextManager:
    def __init__(self) -> None:
        self.texts: list[DamageText] = []

    def spawn(self, damage: int, pos: tuple[int, int]):
        self.texts.append(DamageText(damage, pos))

    def update(self):
        for text in self.texts[:]:
            text.update()

            if not text.alive:
                self.texts.remove(text)

    def draw(self):
        for text in self.texts:
            text.draw()
