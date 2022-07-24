from discord.ext import commands
from managers.languagemanager import Language
import json

languages = ["english", "french", "german"]

class Lang(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("hey")

    @commands.command()
    async def language(self, ctx, language=None):
        if str(language).lower() in languages:
            msg = await Language(ctx.guild.id).getPhrase("language", "success")
            await ctx.send(msg + language)
            language = language[:2]
            json.dump({"language": language}, open("guilds/" + str(ctx.guild.id) + ".json", "w"))
        else:
            msg = await Language(ctx.guild.id).getPhrase("language", "fail")
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Lang(bot))
