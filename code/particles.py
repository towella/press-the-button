import pygame, random
from helper_functions import circle_surf


class Particle(pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        super().__init__()
        self.screen = screen
        # location, velocity, timer
        self.pos =[random.randint(0, screen.get_width()), random.randint(0, 70)]
        self.vel = [random.randint(0, 18) / 10 - 1, random.randint(0, 18) / 10 - 1]
        self.timer = random.randint(1, 10)
        self.size = random.randint(1, 3)
        while self.size > self.timer:
            self.timer = random.randint(1, 10)
        self.colour = colour

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[1] + self.size >= 70:
            self.kill()
        self.timer -= 0.1
        self.size -= 0.1
        if self.size < 1:
            self.size = 1
        surf = circle_surf(int(self.size), self.colour)
        surf_rect = surf.get_rect()
        surf_rect.centerx = int(self.pos[0])
        surf_rect.centery = int(self.pos[1])
        self.screen.blit(surf, surf_rect.topleft, special_flags=pygame.BLEND_RGB_ADD)
        #pygame.draw.circle(self.screen, self.colour, (int(self.pos[0]), int(self.pos[1])), int(self.timer))
        if self.timer <= 0:
            self.kill()
