"""
=========================================
The games main loop
=========================================
"""
import pygame
import sys
import random

from settings import WIDTH, HEIGHT
from models import Horse
from db.db import db_init, create_connect
from utils import resource_path


pygame.init()

# init DB
db_init()
cursor, cnx = create_connect()

# setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# load background
background = pygame.image.load(resource_path('.\\assets\\start_page.png'))
start_page = True

# play music
bg_music = pygame.mixer.Sound(resource_path('.\\assets\\audio\\horse_game.wav'))
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# horse run sound
horse_run_sound = pygame.mixer.Sound(resource_path('.\\assets\\audio\\horse_galopp.mp3'))
horse_run_sound.set_volume(0.1)

# cklick sound
click_sound = pygame.mixer.Sound(resource_path('.\\assets\\audio\\click.mp3'))
click_sound.set_volume(0.1)


# Title of the window
pygame.display.set_caption("The Best GAME")


# init the games clock
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


# Init horses Group
horse_group = pygame.sprite.Group()

shape = [0, 1, 4, 8]

# Get all horses from databases
# filled horse objects by position x and y in a screen and data (id, name, start_pos) from databases
# add them to a Hourse groupe
index = 1
for horse in Horse.manager.all(cursor):
    new_horse = Horse(
        id=horse.id,
        pos_x=20,
        pos_y=500 + 40 * index,
        start_pos=horse.start_pos,
        shape=random.choice(shape),
        name=horse.name
    )
    horse_group.add(new_horse)
    index += 1

counter = 0
# When True update horse value
run_horse = False
# When True show winning text in a screen
stop_game = False

winning_horse = list()


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
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2 - 100))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if start_page:
                background = pygame.image.load(resource_path('.\\assets\\tor.jpg'))
                click_sound.play()
                start_page = False
            else:
                run_horse = True
                horse_run_sound.play(loops=-1)
                for horse in horse_group:
                    horse.animate()

    # set background image
    screen.blit(background, (0, 0))

    # draw horses and update their positions
    horse_group.draw(screen)
    horse_group.update()

    # do this only every 20 ms
    if counter >= 20 and run_horse:

        # for every houses in a group update their values
        # Then in the loop, if the race is not finished, update each horse position with the new value
        for horse in horse_group:
            value = horse.get_value()

            # Check that each horse has not crossed the line.
            # If so, add this horse which crossed the line to the list.
            if value + horse.pos_x >= WIDTH - 100:
                print(f'{horse.name} wygrał')

                winning_horse.append(horse)

                # finish race and stop horse animation
                stop_game = True
                run_horse = False
                horse_run_sound.stop()
                for horse in horse_group:
                    horse.stop_animate()

        # refresh counter
        counter = 0

    counter += 1

    if stop_game and winning_horse:
        show_winning_text(screen, winning_horse)

    pygame.display.flip()

    # 60 ms per second
    clock.tick(60)
