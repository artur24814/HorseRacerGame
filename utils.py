import sys
import os
import pygame
import random

from settings import WIDTH, HEIGHT, HORSE_IMAGES, HORSE_SHAPE_LIST, MAX_START_POS


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def init_horse_group(cursor):
    """Add hose objects to a sprite group"""
    from models import Horse

    # Init horses Group
    horse_group = pygame.sprite.Group()

    # Get all horses from databases
    # filled horse objects by position x and y in a screen and data (id, name, start_pos) from databases
    # add them to a Hourse groupe
    index = 1
    for horse in Horse.manager.all(cursor):
        horse.pos_x = 20
        horse.pos_y = 500 + 40 * index
        horse.shape = random.choice(HORSE_SHAPE_LIST)
        horse.horse_images = HORSE_IMAGES
        horse.setup_images()

        horse_group.add(horse)
        index += 1

    return horse_group


def show_winning_text(screen, horse, font):
    """Show text when any horse croses the line"""
    # if more than one horse crossed the line
    if len(horse) > 1:
        text = 'Remis'
    else:
        text = f'{horse[0].name} Win !!!'

    # add text to a screen
    add_text_to_a_screen(
        screen=screen,
        text=text,
        font=font,
        center=True,
        center_plus_y=-100
    )


def add_text_to_a_screen(screen, text, pos_x=None, pos_y=None, font=None, center=False, center_plus_y=None, color=None):
    """write text on the screen"""
    # add text to a font
    text_surface = font.render(text, True, (0, 0, 0))

    if color:
        text_surface = font.render(text, True, color)

    # if we need text in a center of a screen
    if center:
        pos_x = WIDTH // 2 - text_surface.get_width() // 2
        pos_y = HEIGHT // 2 - text_surface.get_height() // 2

    # cusomize center of a Y
    if center_plus_y:
        pos_y = HEIGHT // 2 - text_surface.get_height() // 2 + center_plus_y

    screen.blit(text_surface, (pos_x, pos_y))


def draw_rectangle(screen, size, color):
    """
    in:
        screen: main GAME screen
        size: tuple(posx, pos_y, size_x, size_y)
        color: tuple(rgb)
    """
    pygame.draw.rect(screen, color, pygame.Rect(size))


def draw_table_with_horses(screen, horse_group, font):
    """
    Iterating by horse in horses_group and add horses name and count win rate for this horse

    in:
        screen: object
        horse_group: list()

    table structure:
        | Imię    | współczynnik wygranej |
        | Bucefal | 1.3                   |
    """

    headers1 = '| Name'
    headers2 = '| Rate'

    positon_x_1_col = 300
    positon_x_2_col = 720
    positon_y = 180

    # add col 1 to a screen
    add_text_to_a_screen(screen=screen, text=headers1, pos_x=positon_x_1_col, pos_y=positon_y, font=font, color=(255, 255, 255))
    # add col 2 to a screen
    add_text_to_a_screen(screen=screen, text=headers2, pos_x=positon_x_2_col, pos_y=positon_y, font=font, color=(255, 255, 255))

    for i, horse in enumerate(horse_group, 1):

        # add col 1 to a screen
        add_text_to_a_screen(
            screen=screen,
            text=f'| {horse.name}',
            pos_x=positon_x_1_col,
            pos_y=positon_y + (i * 35),
            font=font,
            color=(255, 255, 255)
        )
        # add col 2 to a screen
        add_text_to_a_screen(
            screen=screen,
            text=f'| {win_rate_counter(horse.start_pos)}',
            pos_x=positon_x_2_col, pos_y=positon_y + (i * 35),
            font=font,
            color=(255, 255, 255)
        )


def win_rate_counter(start_pos):
    """count winrate base on `start_pos`"""
    # we assume that for max win rate is 1.3
    # count coefficent from max `start_pos`
    if start_pos == 0:
        return 6.3

    return round((MAX_START_POS / start_pos) * 1.3, 1)


def recalculate_start_pos(cursor, horse_group):
    """for each horse count new start_pos base on current points after race"""
    # sort group by points
    sorted_horse_group = sorted(horse_group, key=lambda horse: horse.points)

    # recalculate `start_pos` and save
    for i, horse in enumerate(sorted_horse_group):
        # TODO: Weź pod uwagę MAX_START_POS i MAX_START_POS z pliku setting
        # musimy to ograniczyć od dołu i od góry, aby nie było bezsensownych zabiegów (kiedy wynik będzie znany z góry)
        horse.start_pos = horse.start_pos + (1 - i * 0.5)
        horse.save(cursor)
