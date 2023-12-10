from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///db/horseracer.db', echo=True)
Base = declarative_base()

class Horse(Base):
    __tablename__ = 'horse'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_pos = Column(Float)

class NamePrefix(Base):
    __tablename__ = 'name_prefix'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class NameSuffix(Base):
    __tablename__ = 'name_suffix'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    money = Column(Float)
    win = Column(Integer)
    lose = Column(Integer)

session = None
def init_db():
    global session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print("initdb session:" + str(session))

def get_session():
    if session is None:
        init_db()
    return session