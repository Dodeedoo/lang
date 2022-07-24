import json


class Language:
    def __init__(self, id):
        self.id = id
        self.lang = json.load(open("guilds/" + str(self.id) + ".json", "r"))["language"]

    async def getPhrase(self, command, phrase):
        return json.load(open("languages/" + self.lang + ".json", 'r'))["commands"][command][phrase]
