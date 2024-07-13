import pygame

from src import shared, utils
from src.info_text import render_help_text


class Collectable:
    N = 0

    def __init__(self, image_name, name: str, desc: str, pos) -> None:
        self.image = utils.load_image(f"assets/images/{image_name}", True, True)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.name = name
        self.desc = desc
        self.dist = 0.0
        self.font = utils.load_font("assets/fonts/yamaka.otf", 15)

        self.catch_surf = self.font.render(
            "Press [F] to attach", True, "white", "black"
        )
        self.catch_rect = self.catch_surf.get_rect(midbottom=self.rect.midtop)

        self.attach_surf = self.font.render(
            "Press [R] to attach to mothership", True, "green", "black"
        )
        self.attach_rect = self.catch_surf.get_rect(midbottom=self.rect.midtop)

        self.attached = False
        self.collected = False
        self.n = Collectable.N
        Collectable.N += 1

        width = 40
        x = (self.n * (width + 10)) + 20
        self.utility_rect = pygame.Rect(x, 100 + width, width, width)
        self.utility_image = pygame.transform.scale(self.image, (width, width))
        self.utility_bg = pygame.Surface((width, width), pygame.SRCALPHA)
        self.utility_bg.fill((0, 0, 0, 200))
        pygame.draw.rect(self.utility_bg, "grey", (0, 0, width, width), 2)

        big_font = utils.load_font("assets/fonts/yamaka.otf", width)
        self.ques_surf = big_font.render("?", True, "red")
        self.x_surf = big_font.render("X", True, "green")

    def update(self):
        if not shared.mothership.spawned_player:
            return
        self.dist = self.pos.distance_to(shared.player.rect.center)
        if self.dist < 300 and shared.kp[pygame.K_f]:
            self.attached = not self.attached

        if not self.collected and self.attached and self.dist > 200:
            shared.player.n_attached += 1
            self.pos.move_towards_ip(
                shared.player.rect.center,
                shared.player.velocity * shared.player.boost * shared.dt,
            )

        self.rect.center = self.pos
        self.catch_rect.midbottom = self.rect.midtop
        self.attach_rect.midbottom = self.rect.midtop

        if (
            self.attached
            and self.pos.distance_to(shared.mothership.rect.center) < 200
            and shared.kp[pygame.K_r]
        ):
            self.collected = True

    def draw(self):
        shared.screen.blit(self.utility_bg, self.utility_rect)
        render_help_text(
            self.name,
            self.desc,
            self.utility_rect,
            self.utility_image,
            transform=False,
            render_offest=self.utility_rect.move(0, self.utility_rect.height + 4),
        )
        shared.screen.blit(self.utility_image, self.utility_rect)

        if self.collected:
            shared.screen.blit(self.x_surf, self.utility_rect)
        else:
            shared.screen.blit(self.ques_surf, self.utility_rect)

        if self.collected:
            return
        render_help_text(self.name, self.desc, self.rect, self.image)

        if self.attached:
            pygame.draw.line(
                shared.screen,
                "yellow",
                shared.camera.transform(self.pos),
                shared.camera.transform(shared.player.rect.center),
                3,
            )

        shared.screen.blit(self.image, shared.camera.transform(self.rect))

        if self.dist < 300 and not self.attached:
            shared.screen.blit(
                self.catch_surf, shared.camera.transform(self.catch_rect)
            )

        if self.attached and self.pos.distance_to(shared.mothership.rect.center) < 200:
            shared.screen.blit(
                self.attach_surf, shared.camera.transform(self.attach_rect)
            )


class CollectableManager:
    def __init__(self) -> None:
        self.collectables = [
            Collectable(
                "reflux-manager.png",
                "Reflux Manager",
                "Monitors and regulates the flow of waste gases and liquids, ensuring efficient processing and a safe environment for the crew",
                (1200, -1200),
            ),
            Collectable(
                "spring-balancer.png",
                "Spring Balancer",
                "Maintains tension in mechanical systems, ensuring stable and smooth operation of moving parts",
                (-500, -1200),
            ),
            Collectable(
                "left-wing.png",
                "Left Wing",
                "Provides stability and directional control during flight maneuvers",
                (-500, 1200),
            ),
            Collectable(
                "power-surge.png",
                "Power Surge",
                "Provides a temporary boost of energy to critical systems during high-demand situations",
                (1500, 1400),
            ),
        ]

    def update(self):
        if shared.mothership.spawned_player:
            shared.player.n_attached = 0
        for collectable in self.collectables:
            collectable.update()

    def draw(self):
        for collectable in self.collectables:
            collectable.draw()
