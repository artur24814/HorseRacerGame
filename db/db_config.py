import sqlite3
import random
from models import Horse


CREATE_HORSE_TABLE = """
    CREATE TABLE HORSE (
        id INTEGER NOT NULL,
        name TEXT,
        start_pos REAL,
        PRIMARY KEY (id)
    )"""

CREATE_PLAYER_TABLE = """
    CREATE TABLE PLAYER (
        id INTEGER NOT NULL,
        name TEXT,
        money REAL,
        win INTEGER,
        lose INTEGER,
        PRIMARY KEY (id)
    )"""


def create_connect():
    cnx = sqlite3.connect('horseracer.db')
    cursor = cnx.cursor()
    return cursor, cnx


def db_init():
    cursor, cnx = create_connect()
    try:
        cursor.execute(CREATE_HORSE_TABLE)
        print('Table HORSE created!')
        prefixes_from_file = read_file_to_list('db/name_prefix.txt')
        suffixes_from_file = read_file_to_list('db/name_suffix.txt')

        unique_horses = list()

        while len(unique_horses) <= 3:
            random_name = f'{random.choice(prefixes_from_file)} {random.choice(suffixes_from_file)}'

            if not Horse.manager.filter(cursor, 'name', random_name):
                horse = Horse.manager.create(cursor, random_name, 1.5)
                unique_horses.append(horse)
                cnx.commit()

    except Exception as e:
        print(str(e))

    try:
        cursor.execute(CREATE_PLAYER_TABLE)
        print('Table PLAYER created!')

    except Exception as e:
        print(str(e))

    cnx.commit()
    cnx.close()


def read_file_to_list(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]
