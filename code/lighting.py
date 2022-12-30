import pygame, random, math
from helper_functions import circle_surf


class Light(pygame.sprite.Sprite):
    def __init__(self, screen, pos, max_radius, min_radius, colour):
        super().__init__()
        self.waver_speed = 0.03
        self.screen = screen
        self.pos = pos
        self.max = max_radius
        self.min = min_radius
        self.colour = colour
        self.time_offset = random.randint(0, 60)

    def update(self, time):
        time += self.time_offset
        radius = self.max * math.sin(time * self.waver_speed)
        if radius < self.min:
            radius = self.min
        surf = circle_surf(radius, self.colour)
        surf_rect = pygame.Rect(0, 0, surf.get_width(), surf.get_height())
        surf_rect.centerx = self.pos[0]
        surf_rect.centery = self.pos[1]
        self.screen.blit(surf, (surf_rect.x, surf_rect.y), special_flags=pygame.BLEND_RGB_ADD)