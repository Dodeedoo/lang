import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from managers.languagemanager import db
from data import database

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
    await db.start_databse()

@bot.event
async def on_guild_join(guild):
    if db.session.query(db.session.query(database.Guild.id).filter(database.Guild.id == guild.id).exists()).scalar() is not True:
        db.session.add(database.Guild(id=guild.id, language=os.getenv("DEFAULT_LANGUAGE")))
        db.session.commit()
    else:
        print("Guild already registered " + str(guild.id))

initial_extension = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extension.append(f"cogs.{filename[:-3]}")
if __name__ == "__main__":
    for extension in initial_extension:
        print(extension)
        bot.load_extension(extension)

bot.load_extension("cogs.bans")
bot.load_extension("cogs.kick")
bot.load_extension("cogs.languages")

bot.run(os.getenv("TOKEN"))
