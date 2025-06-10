import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()
token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=1375249715662164050))
    print (f'We are ready to go in, {bot.user.name}')

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename[:-3]}: {e}')

async def main():
    async with bot:
        await load()
        await bot.start(token)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def bum(ctx):
    await ctx.send(f"ong <@{1255499804838989946}> a bummy ahh fella. Tell em cuzzo {ctx.author.mention}!")

#@bot.event
#async def on_member_join(member):
#    await member.send(f'Welcome to the server {member.name}. Here are my socials!/n :underage: NFSW X (Twitter): https://x.com/Sylaellas /n :crown: Patreon: https://www.patreon.com/c/Sylaellas :crown:')
asyncio.run(main())
