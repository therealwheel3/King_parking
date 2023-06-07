import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String  
import time


Base = declarative_base()
__factory = None
def global_init(db_file):
    global __factory
    if __factory:
        return
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    Base.metadata.create_all(engine)


class Owner(Base):
    __tablename__ = 'owner_data_base'
    id = Column(Integer(), primary_key = True)
    email_adress = Column(String(), nullable =False)
    password = Column(String(), nullable = False)
    created_at = Column(Integer(), nullable=False, default=time.time())
    updated_at = Column(Integer(), nullable=False)


class Parking(Base):
    __tablename__ = 'parking_data_base'
    id = Column(Integer(), primary_key = True)
    name = Column(String(), nullable = False)
    adress = Column(String(), nullable=False)
    cost = Column(Integer(), nullable=False)


class Place(Base):
    __tablename__ = 'place_data_base'
    id = Column(Integer(), primary_key = True)
    name = Column(String(), nullable=False)
    ocupied = Column(Integer(), nullable = False)
    Parking = Column(Integer(), nullable = False)


class Tokens(Base):
    __tablename__ = 'token_data_base'
    parking = Column(Integer(), nullable=False)
    place = Column(Integer(), nullable=False)
    start = Column(Integer(), nullable=False)
    end = Column(Integer(), nullable=False)
    token = Column(String(), nullable=False, primary_key=True)
    condition = Column(String(), nullable=False)

global_init('database.db')