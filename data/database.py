import sqlalchemy
from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Guild(Base):
    __tablename__ = "guilds"
    id = Column(Integer, primary_key=True)
    language = Column(String(2))

class DataBase:

    def __init__(self):
        self.session = None
        self.engine = None
        self.conn = None

    async def start_databse(self):
        engine = sqlalchemy.create_engine('sqlite:///guilds.db')
        conn = engine.connect()
        meta = MetaData(engine)
        Table("guilds", meta, Column('id', Integer, primary_key=True), Column('language', String(2)))
        meta.create_all(engine)
        print("databse started")
        self.engine = engine
        self.session = Session(engine)
        self.conn = conn
