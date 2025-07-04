import discord
from discord.ext import commands

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member_id: int):
        member = ctx.guild.get_member(member_id)
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot ban nobody/yourself")
            return
        else:
            await ctx.channel.send("No perms")
        await ctx.channel.send(f"{member} is banned!")
        await ctx.guild.ban(member)

async def setup(bot):
    await bot.add_cog(moderation(bot))