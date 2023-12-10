from models import Horse


def test_create_new_horse(test_database, horse):
    """One already exist add new one"""
    cnx, cursor = test_database
    assert len(Horse.manager.all(cursor)) == 1

    Horse.manager.create(cursor=cursor, name='Koń', start_pos=3)
    cnx.commit()

    assert len(Horse.manager.all(cursor)) == 2


def test_delete_horse(test_database, horse):
    """Delete horse from database"""
    cnx, cursor = test_database

    horses = Horse.manager.all(cursor)
    assert len(horses) == 1

    Horse.manager.delete(cursor=cursor, id=horses[0].id)
    cnx.commit()

    assert len(Horse.manager.all(cursor)) == 0


def test_update_horse(test_database, horse):
    """Update horse and check new value"""
    cnx, cursor = test_database

    horse = Horse.manager.filter(cursor, 'id', 1)
    assert horse is not None
    assert horse.start_pos == 3

    Horse.manager.update(cursor=cursor, start_pos=10, id=1)
    cnx.commit()

    updated_horse = Horse.manager.filter(cursor, 'id', 1)

    assert updated_horse.start_pos == 10


def test_filter_horse(test_database, horse):
    """Update horse and check new value"""
    cnx, cursor = test_database

    horse = Horse.manager.filter(cursor, 'name', 'Koń')
    assert horse is not None
    assert horse.name == 'Koń'

    horse = Horse.manager.filter(cursor, 'name', 'Jon')
    assert horse is None
