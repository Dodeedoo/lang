from discord.ext import commands
from main import languages
import json


class Lang(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        ctx.send("hey")

    @commands.command()
    async def language(self, ctx, language=None):
        if language in languages:
            language = language[:2]
            json.dump({"language": language}, open("guilds/" + ctx.guild.id + ".json", "w"))
        else:
            await ctx.send("Invalid Language! please use [English, French, German]")


def setup(bot):
    bot.add_cog(Lang(bot))
