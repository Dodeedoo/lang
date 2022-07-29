import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from data.database import db
from sqlalchemy import Column, Integer, String, Table

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
    #Table("845734294487171124", db.meta, Column('id', Integer, primary_key=True), Column('balance', Integer), Column('inventory', String))
    #db.meta.create_all(db.engine)

@bot.event
async def on_disconnect():
    print("Bot going offline")

initial_extension = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extension.append(f"cogs.{filename[:-3]}")
if __name__ == "__main__":
    for extension in initial_extension:
        print(extension)
        bot.load_extension(extension)
"""
bot.load_extension("cogs.bans")
bot.load_extension("cogs.kick")
bot.load_extension("cogs.languages")
bot.load_extension("cogs.joinevent")
"""

bot.run(os.getenv("TOKEN"))