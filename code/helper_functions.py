import sys, os, pygame


# allows paths to be used for both normal running in PyCharm and as an .exe
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        relative_path = relative_path[3:]  # slices path if using executable to absolute path. Otherwise use relative for PyCharm
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def load_font_img(path):
    path = resource_path(path)
    font_img = pygame.image.load(path).convert()
    font_img.set_colorkey((0, 255, 255))
    chars = []
    char_widths = []
    last_x = 0

    for x in range(font_img.get_width()):
        # get_at gets specific pixel data from an image based on coordinates
        if font_img.get_at((x, 0)) == (255, 0, 255):
            # clip takes rect to clip out of an image
            chars.append(clip(font_img, last_x, 0, x - last_x, font_img.get_height()))
            char_widths.append(x - last_x)
            last_x = x + 1

    return chars, char_widths


def circle_surf(radius, colour):
    surf = pygame.Surface((radius*2, radius*2))
    pygame.draw.circle(surf, colour, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf