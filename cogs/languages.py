from discord.ext import commands
from managers.languagemanager import Language
from data import database
from data.database import db

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
            guild = db.session.query(database.Guild).filter(
                database.Guild.id == int(ctx.guild.id)
            ).one()
            guild.language = language
            db.session.commit()
        else:
            msg = await Language(ctx.guild.id).getPhrase("language", "fail")
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Lang(bot))
