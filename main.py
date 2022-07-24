import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
import os
from dotenv import load_dotenv
load_dotenv()

#setting up the prefix
#using intents for the permission
bot = commands.Bot(command_prefix='!',intents = intents)

#starting the bot 
@bot.event
async def on_ready():
    print("------------------------------")
    print("Bot is ready to use!")
    print("------------------------------")


#using cogs for the command handeling
#if any file in cogs folder it will remove .py extension and it will run it.
#it will load all the files in the cogs
initial_extension = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extension.append(f"cogs.{filename[:-3]}")
if __name__ == "__main__":
    for extension in initial_extension:
        bot.load_extension(extension)
print("this has been execute too")
#running the bot thrugh the bot token
bot.run(os.getenv("TOKEN"))