import pygame

from src import shared, utils
from src.arcangel import ArcAngelManager
from src.background import Background
from src.camera import Camera
from src.collectables import CollectableManager
from src.enums import State
from src.mothership import MotherShip


class GameOverScreen:
    def __init__(self) -> None:
        self.surf = pygame.Surface(shared.srect.size, pygame.SRCALPHA)
        self.surf.fill("red")
        self.surf.set_alpha(0)
        self.alpha = 0
        self.font = utils.load_font("assets/fonts/yamaka.otf", 60)
        self.init_text_stuffs()

    def init_text_stuffs(self):
        self.over_text = self.font.render("Game Over", True, "white")
        self.over_rect = self.over_text.get_rect(
            center=shared.srect.midtop + pygame.Vector2(0, 100)
        )

        sub_font = utils.load_font("assets/fonts/yamaka.otf", 32)
        self.help_text = sub_font.render("Press TAB to Restart", True, "white")
        self.help_rect = self.help_text.get_rect(
            center=shared.srect.center + pygame.Vector2(0, 50)
        )

        menu_text = sub_font.render("Press ENTER to go to the Main Menu", True, "white")
        menu_rect = menu_text.get_rect(
            center=shared.srect.center + pygame.Vector2(0, 100)
        )

        self.renders: list[tuple[pygame.Surface, pygame.Rect]] = [
            (self.over_text, self.over_rect),
            (self.help_text, self.help_rect),
            (menu_text, menu_rect),
        ]

    def update(self):
        if self.alpha < 150:
            self.alpha += 20 * shared.dt
        else:
            self.alpha = 150

        self.surf.set_alpha(self.alpha)

    def draw(self):
        shared.screen.blit(self.surf, (0, 0))
        for text, rect in self.renders:
            shared.screen.blit(text, rect)


class GameState:
    def __init__(self) -> None:
        self.next_state = None
        shared.camera = Camera()
        shared.mothership = MotherShip()
        self.background = Background()
        shared.arcangel_manager = ArcAngelManager()
        self.collectable_manager = CollectableManager()
        shared.game_over = False
        shared.won = False
        shared.pausing = False

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

        self.game_over_screen = GameOverScreen()
        self.alpha = 0
        self.win_overlay = pygame.Surface(shared.srect.size, pygame.SRCALPHA)
        self.win_overlay.fill("black")
        self.win_overlay.set_alpha(self.alpha)

    def blit_loading_screen(self):
        shared.screen.fill("black")
        font = utils.load_font("assets/fonts/yamaka.otf", 60)
        text = font.render("Loading...", True, "green")
        text_rect = text.get_rect(center=shared.srect.center + pygame.Vector2(0, -100))

        img = utils.load_image(
            "assets/images/pygame_ce_powered.png", True, True, scale=0.2
        )
        img_rect = img.get_rect(center=shared.srect.center + pygame.Vector2(0, 50))

        shared.screen.blit(text, text_rect)
        shared.screen.blit(img, img_rect)
        pygame.display.flip()

    def update(self):
        if shared.mothership.take_off and hasattr(shared, "player"):
            del shared.player

        if shared.mothership.take_off:
            self.alpha += 20 * shared.dt
            if self.alpha >= 255:
                self.alpha = 255
                self.next_state = State.VICTORY
                return
            self.win_overlay.set_alpha(self.alpha)

        if shared.game_over:
            self.game_over_screen.update()
            if shared.kp[pygame.K_TAB]:
                shared.game_over = False
                self.next_state = State.GAME
                del shared.player
                self.blit_loading_screen()
            if shared.kp[pygame.K_RETURN]:
                shared.game_over = False
                del shared.player
                self.next_state = State.MAIN_MENU
            return

        if not shared.won and shared.kp[pygame.K_ESCAPE]:
            shared.pausing = not shared.pausing

        if shared.pausing:
            return

        if shared.kp[pygame.K_g]:
            shared.won = True
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

        if shared.pausing:
            shared.screen.blit(self.paused_image, (0, 0))

        if shared.game_over:
            self.game_over_screen.draw()
        shared.screen.blit(self.win_overlay, (0, 0))
