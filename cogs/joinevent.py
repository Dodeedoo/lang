from discord.ext import commands
from data import database
from data.database import db
from sqlalchemy import Table, Column, Integer, String
import os


class Joinevent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db.session.add(database.create_user_table(member.guild.id)(id=member.id, balance=0, inventory=''))
        db.session.commit()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if db.session.query(db.session.query(database.Guild.id).filter(database.Guild.id == guild.id).exists()).scalar() is not True:
            db.session.add(database.Guild(id=guild.id, language=os.getenv("DEFAULT_LANGUAGE")))
            meta = db.meta
            Table(guild.id, meta, Column('id', Integer, primary_key=True), Column('balance', Integer), Column('inventory', String))
            meta.create_all(db.engine)
            db.session.commit()
        else:
            print("Guild already registered " + str(guild.id))

        #registering all members
        members = guild.members
        for member in members:
            db.session.add(database.create_user_table(guild.id)(id=member.id, balance=0, inventory=''))

        db.session.commit()

    @commands.command()
    async def register(self, ctx):
        guild = ctx.guild
        if db.session.query(db.session.query(database.Guild.id).filter(database.Guild.id == guild.id).exists()).scalar() is not True:
            db.session.add(database.Guild(id=guild.id, language=os.getenv("DEFAULT_LANGUAGE")))
            meta = db.meta
            Table(guild.id, meta, Column('id', Integer, primary_key=True), Column('balance', Integer), Column('inventory', String))
            meta.create_all(db.engine)
            db.session.commit()
        else:
            print("Guild already registered " + str(guild.id))

        #registering all members
        members = guild.members
        for member in members:
            db.session.add(database.create_user_table(guild.id)(id=int(member.id), balance=0, inventory=''))

        db.session.commit()

        await ctx.send("registration " + "successful")


def setup(bot):
    bot.add_cog(Joinevent(bot))
