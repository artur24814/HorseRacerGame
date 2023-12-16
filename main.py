"""
=========================================
The games main loop
=========================================
"""
import pygame
import sys

from settings import WIDTH, HEIGHT
from models import Horse
from db.db_config import db_init, create_connect
from utils import (
    resource_path,
    show_winning_text,
    init_horse_group,
    add_text_to_a_screen,
    draw_table_with_horses,
    recalculate_start_pos
)


pygame.init()

# init DB
db_init()
cursor, cnx = create_connect()
horses = Horse.manager.all(cursor)
print(horses)

# Init Game Fonts
main_font = pygame.font.Font(resource_path('.\\assets\\fonts\\v5_prophit_cell\\V5PRD___.TTF'), 50)
table_font = pygame.font.Font(resource_path('.\\assets\\fonts\\perfect_dos_vga_437\\Perfect DOS VGA 437 Win.ttf'), 40)
winning_font = pygame.font.Font(resource_path('.\\assets\\fonts\\retro_land_mayhem\\retro-land-mayhem.ttf'), 66)

# setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# load background
background = pygame.image.load(resource_path('.\\assets\\start_page.png'))
# Title of the window
pygame.display.set_caption("The Best GAME")
start_page = True

# init music
# background music
bg_music = pygame.mixer.Sound(resource_path('.\\assets\\audio\\horse_game.wav'))
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# horse run sound
horse_run_sound = pygame.mixer.Sound(resource_path('.\\assets\\audio\\horse_galopp.mp3'))
horse_run_sound.set_volume(0.3)

# cklick sound
click_sound = pygame.mixer.Sound(resource_path('.\\assets\\audio\\click.mp3'))
click_sound.set_volume(0.1)


# init the games clock
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


# Init horses Group
horse_group = init_horse_group(cursor)

counter = 0
# When True update horse value
run_horse = False
# When True show winning text in a screen
stop_game = False

winning_horse = list()

# create custome event every 20 milsec
EVERY20MILSEC = pygame.USEREVENT
pygame.time.set_timer(EVERY20MILSEC, 400)  # 20 mlsec


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cnx.close()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if start_page:
                background = pygame.image.load(resource_path('.\\assets\\tor.jpg'))
                click_sound.play()
                start_page = False

            # start ride
            elif not start_page and not run_horse and not stop_game:
                run_horse = True
                horse_run_sound.play(loops=-1)
                for horse in horse_group:
                    horse.animate()

            # when race is over move horse to a start
            elif not start_page and not run_horse and stop_game:
                winning_horse = []
                stop_game = False

                # NOTE: the count should take place before moving the horses to the start
                recalculate_start_pos(cursor=cursor, horse_group=horse_group)

                # commit changes to a database
                cnx.commit()

                # moving the horses to the start
                for horse in horse_group:
                    horse.pos_x = 20
                    horse.points = 0
                    horse.shape_randomize()

        if event.type == EVERY20MILSEC and not start_page and run_horse:

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

    # set background image
    screen.blit(background, (0, 0))

    if start_page:
        add_text_to_a_screen(
            screen=screen,
            text='Horse Racer GAME',
            font=main_font,
            center=True,
            center_plus_y=-50
        )

    if not start_page:
        # draw horses and update their positions
        horse_group.draw(screen)
        horse_group.update()

    if stop_game and winning_horse:
        show_winning_text(screen, winning_horse, winning_font)

    if not start_page and not stop_game and not winning_horse and not run_horse:
        draw_table_with_horses(screen=screen, horse_group=horse_group, font=table_font)

    pygame.display.flip()

    # 60 ms per second
    clock.tick(60)
