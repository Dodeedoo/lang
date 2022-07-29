import discord
from discord.ext import commands

from managers import economymanager


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx, user: discord.Member = None):
        #table = database.create_user_table(ctx.message.author.guild.id)
        if user is not None:
            if economymanager.Wallet.users.get(user.id) is None:
                economymanager.load_user(user.id)
            await ctx.send("balance: " + str(economymanager.Wallet.users.get(user.id).get_money()))
        else:
            senderid = ctx.message.author.id
            if economymanager.Wallet.users.get(senderid) is None:
                economymanager.load_user(senderid)
            await ctx.send("balance: " + str(economymanager.Wallet.users.get(senderid).get_money()))


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addbal(self, ctx, user: discord.Member, amount: int):
        print("e")

def setup(bot):
    bot.add_cog(Balance(bot))

"""
ids = db.session.query(table).filter(
                table.id == user.id
            ).one()
     for user in db.session.query(table).all():
        print("e")
        print(user.id)
"""
