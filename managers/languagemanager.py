import json
from sqlalchemy import select
from data import database

db = database.DataBase()


class Language:
    def __init__(self, id):
        self.id = id
        stmt = select(database.Guild).where(database.Guild.id == '845734294487171124')
        self.lang = db.conn.execute(stmt).mappings().all()[0]["language"]

    async def getPhrase(self, command, phrase):
        return json.load(open("languages/" + self.lang + ".json", 'r'))["commands"][command][phrase]
