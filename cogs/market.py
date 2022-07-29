import traceback

from discord.ext import commands

from managers import inventorymanager


class Market(commands.Cog):
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addmarketitem(self, ctx, name=None, min=None, max=None, price=None, emoji=None):
        try:
            inventorymanager.register_item(min=min, max=max, emoji=emoji, price=price, name=name, gid=ctx.guild.id)
        except:
            traceback.print_exc()
            await ctx.send("usage: !addmarketitem name min max price emoji")

    @commands.command()
    async def listmarket(self, ctx):
        await ctx.send(inventorymanager.MarketItem.items)

def setup(bot):
    bot.add_cog(Market(bot))