import discord
from discord.ext import commands
from discord.utils import get

class TicketLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Suggest something!", style=discord.ButtonStyle.green, custom_id="suggestion_button")
    async def suggestion_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = get(interaction.guild.text_channels, name=f"Commission-for-{interaction.user.name} - {interaction.user.discriminator}")
        if ticket:
            await interaction.response.send_message(
                f"You already suggested something at {ticket.mention}! Give me some time please!",
                ephemeral=True
            )
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            }
            channel = await interaction.guild.create_text_channel(
                name=f"Suggestion-for-{interaction.user.name} - {interaction.user.discriminator}",
                overwrites=overwrites,
                reason=f"Suggestion for {interaction.user}"
            )
            await channel.send(f"{interaction.user.mention} created a suggestion for you <@1255499804838989946>!")
            await channel.send("Don't worry, this conversation is purely between you and Sylaellas")


class SuggestionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="suggestion")
    async def commission_command(self, ctx: commands.Context):
        """Launches a suggestion via button."""
        embed = discord.Embed(
            title="If you need a suggestion, click the button below and create a channel for me to review!",
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed, view=TicketLauncher())

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketLauncher())  # Register persistent view

async def setup(bot: commands.Bot):
    await bot.add_cog(SuggestionCog(bot))
