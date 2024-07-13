import pygame

from src import shared, utils
from src.arcangel import ArcAngelManager
from src.background import Background
from src.camera import Camera
from src.collectables import CollectableManager
from src.mothership import MotherShip


class GameState:
    def __init__(self) -> None:
        self.next_state = None
        shared.camera = Camera()
        shared.mothership = MotherShip()
        self.background = Background()
        shared.arcangel_manager = ArcAngelManager()
        self.collectable_manager = CollectableManager()
        self.pausing = False

        font = utils.load_font("assets/fonts/yamaka.otf", 60)
        self.paused_image = pygame.Surface(shared.srect.size, pygame.SRCALPHA)
        self.paused_image.fill((50, 50, 50, 100))
        titlesurf = font.render("PAUSED", True, "white")
        self.paused_image.blit(
            titlesurf,
            titlesurf.get_rect(center=shared.srect.center - pygame.Vector2(0, 100)),
        )

        font = utils.load_font("assets/fonts/yamaka.otf", 32)
        help_surf = font.render("Press ESC again to unpause", True, "white")
        self.paused_image.blit(
            help_surf,
            help_surf.get_rect(center=shared.srect.center + pygame.Vector2(0, 100)),
        )

    def update(self):
        if shared.kp[pygame.K_ESCAPE]:
            self.pausing = not self.pausing

        if self.pausing:
            return

        self.background.update()
        shared.mothership.update()
        self.collectable_manager.update()
        if shared.mothership.spawned_player:
            shared.player.update()
            shared.arcangel_manager.update()

    def draw(self):
        self.background.draw()
        shared.mothership.draw()
        self.collectable_manager.draw()
        if shared.mothership.spawned_player:
            shared.player.draw()
            shared.arcangel_manager.draw()

        if self.pausing:
            shared.screen.blit(self.paused_image, (0, 0))
