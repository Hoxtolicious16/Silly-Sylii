import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print (f'We are ready to go in, {bot.user.name}')



@bot.command()
async def character(ctx):
    await ctx.send(f"Heyo, {ctx.author.mention} As of now I've got: Illari, Pharah, Symmetra, Widowmaker, Mercy, Kiriko, Tracer, Sojourn, Ana. Alcina Dimitrescu, Claire Redfield, Mia Winters, Ashley Graham. Chun-Li, Juri Han, Cammy White. But work's never finished so master's got me workin'")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


#@bot.event
#async def on_member_join(member):
#    await member.send(f'Welcome to the server {member.name}. Here are my socials!/n :underage: NFSW X (Twitter): https://x.com/Sylaellas /n :crown: Patreon: https://www.patreon.com/c/Sylaellas :crown:')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
