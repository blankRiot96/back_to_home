import pygame

from src import shared, utils


class VictoryState:
    def __init__(self) -> None:
        self.next_state = None
        self.earth = utils.load_image("assets/images/earth.png", True, True)
        self.angle = 0.0
        self.size = 100
        self.growing = True

        self.font = utils.load_font("assets/fonts/yamaka.otf", 40)
        self.congrats_text = self.font.render(
            "Congratulations On Reaching Home!", True, "white"
        )
        self.congrats_rect = self.congrats_text.get_rect(
            midtop=shared.srect.midtop + pygame.Vector2(0, 100)
        )

        font = utils.load_font("assets/fonts/yamaka.otf", 30)
        text = font.render("Thanks so much for playing!", True, "grey")
        rect = text.get_rect(midbottom=shared.srect.midbottom + pygame.Vector2(0, -100))
        self.renders = [
            (self.congrats_text, self.congrats_rect),
            (text, rect),
        ]

        text = font.render("Send me a screenshot on discord :)", True, "grey")
        rect = text.get_rect(midbottom=shared.srect.midbottom + pygame.Vector2(0, -50))

        self.renders.append((text, rect))

    def update(self):
        if self.growing:
            self.size += 20 * shared.dt
            if self.size >= 500:
                self.growing = False
                self.size = 500
            self.angle += 10 * shared.dt

    def draw(self):
        img = pygame.transform.scale(self.earth, (self.size, self.size))
        img = pygame.transform.rotate(img, self.angle)
        shared.screen.blit(img, img.get_rect(center=shared.srect.center))

        if not self.growing:
            for text, rect in self.renders:
                shared.screen.blit(text, rect)
