from sqlalchemy.sql.expression import func
from random import sample
import db.dbconfig as dbconfig
from db.dbconfig import NamePrefix, NameSuffix, Horse

session = None
def init_horse_manager():
    global session
    session = dbconfig.get_session()
    print(dbconfig.get_session())
    add_missing_names_to_db()

def add_missing_names_to_db():
    prefixes_from_file = read_file_to_list('HorseManagement/name_prefix.txt')
    existing_prefixes = {name[0] for name in session.query(NamePrefix.name).all()}
    for name in prefixes_from_file:
        if name not in existing_prefixes:
            session.add(NamePrefix(name=name))

    suffixes_from_file = read_file_to_list('HorseManagement/name_suffix.txt')
    existing_suffixes = {name[0] for name in session.query(NameSuffix.name).all()}
    for name in suffixes_from_file:
        if name not in existing_suffixes:
            session.add(NameSuffix(name=name))

    session.commit()

def read_file_to_list(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]

def create_horse(name=None, start_pos=0):
    if name is None:
        name = create_unique_horse_name()
    horse = Horse(name=name, start_pos=start_pos)
    session.add(horse)
    session.commit()
    return horse

def create_unique_horse_name():
    total_prefixes = session.query(NamePrefix).count()
    total_suffixes = session.query(NameSuffix).count()
    total_combinations = total_prefixes * total_suffixes

    counter = 0
    generated_name = None
    while counter < total_combinations:
        prefix = session.query(NamePrefix).order_by(func.random()).first()
        suffix = session.query(NameSuffix).order_by(func.random()).first()
        name = f'{prefix.name} {suffix.name}'
        if session.query(Horse).filter_by(name=name).count() == 0:
            generated_name = name
        counter += 1
    return generated_name

def get_horse_by_name(name):
    return session.query(Horse).filter_by(name=name).first()

def get_horse_by_id(id):
    return session.query(Horse).filter_by(id=id).first()

def get_all_horses():
    return session.query(Horse).all()

def get_random_horses(count = 4):
    all_horse_ids = [horse.id for horse in session.query(Horse.id).all()]
    if len(all_horse_ids) <= count:
        return session.query(Horse).all()
    random_ids = sample(all_horse_ids, count)
    return session.query(Horse).filter(Horse.id.in_(random_ids)).all()

def update_horse(horse):
    session.add(horse)
    session.commit()

def delete_horse(horse):
    session.delete(horse)
    session.commit()