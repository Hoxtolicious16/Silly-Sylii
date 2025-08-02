import discord
from discord.ext import commands

charnames=["char",'chars','models','caracters','characters','3d','3D','caracter','overwatch','Overwatch','list','List','model','Models','Char','Chars','Caracters','Characters']
class character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "character", aliases=charnames)
    async def character_command(self,ctx):
        await ctx.send(f"Heyo, {ctx.author.mention} As of now I've got: Illari, Pharah, Symmetra, Widowmaker, Mercy, Kiriko, Tracer, Sojourn, Ana. Alcina Dimitrescu, Claire Redfield, Mia Winters, Ashley Graham. Chun-Li, Juri Han, Cammy White. But work's never finished so master's got me workin'",delete_after=60)
        await ctx.message.delete()
async def setup(bot):
    await bot.add_cog(character(bot))