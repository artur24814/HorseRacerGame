"""
=========================================
The games models with theirs ORM managers
=========================================
"""
import pygame
import random


from settings import HORSE_SHAPE_LIST
from utils import resource_path


class HorseManager:
    """ORM manager for Horse model"""

    def create(self, cursor, name, start_pos):
        sql = "INSERT INTO HORSE (name, start_pos) VALUES (?,?)"
        values = (name, start_pos)
        cursor.execute(sql, values)
        return Horse(id=cursor.lastrowid, name=name, start_pos=start_pos)

    def filter(self, cursor, fieldname, value):
        sql = f'SELECT id, name, start_pos FROM HORSE WHERE {fieldname}=?'
        cursor.execute(sql, (str(value), ))
        data = cursor.fetchone()
        if data:
            id_, name, start_pos = data
            loaded_horse = Horse(name=name, start_pos=start_pos)
            return loaded_horse
        else:
            return None

    def all(self, cursor):
        sql = 'SELECT id, name, start_pos FROM HORSE'
        cursor.execute(sql)
        horses_list = list()
        for row in cursor.fetchall():
            id_, name, start_pos = row
            loaded_horse = Horse(id=id_, name=name, start_pos=start_pos)
            horses_list.append(loaded_horse)
        return horses_list

    def delete(self, cursor, id):
        sql = "DELETE FROM HORSE WHERE id=?"
        cursor.execute(sql, (str(id),))
        return True

    def update(self, cursor, start_pos, id):
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

    random_events = [-8, -3, -2, 0]
    manager = HorseManager()

    def __init__(self, id=-1, pos_x=20, pos_y=540, start_pos=0, shape=None, points=0, name=None, horse_images=None):
        super().__init__()

        self.id = id

        self.pos_x = pos_x
        self.pos_y = pos_y
        # start shape
        self.start_pos = start_pos
        # random shape (To give a more random result)
        self.shape = shape

        self.name = name

        # setup horse images
        self.sprites = []
        self.horse_images = horse_images

        # animating
        self.is_animating = False
        self.points = points

        # betting
        self.betted = False

    def shape_randomize(self):
        self.shape = random.choice(HORSE_SHAPE_LIST)

    def setup_images(self):
        self.sprites = [pygame.image.load(resource_path(image)) for image in self.horse_images]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image, (60, 60))

        # create rectangle
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]

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

    def betting_on_this_horse(self):
        """We are betting on this horse"""
        self.betted = True

    def finish_ride(self):
        """
        When ride is over:
        set betted to false,
        move horse in a start,
        Ramdomize shape for next ride
        """
        self.betted = False
        self.pos_x = 20
        self.points = 0
        self.shape_randomize()

    def update(self):
        """Update horse position in 'x' coordinates and draw this horse in a screen"""
        self.rect.center = [self.pos_x + self.points, self.pos_y]
        if self.is_animating:
            self.current_sprite += 0.15

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
            self.image = pygame.transform.scale(self.image, (60, 60))

    def save(self, cursor):
        """Create new record in DB, or update existing"""
        if self.id == -1:
            sql = """INSERT INTO HORSE (name, start_pos)
                            VALUES(?, ?) RETURNING id"""
            values = (self.name, self.start_pos)
            cursor.execute(sql, values)
            self.id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE HORSE  SET name=?, start_pos=?
                           WHERE id=?"""
            values = (self.name, self.start_pos, self.id)
            cursor.execute(sql, values)
            return True

    def __repr__(self):
        return f"ID: {self.id}, NAME: {self.name}, start_pos: {self.start_pos}"


class PlayerManager:
    """ORM manager for Player model"""

    # TODO:
    def create(self, cursor, name):
        pass

    def filter(self, cursor, fieldname, value):
        pass

    def all(self, cursor):
        pass

    def update(self, cursor, id, money):
        pass

    def delete(self, cursor, id):
        pass


class Player:
    manager = PlayerManager()

    def __init__(self, id=-1, name='Player', win=0, lose=0, money=2000):
        self.id = id
        self.name = name
        self.win = win
        self.lose = lose
        self.money = money

    def save(self):
        # TODO:
        if self.id == -1:
            # create new
            pass
        else:
            # update
            pass


class Crosshair(pygame.sprite.Sprite):
    """Cursor class"""

    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Money(pygame.sprite.Sprite):
    """Money class"""

    def __init__(self, path, pos_y, pos_x=20):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (45, 25))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = [self.pos_x, self.pos_y]
