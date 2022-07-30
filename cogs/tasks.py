import random

from discord.ext import commands, tasks
from managers.economymanager import Wallet
from managers import economymanager
from managers.inventorymanager import MarketItem
from managers import inventorymanager


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def loop(self):
        print("updating db...")
        for item in Wallet.users:
            id = item
            item = Wallet.users.get(id)
            economymanager.update_db_user(item, id)

        for item in MarketItem.items:
            id = item
            item = MarketItem.items[id]
            inventorymanager.update_db_item(item, id)

    @tasks.loop(hours=6)
    async def clear_users(self):
        Wallet.users = {}
        print("loaded users cleared")

    @tasks.loop(minutes=2)
    async def price_change(self):
        items = MarketItem.items
        #range = max - min
        #50% chance to increase or decrease
        #increase is in random number between 0 and range/4
        for item in items:
            id = item
            item = items[id]
            range = items.get_max() - items.get_min()
            if random.choice([0, 1]) == 1:
                inc = True
            else:
                inc = False

            amount = random.choice([0, range / 3])

            if inc:
                item.set_price(item.get_price() + amount)
                items[id] = item
            else:
                item.set_price(item.get_price() - amount)
                items[id] = item

    @commands.Cog.listener()
    async def on_ready(self):
        self.loop.start()
        self.clear_users.start()
        self.price_change.start()





def setup(bot):
    bot.add_cog(Tasks(bot))
