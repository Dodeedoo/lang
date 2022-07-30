import traceback

from discord.ext import commands

from data.database import db
from data import database
from managers import inventorymanager
from managers.economymanager import Wallet


class Market(commands.Cog):
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addmarketitem(self, ctx, name=None, min=None, max=None, price=None, emoji=None):
        inventorymanager.check_if_loaded(ctx.guild.id)
        try:
            inventorymanager.register_item(min=min, max=max, emoji=emoji, price=price, name=name, gid=ctx.guild.id)
            await ctx.send("Registered " + name + " " + emoji)
        except:
            traceback.print_exc()
            await ctx.send("usage: !addmarketitem name min max price emoji")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modmarketitem(self, ctx, name, attribute, newvalue):
        inventorymanager.check_if_loaded(ctx.guild.id)
        try:
            item = inventorymanager.get_item_from_name(name)
            setattr(item, attribute, newvalue)
        except:
            traceback.print_exc()
            await ctx.send("usage: !modmarketitem name attribute[emoji, min, max, name, price] new_value")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deleteitem(self, ctx, name):
        it = inventorymanager.get_item_from_name(name)
        table = database.create_item_table(ctx.guild.id)
        query = db.session.query(table).filter(table.name == name).one()
        query.delete(synchronize_session=False)
        db.session.commit()
        inventorymanager.MarketItem.items.pop(it.id)
        await ctx.send("Deleted " + it.name)

    @commands.command()
    async def listmarket(self, ctx):
        inventorymanager.check_if_loaded(ctx.guild.id)
        await ctx.send(inventorymanager.MarketItem.items)

    @commands.command()
    async def checkprice(self, ctx, name):
        inventorymanager.check_if_loaded(ctx.guild.id)
        try:
            item = inventorymanager.get_item_from_name(name)
            print(item.get_id())
            await ctx.send(
                "Price of " + str(item.get_emoji()) + " " + name + ": " + str(format(item.get_price(), ",")) + "$")
        except:
            traceback.print_exc()
            await ctx.send("ERROR!! Most likely item not found! do !listmarket")

    @commands.command()
    async def sell(self, ctx, name, amount):
        inventorymanager.check_if_loaded(ctx.guild.id)
        try:
            amount = int(amount)
            item = inventorymanager.get_item_from_name(name)
            #invitem = inventorymanager.get_as_invitem(item.get_id(), amount)
            wallet = Wallet.users.get(ctx.message.author.id)
            print(wallet.get_inventory())
            userinvitem = wallet.get_inventory()[item.get_id()]
            userinv = wallet.get_inventory()
            if userinvitem.get_amount() >= int(amount):
                userinvitem.remove(amount)
                money = item.get_price() * amount
                wallet.add(money)
                if userinvitem.get_amount() == 0:
                    userinv.pop(item.get_id())
                    wallet.set_inventory(userinv)
                Wallet.users[ctx.message.author.id] = wallet
                await ctx.send("Sold " + str(amount) + "x " + name + " " + str(userinvitem.get_emoji()))
            else:
                await ctx.send("not enough items in inventory!!!")
        except:
            traceback.print_exc()
            await ctx.send("usage: !sell name amount")

    @commands.command()
    async def buy(self, ctx, name, amount):
        inventorymanager.check_if_loaded(ctx.guild.id)
        try:
            amount = int(amount)
            item = inventorymanager.get_item_from_name(name)
            wallet = Wallet.users.get(ctx.message.author.id)
            print(wallet.get_inventory())
            userinv = wallet.get_inventory()
            try:
                userinvitem = inventorymanager.get_as_invitem(item.get_id(), amount +
                            int(wallet.get_inventory()[item.get_id()].get_amount()))
            except KeyError:
                userinvitem = inventorymanager.get_as_invitem(item.get_id(), amount)
            payment = item.get_price() * amount
            if wallet.get_money() >= payment:
                userinvitem.add(amount)
                wallet.remove(payment)
                userinv[item.get_id()] = userinvitem
                wallet.set_inventory(userinv)
                Wallet.users[ctx.message.author.id] = wallet
                await ctx.send("Bought " + str(amount) + "x " + name + " " + str(userinvitem.get_emoji()))
            else:
                await ctx.send("not enough money!!!")
        except:
            traceback.print_exc()
            await ctx.send("usage: !buy name amount")


def setup(bot):
    bot.add_cog(Market(bot))
