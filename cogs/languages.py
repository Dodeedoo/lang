from discord.ext import commands
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
            await ctx.send("switched to " + language)
            language = language[:2]
            json.dump({"language": language}, open("guilds/" + str(ctx.guild.id) + ".json", "w"))
        else:
            await ctx.send("Invalid Language! please use [English, French, German]")


def setup(bot):
    bot.add_cog(Lang(bot))
