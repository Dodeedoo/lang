from discord.ext import commands, tasks


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def loop(self):
        print("updating db...")

    @tasks.loop(hours=6)
    async def clear_users(self):
        print("loaded users cleared")


def setup(bot):
    bot.add_cog(Tasks(bot))
