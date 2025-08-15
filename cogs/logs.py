import discord
from discord.ext import commands
import datetime
moderation_channel = 1375874831505166336
max_cache = 5000 # max amount of messages cached

leave_channel = 1385774522719928422
welcome_channel = 1375873182854283448


class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = [] # store messages as lists
    
    @commands.command(name="leave") # test commands
    @commands.has_permissions(view_audit_log=True)
    async def server_leave_test(self, ctx):
        moderation = self.bot.get_channel(moderation_channel)
        embed = discord.Embed(
            title="👋Member Left",
            description=f"<@{ctx.author.id}> has left the server.",
            color=discord.Color.from_rgb(144, 20, 68)
        )
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.add_field(name="User ID", value=ctx.author.id, inline=True)
        embed.add_field(name="Joined at", value=f"<t:{int(ctx.author.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Left at", value=f"<t:{int(datetime.datetime.now().timestamp())}:R>", inline=True)
        embed.set_footer(text="We will (probably not) miss you!")
        await moderation.send(embed=embed)

    @commands.command(name="server_boost") # test commands
    @commands.has_permissions(view_audit_log=True)
    async def server_boost_test(self, ctx):
        moderation = self.bot.get_channel(moderation_channel)
        embed = discord.Embed(
                    title="‎                              ✦・Beloved Booster!・✦ ",
                    description=f"Beloved choom <@{ctx.author.id}> has just boosted the server, massive flex, massive thanks!‎  ‎  🎋",
                    color=discord.Color.from_rgb(144, 20, 68)
                )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1375874831505166336/1406030884976464004/Ruby.png?ex=68a0fbcd&is=689faa4d&hm=470009afd81dd0dd837b632e59b078aec6ef0b94a307728fae25fb5e7611e391&")
        embed.set_image(url="https://preview.redd.it/day-one-tryna-officially-start-zenless-zone-zero-v0-iosk3h7rwkad1.gif?width=498&auto=webp&s=486b6578fe12fe230b489c35e7164151a95ef578")
        await moderation.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        welcome = self.bot.get_channel(welcome_channel)
        booster = after.guild.premium_subscriber_role
        if booster and booster not in before.roles and booster in after.roles:
            embed = discord.Embed(
                title="‎                              ✦・Beloved Booster!・✦ ",
                description=f"Beloved choom <@{after.id}> has just boosted the server, massive flex, massive thanks!‎  ‎  🎋",
                color=discord.Color.from_rgb(144, 20, 68)
                )
        embed.set_author(name=after.name, icon_url=after.avatar.url if after.avatar else None)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1375874831505166336/1406030884976464004/Ruby.png?ex=68a0fbcd&is=689faa4d&hm=470009afd81dd0dd837b632e59b078aec6ef0b94a307728fae25fb5e7611e391&")
        embed.set_image(url="https://preview.redd.it/day-one-tryna-officially-start-zenless-zone-zero-v0-iosk3h7rwkad1.gif?width=498&auto=webp&s=486b6578fe12fe230b489c35e7164151a95ef578")
        await welcome.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        leave = self.bot.get_channel(leave_channel)
        if leave is None:
            print("Log channel not found.")
            return

        embed = discord.Embed(
            title="👋Member Left",
            description=f"<@{member.id}> has left the server.",
            color=discord.Color.from_rgb(144, 20, 68)
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Joined at", value=f"<t:{int(member.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Left at", value=f"<t:{int(datetime.datetime.now().timestamp())}:R>", inline=True)
        embed.set_footer(text="We will (probably not) miss you!")
        await leave.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message :discord.Message):
        if message.author.bot: # if its a message made by a bot
            return

        self.cache.append(message)
        if len(self.cache) > max_cache:
            self.cache.pop(0)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        
        log_channel = self.bot.get_channel(moderation_channel)
        if log_channel is None:
            print("Log channel not found.")
            return

        # check who deleted the message
        async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            delete = entry.user

        # create embedded message
        embed = discord.Embed(
            title="🗑️Message Deleted",
            description=f"Message from <@{message.author.id}> deleted in {message.channel.mention} by <@{delete.id}>",
            color=discord.Color.red()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url if message.author.avatar else None)
        embed.add_field(name="Content", value=message.content or "No content", inline=False)
        if message.attachments:
            embed.add_field(name="Attachments", value=", ".join([f"[{attachment.filename}]({attachment.url})" for attachment in message.attachments]), inline=False)
            embed.set_image(url=message.attachments[0].url)
        embed.add_field(name="User ID", value=message.author.id, inline=True)
        embed.add_field(name="Timestamp", value=f"<t:{int(message.created_at.timestamp())}:R>", inline=True) # timestamp of when it was deleted
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        timestamp = datetime.datetime.now().timestamp() # timestamp of when it was edited
        if before.author.bot:
            return
        if before.content == after.content:
            return
        
        log_channel = self.bot.get_channel(moderation_channel)
        if log_channel is None:
            print("Log channel not found.")
            return
        
        embed = discord.Embed(
            title="✏️Message Edited",
            description=f"Message from <@{before.author.id}> edited in {before.channel.mention}",
            color=discord.Color.yellow()
        )
        embed.set_author(name=before.author.name, icon_url=before.author.avatar.url if before.author.avatar else None)
        embed.add_field(name="Before", value=before.content or "No content", inline=False)
        embed.add_field(name="After", value=after.content or "No content", inline=False)
        if before.attachments:
            embed.add_field(name="Attachments", value=", ".join([f"[{attachment.filename}]({attachment.url})" for attachment in before.attachments]), inline=False)
            embed.set_image(url=before.attachments[0].url)
        embed.add_field(name="Message ID", value=before.id, inline=True)
        embed.add_field(name="Timestamp", value=f"<t:{int(timestamp)}:R>", inline=True) # timestamp of when it was edited
        await log_channel.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(logs(bot))
