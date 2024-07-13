import textwrap

import pygame

from src import shared, utils
from src.enums import State


class IntroState:
    def __init__(self) -> None:
        self.next_state = None
        self.renders = []

        font = utils.load_font("assets/fonts/yamaka.otf", 20)
        text0 = font.render("Press TAB to skip", True, "yellow")
        rect0 = text0.get_rect(topleft=(20, 20))
        self.renders.append((text0, rect0))

        text = font.render(
            """
            Your goal is very simple
            You have travelled across the universe to complete an older
            mission, however, in process of doing that your ship has been badly
            damaged. Due to this you must repair it in order to get back to Earth - To Get Back Home!

            Luckily for you, there is an enemy base which is currently weakened from an attack
            that should be easy to rob from. It has all the items you need in order to fix the ship!

            The items - A <Spring Balancer>, <Power Surge>, <Reflux Manager> and the <Left Wing>
            We have sent over information about the location of these items in the form of a circle,
            however this is an approximation. You must find the items on your own and 
            bring them to the MotherShip!

            The location has been marked by a red circular boundary, be careful not to cross it!
            Be wary about the ArcAngels protecting these items, they are formiddable and must be 
            killed
            """,
            True,
            "white",
        )
        text = text.subsurface(text.get_bounding_rect()).copy()
        rect = text.get_rect(topleft=(20, rect0.height + 70))

        self.renders.append((text, rect))

        text2 = font.render(
            """
            Controls:

            WASD - Move around, diagonal movement is possible
            SPACE - Shoot
            SHIFT - Boost
            F - Attach an item to your mini ship
            R - Attach an item to the mothership
            """,
            True,
            "green",
        )
        text2 = text2.subsurface(text2.get_bounding_rect()).copy()
        rect2 = text2.get_rect(topleft=(20, rect0.height + 20 + rect.height + 100))

        self.renders.append((text2, rect2))

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
        if shared.kp[pygame.K_TAB]:
            self.blit_loading_screen()
            self.next_state = State.GAME
            return

    def draw(self):
        for text, rect in self.renders:
            shared.screen.blit(text, rect)
