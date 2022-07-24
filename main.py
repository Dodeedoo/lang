import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

intents = discord.Intents.default()
intents.members = True
load_dotenv("config.env")

bot = commands.Bot(command_prefix='!', intents=intents)


# starting the bot
@bot.event
async def on_ready():
    print("------------------------------")
    print("Bot is ready to use!")
    print("------------------------------")


@bot.event
async def on_guild_join(guild):
    path = "guilds/" + str(guild.id) + ".json"
    try:
        with open(path, 'w') as outfile:
            json.dump({'language': 'en'}, outfile)
    except FileExistsError:
        print("Guild already registered " + path)


initial_extension = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extension.append(f"cogs.{filename[:-3]}")
if __name__ == "__main__":
    for extension in initial_extension:
        bot.load_extension(extension)

bot.run(os.getenv("TOKEN"))
