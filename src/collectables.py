import pygame

from src import shared, utils
from src.info_text import render_help_text


class Collectable:
    def __init__(self, image_name, name: str, desc: str, pos) -> None:
        self.image = utils.load_image(f"assets/images/{image_name}", True, True)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.name = name
        self.desc = desc

    def update(self):
        pass

    def draw(self):
        render_help_text(self.name, self.desc, self.rect, self.image)
        shared.screen.blit(self.image, shared.camera.transform(self.rect))


class CollectableManager:
    def __init__(self) -> None:
        self.collectables = [
            Collectable(
                "reflux-manager.png",
                "Reflux Manager",
                "Monitors and regulates the flow of waste gases and liquids, ensuring efficient processing and a safe environment for the crew",
                (0, 0),
            )
        ]

    def update(self):
        for collectable in self.collectables:
            collectable.update()

    def draw(self):
        for collectable in self.collectables:
            collectable.draw()
