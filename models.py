import pygame
import random

class Horse(pygame.sprite.Sprite):

    random_events = [-4, -3, -2, 0]

    def __init__(self, pos_x, pos_y, start_pos, shape, points=0, name=None):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('./assets/kon1.png'))
        self.sprites.append(pygame.image.load('./assets/kon2.png'))
        self.sprites.append(pygame.image.load('./assets/kon3.png'))
        self.sprites.append(pygame.image.load('./assets/kon4.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        # form start
        self.start_pos = start_pos
        self.shape = shape

        self.pos_x=pos_x
        self.pos_y=pos_y

        self.name = name

        # animating
        self.is_animating = False
        self.points = points

    def animate(self):
        self.is_animating = True

    def stop_animate(self):
        self.is_animating = False
 
    def increase_points(self, points):
        self.points += points
        return self.points
    
    def get_value(self):

        result = self.pos_x + self.shape + random.choice(self.random_events) + self.start_pos
        result = self.increase_points(result)
        return result
    
    def change_position(self, position):
        self.pos_x = position

    def update(self):
        self.rect.center = [self.pos_x + self.points, self.pos_y]
        if self.is_animating:
            self.current_sprite += 0.15

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
            self.image = pygame.transform.scale(self.image, (60,60))


class Finish:

    def __init__(self, start_pos, pos_x, pos_y, image):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.image = image
        self.rect = self.image.get_rect()


    def check_collide(self, horse):
        
        return self.rect.colliderect(horse.rect)