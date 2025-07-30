import discord
from discord import app_commands
from discord.ext import commands
import requests
import traceback

icon_url = f"https://api.mcsrvstat.us/icon/play.spectralsportsnetwork.com"
MINECRAFT_STATUS_API = 'https://api.mcsrvstat.us/3/play.spectralsportsnetwork.com'
GUILD_ID = 1375249715662164050

class serverInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def server_information(self, interaction: discord.Interaction):
        try:
            r = requests.get(MINECRAFT_STATUS_API, timeout=10)
            data_parsed = r.json()

            if not data_parsed.get('online'):
                await interaction.response.send_message("🔴 The server is currently **down**.", ephemeral=True)
                return

            server_name = data_parsed.get('hostname', 'Unknown')
            port = data_parsed.get('port', 'N/A')
            players = data_parsed.get('players', {}).get('online', 0)
            players_max = data_parsed.get('players', {}).get('max', 0)
            motd = '\n'.join(data_parsed.get('motd', {}).get('clean', [])) or "N/A"

            embed = discord.Embed(                                                              #creates an invisible embedded message (only for user)
                title="MSSN Status",
                description=f"For Java and Bedrock. Check #xyz for more details on how to play\n-------------------------------------------------------------------", 
                color=discord.Color.green())

            embed.set_thumbnail(url=icon_url)
            embed.add_field(name="🌐 IP Address:", value=f"{server_name}:{port}", inline=True)
            embed.add_field(name="🟢 Status:", value="Online", inline=True)
            embed.add_field(name="👥 Players", value=f"`{players} / {players_max}`", inline=True)
            embed.add_field(name="🗓️ Event:", value=motd, inline=False)
            embed.set_footer(text="-----------------------------------------------------------------------------\nSpectral Sports Network")

            await interaction.response.send_message(embed=embed, ephemeral=True)                #sends out the embed message, needs a cooldown or something soon

        except Exception as e:
            traceback_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))                #logging for testing purposes, will be deleted once public
            print(traceback_str)
            await interaction.response.send_message(f"❌ An error occurred:\n```{e}```", ephemeral=True)    #catches exception for user

    async def cog_load(self):
        command = app_commands.Command(
            name="server",
            description="Get Minecraft server info",
            callback=self.server_information)
        self.bot.tree.add_command(command, guild=discord.Object(id=GUILD_ID))               #honestly i had no idea how to sync up /commands on discord, i had to rely on google for this one

async def setup(bot):
    await bot.add_cog(serverInfo(bot))
