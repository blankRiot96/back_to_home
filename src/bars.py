import pygame

from src import shared, utils


class Bar:
    def __init__(
        self, text: str, bg_color, max_amount: int, pos: tuple[int, int]
    ) -> None:
        self.text = text
        self.bg_color = bg_color
        self.amount = 0
        self.max_amount = max_amount

        self.font = utils.load_font("assets/fonts/yamaka.otf", 20)
        self.bar_frame = utils.load_image("assets/images/bar.png", True, True, 0.7)
        self.bar_bg = utils.load_image(
            "assets/images/bar-bg.png", True, True, 0.7
        ).copy()
        self.pos = pygame.Vector2(pos)
        self.rect = self.bar_frame.get_rect(topleft=self.pos)

        self.text_surf = self.font.render(self.text, True, "white")
        self.text_rect = self.text_surf.get_rect(topleft=self.pos + (30, -10))
        self.bg = pygame.Surface((0, 0), pygame.SRCALPHA)

    def update(self):
        scale = self.amount / self.max_amount

        sub_rect = pygame.Rect(0, 0, self.rect.width * scale, self.rect.height)
        self.bg = self.bar_bg.subsurface(sub_rect).copy()
        self.bg.fill(self.bg_color, special_flags=pygame.BLEND_RGBA_MIN)

    def draw(self):
        shared.screen.blit(self.bg, self.rect)
        shared.screen.blit(self.bar_frame, self.rect)
        shared.screen.blit(self.text_surf, self.text_rect)


class HealthBar(Bar):
    def __init__(self) -> None:
        super().__init__(
            text="HEALTH",
            bg_color="green",
            max_amount=500,
            pos=(20, 20),
        )
        self.amount = 500

    def update(self):
        super().update()

        scale = 1 - self.amount / self.max_amount
        self.bg_color = pygame.Color("green").lerp("red", scale)


class BoostBar(Bar):
    def __init__(self) -> None:
        super().__init__(
            text="BOOST",
            bg_color="blue",
            max_amount=200,
            pos=(20, 80),
        )

    def update(self):
        super().update()

        self.bg_color = "blue"
        if shared.player.boost > 1:
            self.bg_color = "orange"
