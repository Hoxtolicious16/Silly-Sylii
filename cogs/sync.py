import discord
from discord import app_commands
from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @app_commands.command(name='sync', description='Synch slash commands globally') #to make sure /commands are useable on other servers
    @app_commands.checks.has_permissions(administrator=True)
    async def sync_commands(self, interaction: discord.Interaction):
        if interaction.user.id == 299952743064403969:                               # only if the owner of the bot runs this command.
            try:
                await self.bot.tree.sync()                                          #syncs commands
                await interaction.response.send_message('✅ Synched commands globally',delete_after=10)
            except Exception as e:
                await interaction.response.send_message(f'❌ Sync failed: \n```{e}```',ephemeral=True)
        else:
            await interaction.response.send_message('❌You are not the owner!',ephemeral=True)

async def setup(bot):
    await bot.add_cog(Sync(bot))