import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎Help",
            description=f"‎ ‎ ‎‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎Commands \n❖ —————— ❖ —————— ❖ —————— ❖ —————— ❖ —————— ❖",
            # for anybody seeing this, I'm so sorry for the invisible characters, I just wanted to make the embed look nice and discord doesn't allow spaces in embed titles.
            color=discord.Color.purple())
        embed.set_author(name="✦・Sylaellas・✦", icon_url="https://cdn.discordapp.com/avatars/1380215695651897535/c35aafc14a675a1ed0f57bdcbce7f14e.webp?size=128", url="https://linktr.ee/sylaellas")  # Replace with your bot's avatar URL
        embed.add_field(name=f"```!blackjack``` 🃏", value="Play a game of blackjack.", inline=False)
        embed.add_field(name=f"```!character``` 📝", value="Makes the bot tell you about my Patreon work!", inline=False)
        embed.add_field(name=f"```!seeds``` 🌱", value="Get a list of all available seeds in stock for the Roblox game 'Grow a Garden'.", inline=False)
        embed.set_footer(text="❖ ——————— ❖ ——————— ❖ ——————— ❖ ——————— ❖ ——————— ❖")
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))