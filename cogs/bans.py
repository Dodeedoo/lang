import discord 
from discord.ext import commands

class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, user: discord.Member, *, reason = None):
        if not reason:
            await user.ban()
            await ctx.send(f"**{user}** has been banned permanently for **no reason**.")
        elif not user:
            await ctx.send("please clarify which user to ban!")
        else:
            await user.ban(reason=reason)
            await ctx.send(f"**{user}** has been banned for **{reason}**.")
    @ban.error
    async def ban_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You dont have Permission to ban the User")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"{user.mention} has been unbanned successfully!")
        else:
            await ctx.channel.send("Not a Proper Way to Unban ```!unban Gotcha#3080```")
    @unban.error
    async def unban_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You dont have Permission to Unban the User")
    

    @commands.command()
    async def ping(self,ctx):
        await ctx.send("Pong!")



def setup(bot):
    bot.add_cog(Bans(bot))