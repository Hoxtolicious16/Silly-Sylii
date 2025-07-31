import discord
from discord.ext import commands, tasks
import aiohttp
import os
from datetime import datetime, timezone

STOCK_API_URL = "https://api.joshlei.com/v2/growagarden/stock" #thanks joshlei for the public api :)
CHANNEL_ID = 1380217539065282663 #hardcoded to my the current channel ID of the discord server, will be able to be changed later on. 
JSTUDIO_KEY = os.getenv('JSTUDIO_KEY')

def format_duration(sec: float) -> str:
        m = int(sec // 60)
        s = int(sec % 60)
        return f"{m}m {s}s"

class SeedChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_seed_time = 0
        self.check_seeds.start()

    def cog_unload(self):
        self.check_seeds.cancel()

    @tasks.loop(minutes=5)
    async def check_seeds(self):
        pass


    
    @commands.command(name="seeds")
    async def seeds_command(self, ctx):
        headers = {
            'jstudio-key': JSTUDIO_KEY
        }

        async with aiohttp.ClientSession(headers=headers) as session:
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

        names = "\n".join(f"{i.get(f'display_name','Unknown')} : {i.get('quantity', 0)}" for i in items)
        end_ts = max(i.get("end_date_unix",   0) for i in items)
        
        embed = discord.Embed(
            title="🌿 Current Seed Stock",
            description=names,
            color=discord.Color.green()
        )
        embed.set_footer(text="Grow a Garden")
        embed.timestamp = datetime.now(timezone.utc)
        remaining = max(0, end_ts - datetime.now(timezone.utc).timestamp()) # calculates the Time remaining until the seed stock expires from the API 
        embed.add_field(name='Ends in:', value =f"<t:{end_ts}:R>", inline=True) # unix timestamp at the bottom of the embed file
        await ctx.send(embed=embed, delete_after = remaining) # deletes the message after remaining time has been reached.
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(SeedChecker(bot))