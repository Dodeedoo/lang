import discord
from discord.ext import commands


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        if user is not None:
            if reason is not None:
                await user.kick()
                await ctx.send(f"**{user}** has been kicked for **no reason**.")
            else:
                await user.kick(reason=reason)
                await ctx.send(f"**{user}** has been kicked for **{reason}**.")
        else:
            await ctx.send("Please specify a user!")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello! my name is Guz Bot.")


def setup(bot):
    bot.add_cog(Kick(bot))