import discord
from discord.ext import commands, tasks
import aiohttp
from datetime import datetime, timezone

STOCK_API_URL = "https://api.joshlei.com/v2/growagarden/stock" #thanks joshlei for the public api :)
CHANNEL_ID = 1380217539065282663 #hardcoded to my the current channel ID of the discord server, will be able to be changed later on. 

class SeedChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_seed_time = 0
        self.check_seeds.start()

    def cog_unload(self):
        self.check_seeds.cancel()

    @commands.command(name="seeds")
    async def seeds_command(self, ctx):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(STOCK_API_URL) as r:
                    if r.status != 200:
                        await ctx.send("❌ Failed to fetch seeds.")
                        return
                    raw_data = await r.json()
            except Exception as e:
                await ctx.send(f"❌ API error: {e}")
                return

        stock = raw_data[0] if isinstance(raw_data, list) else raw_data

        items = stock.get("seed_stock", [])
        if not items:
            await ctx.send("🌱 No seed stock available right now.")
            return

        names = "\n".join(i.get(f"display_name","quantity") for i in items)
        embed = discord.Embed(
            title="🌿 Current Seed Stock",
            description=names,
            color=discord.Color.green()
        )
        embed.set_footer(text="Grow a Garden")
        embed.timestamp = datetime.now(timezone.utc)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SeedChecker(bot))