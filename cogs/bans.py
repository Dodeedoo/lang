import traceback

import discord
from discord.ext import commands
from managers.languagemanager import Language

class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *, reason=None):
        try:
            if user == None:
                msg = await Language(ctx.guild.id).getPhrase("ban", "fail")
                await ctx.send(msg)
            else:
                if reason == None:
                    await user.ban()
                    msg = await Language(ctx.guild.id).getPhrase("ban", "bannednoreason")
                    await ctx.send(str(msg).format(user=user))
                    return
                await user.ban(reason=reason)
                msg = await Language(ctx.guild.id).getPhrase("ban", "banned")
                await ctx.send(str(msg).format(user=user, reason=reason))
        except:
            msg = await Language(ctx.guild.id).getPhrase("error", "error")
            await ctx.send(msg)
            traceback.print_exc()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member = None):
        if member is None:
            msg = await Language(ctx.guild.id).getPhrase("unban", "fail")
            await ctx.channel.send(msg)
            return
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                msg = await Language(ctx.guild.id).getPhrase("unban", "unbanned")
                await ctx.channel.send(str(msg).format(user=user.name))
            else:
                msg = await Language(ctx.guild.id).getPhrase("unban", "notbanned")
                await ctx.channel.send(msg)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")



def setup(bot):
    bot.add_cog(Bans(bot))
