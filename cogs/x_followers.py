import discord
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
import os
import http.client
from datetime import datetime, timezone
import json
import math

Start_name = '@Sylaellas' # at the moment it's only set to this twitter account, in the future it will be setable using !setup and gather information of that exact twitter @ for the API

moderation_channel_id = 1380217539065282663 # used to send in channels for moderators only. Will be changed to make it setable to something else using !setup

load_dotenv()
API_KEY = os.getenv('TWITTER_API') # limited to 500 calls a month

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "twitter154.p.rapidapi.com"
}


class twitter_scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_channel_name.start()

    def get_follower_count(self):
        try:
            conn = http.client.HTTPSConnection("twitter154.p.rapidapi.com")
            conn.request("GET", "/user/details?username=sylaellas&user_id=44196397", headers=headers)  # username will use a variable set by the user for the API call in the future
            res = conn.getresponse()
            data = res.read()
            json_data = json.loads(data)
            return json_data['follower_count'] # only wanted data atm is follower count.
        except Exception as e:
            print("API Error:", e)
            return None
        
    def format_number(self, n):
        if n >= 1_000_000:
            value = math.floor(n / 100_000) / 10  # 2.87M → 2.8M followers
            return f"{value}M"
        elif n >= 1_000:
            value = math.floor(n / 100) / 10  # 16,499 → 16.4K followers
            return f"{value}K"
        else:
            return str(n)
        
    async def update_channel_now(self, guild): #force update API call, needs a cooldown to avoid API call abuse
        voice_channel = discord.utils.find(lambda c: Start_name in c.name, guild.voice_channels)
        if voice_channel:
            followers = self.get_follower_count()
            if followers:
                formatted = self.format_number(followers) # formatted follower count
                new_name = f"✦ {Start_name} {formatted} ✦"
                try:
                    await voice_channel.edit(name=new_name)
                    mod_channel = guild.get_channel(moderation_channel_id)
                    if mod_channel:
                        await mod_channel.send(f"✅ Force updated follower counter {new_name} at {datetime.now()}")
                except Exception as e:
                    print("Immediate update failed:", e)

    @tasks.loop(hours=24)                       #Called to once a day to reduce the amount of calls. Will be lowered or made higher depending on the future use of the bot.
    async def update_channel_name(self):
        for guild in self.bot.guilds:
            voice_channel = discord.utils.find(lambda c: Start_name in c.name, guild.voice_channels)
            if voice_channel:
                followers = self.get_follower_count()
                if followers:
                    formatted = self.format_number(followers)
                    new_name = f"✦ {Start_name} {formatted} ✦"
                    try:
                        await voice_channel.edit(name=new_name)
                        mod_channel = guild.get_channel(moderation_channel_id)
                        if mod_channel:
                            await mod_channel.send(f"🔄 Auto-updated follower count to {new_name} at {datetime.now()}") # auto updates every 24 hours.
                    except Exception as e:
                        print("Error editing channel name:", e)

    @commands.command(name='update') # force update command
    @commands.has_role('The Snost & Lost') # will be changed to has permissions to make it more customizeable later
    async def update(self,ctx):
        guild = ctx.guild
        await self.update_channel_now(guild)

    @commands.command(name='setup') # used to create the channel and in the future to set up important variables such as twitter @ and moderation channel.
    @commands.has_role('The Snost & Lost')
    async def setup(self, ctx):
        guild = ctx.guild
        existing_channel = get(guild.voice_channels, name=Start_name)
        if not existing_channel:
            await guild.create_voice_channel(Start_name)
            await ctx.send(f"🎉 Created voice channel '{Start_name}'")
        await self.update_channel_now(guild)


async def setup(bot):
    await bot.add_cog(twitter_scraper(bot))
