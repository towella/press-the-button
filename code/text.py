import pygame
from helper_functions import load_font_img

# SOURCE: Lynez Source Project by DaFluffyPotato


class Text():
    def __init__(self, path):
        self.chars, self.char_widths = load_font_img(path)
        self.char_order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.base_spacing = 1

    def width(self, text):
        text_width = 0
        for char in text:
            text_width += self.char_widths[self.char_order.index(char)] + self.base_spacing

        return text_width

    def render(self, text, screen, pos):
        x_offset = 0

        for char in text:
            screen.blit(self.chars[self.char_order.index(char)], (pos[0] + x_offset, pos[1]))
            x_offset += self.char_widths[self.char_order.index(char)] + self.base_spacing
