import discord
from discord.ext import commands

from managers import economymanager
from managers.economymanager import Wallet


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx, user: discord.Member = None):
        # table = database.create_user_table(ctx.message.author.guild.id)
        if user is not None:
            economymanager.check_if_loaded(user.id, ctx.guild.id)
            await ctx.send("balance: " + str(Wallet.users.get(user.id).get_money()))
        else:
            senderid = ctx.message.author.id
            economymanager.check_if_loaded(senderid, ctx.guild.id)
            await ctx.send("balance: " + str(Wallet.users.get(senderid).get_money()))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addbal(self, ctx, user: discord.Member = None, amount: int = 1000):
        if user is not None:
            economymanager.check_if_loaded(user.id, ctx.guild.id)
            oldbal = Wallet.users.get(user.id).get_money(formatted=False)
            Wallet.users.get(user.id).add(amount)
            await ctx.send("balance of " + str(user) + " " + str(oldbal) + " -> " +
                           str(Wallet.users.get(user.id).get_money(formatted=False)))
        else:
            await ctx.send("Please specify a user!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removebal(self, ctx, user: discord.Member = None, amount: int = 1000):
        if user is not None:
            economymanager.check_if_loaded(user.id, ctx.guild.id)
            oldbal = Wallet.users.get(user.id).get_money(formatted=False)
            Wallet.users.get(user.id).remove(amount)
            await ctx.send("balance of " + str(user) + " " + str(oldbal) + " -> " +
                           str(Wallet.users.get(user.id).get_money(formatted=False)))
        else:
            await ctx.send("Please specify a user!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def operationbal(self, ctx, user: discord.Member = None, amount: int = 1000, operation: str = ""):
        if user is not None:
            economymanager.check_if_loaded(user.id, ctx.guild.id)
            oldbal = Wallet.users.get(user.id).get_money(formatted=False)
            if Wallet.operators.get(operation) is not None:
                Wallet.users.get(user.id).operate(amount, operation)
            else:
                await ctx.send("Invalid operator!! please use [+, -, /, *, **]")
                return
            await ctx.send(str("balance of " + str(user) + " " + str(oldbal) + " -> " +
                           str(Wallet.users.get(user.id).get_money(formatted=False))))
        else:
            await ctx.send("Please specify a user!")


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
