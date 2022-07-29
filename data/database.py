import sqlalchemy
from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Guild(Base):
    __tablename__ = "guilds"
    id = Column(Integer, primary_key=True)
    language = Column(String(2))


def create_user_table(name):
    return type(str(name), (Base, ), {
        "__tablename__": str(name),
        "__table_args__": {'extend_existing': True},
        "id": Column(Integer, primary_key=True),
        "balance": Column(Integer),
        "inventory": Column(String)
    })


class DataBase:

    def __init__(self):
        self.session = None
        self.engine = None
        self.conn = None
        self.meta = None

    async def start_databse(self):
        engine = sqlalchemy.create_engine('sqlite:///guilds.db')
        conn = engine.connect()
        meta = MetaData(engine)
        Table("guilds", meta, Column('id', Integer, primary_key=True), Column('language', String(2)))
        meta.create_all(engine)
        print("databse started")
        self.engine = engine
        self.session = Session(engine)
        self.meta = meta
        self.conn = conn


db = DataBase()
