import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')  #bot logs, ignore doesn't work atm.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')  # Remove the default help command to use our custom one.

@bot.event
async def on_ready():
    for guild in bot.guilds:
        try:
            print(f'Silly Sylii loaded on: {guild.name} ({guild.id})')
        except Exception as e:
            print(f'failed to load on: {guild.name} ({guild.id})')

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
        await bot.start(token)                      #starts bot using the my bots token from the .env file.
asyncio.run(main())                                 #runs the bot.


