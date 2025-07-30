import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD_ID = 1375249715662164050 # hard coded guild id as of now, will be customizeable in the future (maybe)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')  #bot logs, ignore doesn't work atm.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))   #1 command works as of right now, /server for MSSN but its still in testing not prod

async def load():
    for filename in os.listdir('./cogs'):           #loads all the cogs for the functions to work.
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename[:-3]}: {e}')

async def main():
    async with bot:
        await load()
        await bot.start(token)              #starts bot using the my bots token from the .env file.
asyncio.run(main())         #runs the bot.


