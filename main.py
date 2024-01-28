"""
=========================================
The game main loop
=========================================
"""
import pygame
import sys

from settings import WIDTH, HEIGHT
from models import Horse, Crosshair, Money
from db.db_config import db_init, create_connect
from utils import (
    resource_path,
    show_winning_text,
    init_horse_group,
    add_text_to_a_screen,
    draw_table_with_horses,
    draw_rectangle,
    recalculate_start_pos,
    win_rate_counter
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
pygame.display.set_caption("GAMBLE GALLOP")
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

# shot sound
shot_sound = pygame.mixer.Sound(resource_path('.\\assets\\audio\\shot.wav'))
shot_sound.set_volume(0.1)

# init the games clock
clock = pygame.time.Clock()

# hide standart mouse cursor on top of the screen
pygame.mouse.set_visible(False)

# Init custome cursor class
crosshair = Crosshair('./assets/curs.png')
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Init Money class
money = Money('./assets/money.jpg', -30)
money_group = pygame.sprite.Group()
money_group.add(money)

player_money = 2000

# Init horses Group
horse_group = init_horse_group(cursor)

# group of variables for animating the start page
# we start displaying the text in large font and reduce it to normal size
counter_start_page_anim = 300

# variable for animating the money counter
# start count from zero to player actual amount of money
counter_start_money_anim = 0

# group of variables for animating betting on the horse
# we start drowing money on top of the screen and put then onthe betting horse
counter_money_position_animation = -30
money_bet_position = -30

# When True update horse value (animate horse)
run_horse = False

# When True show winning text in a screen
stop_game = False

winning_horse = list()

# create custome event every 20 milsec
EVERY20MILSEC = pygame.USEREVENT
pygame.time.set_timer(EVERY20MILSEC, 400)  # 20 mlsec

horse_for_bet = None
bet_done = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cnx.close()
            pygame.quit()
            sys.exit()

        # if any key pressed:
        if event.type == pygame.KEYDOWN:
            # go to the next page for the current start window
            if start_page:
                background = pygame.image.load(resource_path('.\\assets\\tor.jpg'))
                click_sound.play()
                start_page = False

            # If not the starting window, start ride after push any button
            # run horse, play sound
            elif not start_page and not run_horse and not stop_game:
                run_horse = True
                horse_run_sound.play(loops=-1)
                shot_sound.play()
                for horse in horse_group:
                    horse.animate()

            # when race is over move horse to a start after push any button
            # and recalculate their `start_pos`
            elif not start_page and not run_horse and stop_game:
                winning_horse = []
                stop_game = False

                # NOTE: the count should take place before moving the horses to the start
                recalculate_start_pos(cursor=cursor, horse_group=horse_group)

                # commit changes to a database
                cnx.commit()

                # moving the horses to the start
                for horse in horse_group:
                    horse.finish_ride()
                    bet_done = False

        # if mouse clicked
        # and the bet hasn't done yet
        if event.type == pygame.MOUSEBUTTONDOWN and horse_for_bet and not bet_done:
            money_bet_position = horse_for_bet.pos_y

            # for each horse in the group, find the horse on which we clicked as a horse on which we are betting money
            # reduce the player's money and set this horse's variable `betted` as True
            # for others set variable `betted` as False
            for horse in horse_group:
                if horse == horse_for_bet:
                    horse.betted = True
                    player_money -= 100
                    counter_start_money_anim = 0
                    bet_done = True
                else:
                    horse.betted = False

        # special custome event
        # recalculate randome event for each horse if race has been started
        if event.type == EVERY20MILSEC and not start_page and run_horse:

            # for every horses in a group update their values
            # Then in the loop, if the race is not finished, update each horse position with the new value
            for horse in horse_group:
                value = horse.get_value()

                # Check that each horse has not crossed the line.
                # If so, add this horse which crossed the line to the list.
                if value + horse.pos_x >= WIDTH - 100:

                    winning_horse.append(horse)

                    # finish race and stop horse animation
                    stop_game = True
                    run_horse = False
                    horse_run_sound.stop()
                    for horse in horse_group:
                        horse.stop_animate()

    # set background image
    screen.blit(background, (0, 0))

    # on the start page we don't need horses
    # only texts
    if start_page:
        # NOTE:  we use counter_start_page_anim variable for animation main font
        # define main font size as equal to counter_start_page_anim
        main_font = pygame.font.Font(resource_path('.\\assets\\fonts\\v5_prophit_cell\\V5PRD___.TTF'), counter_start_page_anim)

        add_text_to_a_screen(
            screen=screen,
            text='Gamble Gallop GAME',
            font=main_font,
            center=True,
            center_plus_y=-50
        )
        # stop reducing the size 50 counter
        if counter_start_page_anim >= 50:
            counter_start_page_anim -= 3

        add_text_to_a_screen(
            screen=screen,
            text='Press any button to start',
            font=winning_font,
            center=True,
            center_plus_y=200,
            color=(0, 0, 255)
        )

    # if it's not start page > draw horses
    if not start_page:
        # draw horses and update their positions
        horse_group.draw(screen)
        horse_group.update()

    # if the race didn't take place and we have an any winning horse
    if stop_game and winning_horse:
        show_winning_text(screen, winning_horse, winning_font)

        # iterates over the winning horses, check if we have the horse we are betting money on
        for horse in winning_horse:
            if horse.betted is True:
                # increase player's money
                player_money += (100 * win_rate_counter(horse.start_pos))
                horse.betted = False

        # refresh money counter
        counter_start_money_anim = 0
        counter_money_position_animation = -30
        money_bet_position = -30

    # window between the start page and the race and after the race before the next race
    # in this window we show the table with horses winning rate
    # and in this window we can place bets
    if not start_page and not stop_game and not winning_horse and not run_horse:

        # animate money counter (Start at 0 and increase to reach the player's money amount)
        if counter_start_money_anim < player_money:
            counter_start_money_anim += 30

        # in case that after increasing the counter it will be more than the player's money
        if counter_start_money_anim > player_money:
            counter_start_money_anim = player_money

        # show money counter
        add_text_to_a_screen(screen, f'{counter_start_money_anim}$', pos_x=20, pos_y=10, font=table_font)

        # draw rectangle under a table (for better reading)
        draw_rectangle(screen=screen, size=(300, 180, 600, 180), color=(50, 50, 50))
        draw_table_with_horses(screen=screen, horse_group=horse_group, font=table_font)

        # Checking if cursor is colliding with horse rect
        # usind colliderect() method.
        # It will return a horse object
        collide = pygame.sprite.spritecollideany(
            crosshair,
            horse_group,
        )

        if collide:
            # set horse_for_bet variable as this horse object
            horse_for_bet = collide
        else:
            # clean this variable
            horse_for_bet = None

        money.pos_y = counter_money_position_animation

        if money_bet_position != -30 and counter_money_position_animation < money_bet_position:
            counter_money_position_animation += 30

        # draw money
        money_group.draw(screen)
        money_group.update()

    # draw cursor
    crosshair_group.draw(screen)
    crosshair_group.update()

    pygame.display.flip()

    # 60 ms per second
    clock.tick(60)
