"""
=========================================
The games models with theirs ORM managers
=========================================
"""
import pygame
import random

from utils import resource_path


class HorseManager:
    """ORM manager for Horse model"""

    def create(cursor, name, start_pos):
        sql = "INSERT INTO HORSE (name, start_pos) VALUES (?,?)"
        values = (name, start_pos)
        cursor.execute(sql, values)
        return Horse(id=cursor.lastrowid, name=name, start_pos=start_pos)

    def filter(cursor, fieldname, value):
        sql = f'SELECT id, name, start_pos FROM HORSE WHERE {fieldname}=?'
        cursor.execute(sql, (str(value), ))
        data = cursor.fetchone()
        if data:
            id_, name, start_pos = data
            loaded_horse = Horse(name=name, start_pos=start_pos)
            return loaded_horse
        else:
            return None

    def all(cursor):
        sql = 'SELECT id, name, start_pos FROM HORSE'
        cursor.execute(sql)
        horses_list = list()
        for row in cursor.fetchall():
            id_, name, start_pos = row
            loaded_horse = Horse(id=id_, name=name, start_pos=start_pos)
            horses_list.append(loaded_horse)
        return horses_list

    def delete(cursor, id):
        sql = "DELETE FROM HORSE WHERE id=?"
        cursor.execute(sql, (str(id),))
        return True

    def update(cursor, start_pos, id):
        sql = """
            UPDATE HORSE
            SET start_pos=?
            WHERE id=?
        """
        values = (start_pos, id)
        cursor.execute(sql, values)
        return cursor.lastrowid


class Horse(pygame.sprite.Sprite):
    """The hourse Model

    Argument
    -----------
    pos_x, pos_y: integers (Position in a screen)
    shape: random item from list(self.random_events)
    points: integer
        After initializating house have start_pos to 0,
        After each race, each horse receives points and starts_pos is calculated again
    name: string

    Methods
    ----------
    animate
        if true, animate the horse (changing index images from :self.sprites:)

    stop_animate

    increase_points

    get_value
        get hourse position after the GAME loop is rotated

    change_position
        change horse position in 'x' coordinates on the screen

    update
        Update horse position in 'x' coordinates and draw this horse in a screen
    """

    random_events = [-4, -3, -2, 0]
    manager = HorseManager

    def __init__(self, id=-1, pos_x=20, pos_y=540, start_pos=0, shape=None, points=0, name=None):
        super().__init__()

        self.id = id

        self.pos_x = pos_x
        self.pos_y = pos_y
        # start shape
        self.start_pos = start_pos
        # random shape (To give a more random result)
        self.shape = shape

        self.name = name

        self.sprites = []
        self.sprites.append(pygame.image.load(resource_path('.\\assets\\kon1.png')))
        self.sprites.append(pygame.image.load(resource_path('.\\assets\\kon2.png')))
        self.sprites.append(pygame.image.load(resource_path('.\\assets\\kon3.png')))
        self.sprites.append(pygame.image.load(resource_path('.\\assets\\kon4.png')))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

        # animating
        self.is_animating = False
        self.points = points

    def animate(self):
        """Start animating"""
        self.is_animating = True

    def stop_animate(self):
        self.is_animating = False

    def increase_points(self, points):
        """Add some value for x coordinate"""
        self.points += points
        return self.points

    def get_value(self):
        """
        Combine current position in x coordinate with random value 'shape' (It will be the same throughout the entire race)
        and with randomly chosen number from :self.random_events: and combine with horse's 'start_pos'
        """

        result = self.pos_x + self.shape + random.choice(self.random_events) + self.start_pos
        result = self.increase_points(result)
        return result

    def change_position(self, position):
        """Change object's positin atribute"""
        self.pos_x = position

    def update(self):
        """Update horse position in 'x' coordinates and draw this horse in a screen"""
        self.rect.center = [self.pos_x + self.points, self.pos_y]
        if self.is_animating:
            self.current_sprite += 0.15

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
            self.image = pygame.transform.scale(self.image, (60, 60))


class Finish:

    def __init__(self, start_pos, pos_x, pos_y, image):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.rect = self.image.get_rect()

    def check_collide(self, horse):

        return self.rect.colliderect(horse.rect)
