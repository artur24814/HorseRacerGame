"""
=========================================
The games main loop
=========================================
"""
import pygame, sys
import random
from settings import WIDTH, HEIGHT
from models import Horse, Finish

pygame.init()

# setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# load background
background = pygame.image.load('./assets/tor.jpg')

# Title of the window
pygame.display.set_caption("The Best GAME")


#init the games clock
clock =pygame.time.Clock()
pygame.mouse.set_visible(False)


# Init horses Group

horse_group = pygame.sprite.Group()

shape = [0, 1, 4, 8]

# create horse object nad add them to a Hourse groupe
index = 1
for _ in range(4):
    new_horse = Horse(20, 500 + 40 * index, start_pos=0, shape=random.choice(shape), name=f"Koń {index}")
    horse_group.add(new_horse)
    index += 1

counter = 0
run_horse = False
stop_game = False
winning_horse = list()

def show_winning_text(screen, horse):
    if len(horse) > 1:
        text = 'Remis'
    else:
        text = f'{horse[0].name} wygrał'
    font = pygame.font.Font(None,56)

    text_surface = font.render(text, True, (0, 0, 0))

    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2 -100))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            run_horse = True
            for horse in horse_group:       
                horse.animate()

    current_time = pygame.time.get_ticks()
   
    current_time = pygame.time.get_ticks()

    # set background image
    screen.blit(background, (0,0))
    
    horse_group.draw(screen)
    horse_group.update()

    if counter >= 20 and run_horse:
        for horse in horse_group:       
            value = horse.get_value()
            if value + horse.pos_x >= WIDTH - 100:
                print(f'{horse.name} wygrał')
                winning_horse.append(horse)
                stop_game = True
                run_horse = False
                for horse in horse_group:       
                    horse.stop_animate()

        counter = 0

    counter += 1
    if stop_game and winning_horse:
        show_winning_text(screen, winning_horse)
    pygame.display.flip()
    clock.tick(60)
