import pygame

from src import shared
from src.states import StateManager


class Core:
    def __init__(self) -> None:
        self.win_init()
        self.state_manager = StateManager()

    def win_init(self):
        pygame.init()
        shared.screen = pygame.display.set_mode((1100, 650))
        shared.srect = shared.screen.get_rect()
        shared.clock = pygame.Clock()

    def get_events(self):
        shared.events = pygame.event.get()
        shared.dt = shared.clock.tick(60) / 1000
        shared.dt = max(shared.dt, 0.1)
        shared.keys = pygame.key.get_pressed()
        shared.kp = pygame.key.get_just_pressed()
        shared.kr = pygame.key.get_just_released()
        shared.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        shared.mouse_press = pygame.mouse.get_pressed()

    def check_for_exit(self):
        for event in shared.events:
            if event.type == pygame.QUIT:
                raise SystemExit

    def update(self):
        self.get_events()
        self.check_for_exit()
        self.state_manager.update()

    def draw(self):
        shared.screen.fill("black")
        self.state_manager.draw()
        pygame.display.flip()

    def run(self):
        while True:
            self.update()
            self.draw()
