import pygame
from helper_functions import resource_path
from circle import Circle


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, colour, screen, circles=pygame.sprite.Group()):
        super().__init__()
        self.screen = screen
        self.pressed = False
        self.colour = colour
        self.pos = pos

        # get animation/images
        self.up = []
        self.down = []
        if colour == 'red':
            self.up.append(pygame.image.load(resource_path('../assets/images/red_button_up.png')).convert_alpha())
            self.down.append(pygame.image.load(resource_path('../assets/images/red_button_down.png')).convert_alpha())
        else:
            self.up.append(pygame.image.load(resource_path('../assets/images/gold_button_up.png')).convert_alpha())
            self.down.append(pygame.image.load(resource_path('../assets/images/gold_button_down.png')).convert_alpha())
        self.image = self.up[0]
        self.hitbox = pygame.Rect(12, 12 + 70, 26, 26)

        # circles
        self.create_circles = False
        self.circles = pygame.sprite.Group()
        #for circle in circles:
        self.circles.add(circles)
        self.double_circles = False
        self.circle_colour = (220, 0, 52)

    def set_circle_colour(self, colour):
        self.circle_colour = colour

    def set_create_circles(self):
        self.create_circles = True

    def set_double_circles(self):
        self.double_circles = True

    # also creates circles
    def set_pressed(self, pressed=False):
        if not self.pressed and pressed and self.create_circles:
            self.circles.add(Circle(14, self.circle_colour, 5, self.screen, self.hitbox.center, self.double_circles))
        self.pressed = pressed

    def check_pressed(self, mpos):
        if self.hitbox.collidepoint(mpos):
            self.set_pressed(True)
            return True
        return False

    def get_circles(self):
        return self.circles

    def update(self):
        # update and draw circles
        self.circles.update()

        # draw button
        if self.pressed:
            self.image = self.down[0]
            self.screen.blit(self.image, (5, 7 + 70))
        else:
            self.image = self.up[0]
            self.screen.blit(self.image, self.pos)