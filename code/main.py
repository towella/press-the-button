import pygame, sys, math, time
import random
from helper_functions import resource_path, circle_surf
from button import Button
from text import Text
from lighting import Light
from particles import Particle


# -- General setup --
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
game_speed = 60

# window and screen Setup ----- The window is the real pygame window. The screen is the surface that everything is
# placed on and then resized to blit on the window. Allowing larger pixels (art pixel = game pixel)
scaling_factor = 10
screen_width = 50
screen_height = 70
# window is 500 by 700
window = pygame.display.set_mode((screen_width * scaling_factor, screen_height * scaling_factor), pygame.DOUBLEBUF, vsync=True)
screen_height = 140

# all pixel values in game logic should be based on the screen!!!! NO .display FUNCTIONS!!!!!
screen = pygame.Surface((screen_width, screen_height))  # the display surface, re-scaled and blit to the window
screen_rect = screen.get_rect()  # used for camera scroll boundaries

# game icon
pygame.display.set_icon(pygame.image.load(resource_path('../icon/app_icon.png')))

bg = pygame.image.load(resource_path('../assets/images/bg.png')).convert_alpha()
special_bg = pygame.image.load(resource_path('../assets/images/special_bg.png')).convert_alpha()

unmute_img = pygame.image.load(resource_path('../assets/images/unmute.png')).convert_alpha()
mute_img = pygame.image.load(resource_path('../assets/images/mute.png')).convert_alpha()

# transparency: https://stackoverflow.com/questions/12879225/pygame-applying-transparency-to-an-image-with-alpha
press_text = pygame.image.load(resource_path('../assets/images/press_the_button.png')).convert(24)
press_text.set_colorkey('magenta')
press_text.set_alpha(255)

final_arrow = pygame.image.load(resource_path('../assets/images/final_arrow.png')).convert(24)
final_arrow.set_colorkey('magenta')
final_arrow.set_alpha(0)

mouse_up = pygame.image.load(resource_path('../assets/images/hand_1.png')).convert()
mouse_down_button = pygame.image.load(resource_path('../assets/images/hand_2.png')).convert()
mouse_down = pygame.image.load(resource_path('../assets/images/hand_3.png')).convert()
mouse_up.set_colorkey('magenta')
mouse_down.set_colorkey('magenta')
mouse_down_button.set_colorkey('magenta')
mouse_up.set_alpha(255)
mouse_down_button.set_alpha(255)
mouse_down.set_alpha(255)

glass_up = pygame.image.load(resource_path('../assets/images/glass.png')).convert_alpha()
glass_down = pygame.image.load(resource_path('../assets/images/glass_broken.png')).convert_alpha()

mouse_up_demo = mouse_up.copy()
mouse_down_demo = mouse_down_button.copy()
mouse_up_demo.set_colorkey('magenta')
mouse_down_demo.set_colorkey('magenta')
mouse_up_demo.set_alpha(150)
mouse_down_demo.set_alpha(150)

# colours and text
colours = {'red': (220, 0, 52), 'gold': (255, 226, 27), 'light_gold': (228, 199, 0)}
lower_text = Text('../assets/images/lower_font.png')
upper_text = Text('../assets/images/upper_font.png')

# audio
click_audio = pygame.mixer.Sound(resource_path('../assets/sound/click.wav'))
button_audio = pygame.mixer.Sound(resource_path('../assets/sound/button.wav'))
button_ten_audio = pygame.mixer.Sound(resource_path('../assets/sound/button_ten.wav'))
button_hundred_audio = pygame.mixer.Sound(resource_path('../assets/sound/button_100_2.wav'))
button_fiveh_audio = pygame.mixer.Sound(resource_path('../assets/sound/button_500.wav'))
thousand = pygame.mixer.Sound(resource_path('../assets/sound/1000.wav'))
glass_break_audio = pygame.mixer.Sound(resource_path('../assets/sound/glass_break.wav'))

pygame.display.set_caption('PRESS THE BUTTON -- Andrew Towell')


def game():
    click = False
    game_time = 0
    mute = False
    mute_button = pygame.Rect(screen.get_width() - 8, 2 + 70, 6, 6)
    screen_shake_offset = [0, 0]
    max_shake = 8
    screen_shake_max = 10
    screen_shake_timer = 0

    presses = 0
    score_offset_timer = 0

    button = Button((9, 9 + 70), 'red', screen)
    glass_button_hitbox = pygame.Rect(14, 14, 22, 22)
    glass_b = True
    glass_light = pygame.sprite.Group()
    glass_light.add(Light(screen, (glass_button_hitbox.centerx, glass_button_hitbox.centery), 30 ,25 ,(50, 0, 50)))
    glass_light.add(Light(screen, (glass_button_hitbox.centerx, glass_button_hitbox.centery), 23, 18, (40, 40, 40)))

    particles = pygame.sprite.Group()

    mouse_image = None

    press_text_increment = 5
    press_text_offset = 5
    offset_speed = 0.05

    scroll_offset = 0

    running = True
    while running:

        # x and y mouse pos
        mx, my = pygame.mouse.get_pos()
        mx = mx//scaling_factor
        my = my//scaling_factor + 70 - scroll_offset//scaling_factor  # <--- please NEVER do this again, actually think

        # -- INPUT --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_COMMA or event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    mute = not mute
                    if mute:
                        pygame.mixer.stop()

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scroll_offset += 1 * scaling_factor
                elif event.y < 0:
                    scroll_offset -= 1 * scaling_factor

                if scroll_offset < 0:
                    scroll_offset = 0
                elif scroll_offset > 700:
                    scroll_offset = 700

            if event.type == pygame.MOUSEBUTTONDOWN:
                # button pressed checks and actions
                if event.button == 1:
                    click = True
                    # mute
                    if mute_button.collidepoint((mx, my)):
                        mute = not mute
                        if mute:
                            pygame.mixer.stop()
                    if button.check_pressed((mx, my)):
                        mouse_image = mouse_down_button
                        presses += 1
                        score_offset_timer = 0
                        if not mute:
                            button_audio.play()
                        if presses % 10 == 0 and presses % 100 != 0 and not mute:
                            button_ten_audio.play()
                        elif presses % 100 == 0 and presses != 500 and presses != 1000 and not mute:
                            button_hundred_audio.play()
                        elif presses == 500 and not mute:
                            button_fiveh_audio.play()
                        elif presses == 1000 and not mute:
                            thousand.play()
                    elif glass_button_hitbox.collidepoint((mx, my)):
                        if not mute:
                            glass_break_audio.play()
                        glass_b = False
                    else:
                        mouse_image = mouse_down
                        if not mute:
                            click_audio.play()
            else:
                #if click and button.check_pressed((mx, my)):
                click = False
                button.set_pressed()
                mouse_image = mouse_up

        # -- UPDATES --
        screen.fill('black')
        screen.blit(special_bg, (0, 0))
        screen.blit(bg, (0, 70))

        # - Text -
        if presses % 10 != 0 and presses != 0:
            lower_text.render(str(presses), screen, ((screen.get_width() - lower_text.width(str(presses)) + 2) // 2, 46 + 70 - 3 * math.sin(score_offset_timer)))
        elif presses != 0:
            upper_text.render(str(presses), screen, ((screen.get_width() - upper_text.width(str(presses)) + 2) // 2, 45 + 70))

        # buttons
        button.update()

        if glass_b:
            # light
            glass_light.update(game_time)
            screen.blit(glass_up, (4, 9))
            #pygame.draw.rect(screen, 'red', glass_button_hitbox)
        else:
            screen.blit(glass_down, (5, 7))


        # - REWARDS -
        if presses == 9:  # 10 - circles
            button.set_create_circles()
        elif presses == 99 or presses == 349:  # 100, 350 - double circles
            button.set_double_circles()
        elif presses == 200:  # 200 - gold button
            button = Button((9, 9 + 70), 'gold', screen, button.get_circles())  # TODO gold button is broken on start
            button.set_create_circles()
        elif presses == 249:  # 250 - gold circles
            button.set_circle_colour(colours['gold'])

        # red progression
        # screen shake is multiple of 10 next press
        if (presses + 1) % 10 == 0 and presses != 9 and button.colour == 'red':
            button.set_circle_colour(colours['gold'])
        # gold progression
        elif (presses + 1) % 10 == 0 and presses != 9 and button.colour == 'gold':
            button.set_circle_colour(colours['gold'])
        elif presses < 249:
            button.set_circle_colour(colours['red'])

        # screen shake if multiple of 10
        if presses % 10 == 0 and presses != 0:
            if screen_shake_timer == 0:
                screen_shake_timer = 1
                max_shake += 1
                if max_shake > 20:
                    max_shake = 20

        if mute:
            screen.blit(mute_img, (mute_button.x, mute_button.y))
        else:
            screen.blit(unmute_img, (mute_button.x, mute_button.y))

        # on game startup:
        if presses != 0:
            press_text.set_alpha(press_text.get_alpha() - press_text_increment)
            mouse_up_demo.set_alpha(0)
            mouse_down_demo.set_alpha(0)
        if 1000 <= presses <= 1019:
            final_arrow.set_alpha(final_arrow.get_alpha() + press_text_increment)
        else:
            final_arrow.set_alpha(final_arrow.get_alpha() - press_text_increment)

        # y + amplitude * sin(time * speed)
        # offset is amplitude of sin wave
        # time provides a value to sin that is updated every frame. Movement loops due to nature of sin
        # speed speeds up or slows down movement (multiplies input value to sin)
        if math.sin(game_time * offset_speed) > 0:
            screen.blit(mouse_up_demo, (19, 19 + 70))
        else:
            screen.blit(mouse_down_demo, (19, 19 + 70))

        # hand
        screen.blit(mouse_image, (mx, my))

        screen.blit(press_text, (11, int(35 + 70 + press_text_offset * math.sin(game_time * offset_speed))))
        screen.blit(final_arrow, ((screen.get_width() - final_arrow.get_width())//2, 10 + 70 + press_text_offset * math.sin(game_time * offset_speed)))

        # particles
        if random.randint(1, 20) == 5:
            particles.add(Particle(screen, colours['light_gold']))
        if glass_b:
            particles.update()

        # Screen shake
        if 0 < screen_shake_timer < screen_shake_max:
            screen_shake_offset = [random.randint(0, max_shake) - max_shake//2, random.randint(0, max_shake) - max_shake//2]
        else:
            screen_shake_offset = [0, 0]
            # reset shake timer if not on a shake press
        if screen_shake_timer >= screen_shake_max and presses % 10 != 0:
            screen_shake_timer = 0

        window.fill('black')
        window.blit(pygame.transform.scale(screen, (window.get_width(), window.get_height()*2)), (screen_shake_offset[0], screen_shake_offset[1] + scroll_offset - 700))  # scale screen to window

        # Timers
        game_time += 1
        if score_offset_timer < 3:
            score_offset_timer += 1
        if screen_shake_timer > 0:
            screen_shake_timer += 1

        # -- RENDER --
        pygame.display.update()
        clock.tick(game_speed)

        if not glass_b:
            time.sleep(2)
            running = False
            pygame.quit()
            sys.exit()


game()