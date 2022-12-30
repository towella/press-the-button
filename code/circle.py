import pygame


class Circle(pygame.sprite.Sprite):
    def __init__(self, radius, colour, thickness, screen, pos, double_circle):
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.radius = radius
        self.colour = colour
        self.thickness = thickness
        self.double_circle = double_circle

    def update(self):

        # double circles
        pygame.draw.circle(self.screen, self.colour, self.pos, self.radius, int(self.thickness))
        self.thickness -= 0.2
        if self.double_circle:
            pygame.draw.circle(self.screen, 'white', self.pos, self.radius - 2, 1)
            pygame.draw.circle(self.screen, 'white', self.pos, self.radius, 1)
            if self.thickness <= 2:
                self.thickness = 2
        else:
            if self.thickness <= 1:
                self.thickness = 1

        self.radius += 1
        if self.radius > 60:
            self.kill()
