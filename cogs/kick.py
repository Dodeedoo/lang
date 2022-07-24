import discord
from discord.ext import commands
from managers.languagemanager import Language


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        if user is not None:
            if reason is None:
                await user.kick()
                msg = await Language(ctx.guild.id).getPhrase("kick", "kickednoreason")
                await ctx.send(str(msg).format(user=user))
            else:
                await user.kick(reason=reason)
                msg = await Language(ctx.guild.id).getPhrase("kick", "kicked")
                await ctx.send(str(msg).format(user=user, reason=reason))
        else:
            msg = await Language(ctx.guild.id).getPhrase("kick", "fail")
            await ctx.send(msg)

    @commands.command()
    async def hello(self, ctx):
        msg = await Language(ctx.guild.id).getPhrase("hello", "hello")
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Kick(bot))
