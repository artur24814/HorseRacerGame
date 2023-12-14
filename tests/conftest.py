import sqlite3
import pytest
import tempfile

from db.db_config import CREATE_HORSE_TABLE, CREATE_PLAYER_TABLE
from models import Horse


@pytest.fixture
def test_database():
    db_fd, db_path = tempfile.mkstemp()
    cnx = sqlite3.connect(db_path)
    cursor = cnx.cursor()
    cursor.execute(CREATE_PLAYER_TABLE)
    cursor.execute(CREATE_HORSE_TABLE)
    cnx.commit()
    return cnx, cursor


@pytest.fixture
def horse(test_database):
    cnx, cursor = test_database
    horse = Horse.manager.create(cursor=cursor, name='Koń', start_pos=3)
    cnx.commit()
    return horse
