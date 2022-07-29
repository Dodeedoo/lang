import traceback

from discord.ext import commands
import discord
from managers import economymanager
from managers.economymanager import Wallet


class Inventory(commands.Cog):
    @commands.command()
    async def inventory(self, ctx, user: discord.Member = None):
        if user is not None:
            economymanager.check_if_loaded(user.id, ctx.guild.id)
            msg = "inventory of " + user.display_name
            for item in Wallet.users.get(user.id).get_inventory():
                msg = msg + "\n" + item.get_emoji() + " " + item.get_name() + " x" + item.get_amount

            await ctx.send(msg)
        else:
            economymanager.check_if_loaded(ctx.message.author.id, ctx.guild.id)
            msg = "inventory of " + ctx.message.author.display_name
            for item in Wallet.users.get(ctx.message.author.id).get_inventory():
                msg = msg + "\n" + item.get_emoji() + " " + item.get_name() + " x" + item.get_amount

            await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modinventory(self, ctx, user: discord.Member = None, itemid: str = None, action: str = "",
                           amount: int = 1):
        try:
            economymanager.check_if_loaded(user.id, ctx.guild.id)
            inv = Wallet.users.get(user.id)
            inv.set_inventory(economymanager.mod_inventory(inventory=inv.get_inventory(), operation=action, itemid=itemid,
                                                           amount=amount))
        except:
            traceback.print_exc()
            await ctx.send("usage: !modinventory @user itemid add/remove amount")


def setup(bot):
    bot.add_cog(Inventory(bot))
