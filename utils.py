import sys
import os
import pygame
import random

from settings import WIDTH, HEIGHT, HORSE_IMAGES, HORSE_SHAPE_LIST


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


def show_winning_text(screen, horse):
    # if more than one horse crossed the line
    if len(horse) > 1:
        text = 'Remis'
    else:
        text = f'{horse[0].name} wygrał'

    # write text on the screen
    # create font
    font = pygame.font.Font(None, 56)
    # add text to a font
    text_surface = font.render(text, True, (0, 0, 0))

    # add text to a screen
    screen.blit(
        text_surface,
        (
            WIDTH // 2 - text_surface.get_width() // 2,
            HEIGHT // 2 - text_surface.get_height() // 2 - 100
        )
    )  # text, (pos_x, pos_y)


def draw_table_with_horses(screen, horse_group):
    """
    in:
        screen: object
        horse_group: list()

    table structure:
        | Imię    | współczynnik wygranej |
        | Buzefal | 1.3                   |
    """
    # TODO: iteruj po koniach w grupie i maluj rząd tablic zawierający imię konia i jego współczynnik dla każdego konia
    # Przykład jak malować text jest w funkcji `show_winning_text`
    # use win_rate_counter dla obliczania współczynnika wygranej  
    pass


def win_rate_counter(start_pos):
    # TODO: obliczyć współczynnik wygranej na bazie `start_pos`
    # maksymalna wartość `start_pos` wynosi 5, minimalna wynosi 0
    # zakładamy że dla maximum podajemy wspólczynnik 1.3, dla minimum 2.3
    # wszystko pomiędzy zostanie obliczone według wzoru, który musisz wymyślić
    # maksymalna wartość `start_pos` i minimalna ustalia się w settings.py i ją morzesz zmieniać jeśli ci nie będzie pasować
    # również wspólczynnik 1.3, i dla minimum 2.3 też nie jest stalą liczbą
    pass


def recalculate_start_pos(cursor, horse_group):
    # TODO: dla każdego konia prelicz nową wartość `start_pos` i zapisz (użyj horse.save(cursor) dla konia z nową wartością `start_pos`)
    # Posortuj liste po horse.points
    # dla konia z największym znaczenia `points` dodaj 1 do `start_pos`
    # dla konia na pozycji No 2 dodaj 0.5
    # dla konia na pozycji No 3 dodaj 0
    # dla konia na pozycji No 4 dodaj -0.5
    pass
