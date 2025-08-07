import discord, asyncio, typing
from discord import app_commands
from discord.ext import commands
from .moderationClasses.muteClasses.muteUtility import MuteUtility

class ModeratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.guild_id))
    @app_commands.command(
        name="purge",
        description="A Command that allows moderators to purge the chat!")
    @app_commands.describe(count="specify how many messages to purge")
    @app_commands.rename(count="count")
    async def purge_command(        
        self,
        interaction: discord.Interaction,
        count: int,
    ):
        await interaction.channel.purge(limit=count)
        
        response_embed = discord.Embed(
            description=f"✅ {count} Messages Have Been Purged!", 
            colour=0x00ffff
        )
        
        success_message = await interaction.channel.send(embed=response_embed)
     
        log_embed = discord.Embed(
            color=0x00ffff, 
            timestamp=interaction.created_at
        )
        
        log_embed.set_author(
            name=f"{interaction.guild.name}",
            icon_url=f"{interaction.guild.icon}"
        )

        log_embed.add_field(
            name="Moderator",
            value=f"{interaction.user.mention}, ``{interaction.user.id}``",
            inline=False
        )
        
        log_embed.add_field(
            name="Number of messages deleted",
            value=f"{count}",
            inline=False
        )           
        
        log_embed.add_field(
            name="Channel",
            value=f"{interaction.channel.mention}",
            inline=False
        )

        log_embed.add_field(
            name="Jump", 
            value = f"[Go to message!]({success_message.jump_url})",
            inline=False
        )

        if self.interaction.guild.id == 350068992045744141:
            log_channel = self.bot.get_channel(1028869177798295632)
            await log_channel.send(embed=log_embed)

    perm_mute_command_group = app_commands.Group(
        name="perm", 
        description="A Command That Allows You To Perma Mute a Member!"
    )

    @app_commands.checks.has_permissions(manage_messages=True)
    @perm_mute_command_group.command(
        name="mute",
        description="A Command that allows moderators to mute a member permanently")
    @app_commands.describe(member="specify which member to mute")
    @app_commands.describe(reason="specify reason of mute")
    @app_commands.rename(member="member")
    @app_commands.rename(reason="reason")
    async def perma_mute_command(        
        self,
        interaction: discord.Interaction,
        member: discord.User,
        reason: typing.Optional[str]       
    ):
        mute_utility_obj = MuteUtility(
            member=member,
            duration=None,
            interaction=interaction,
            time_type=None,
            reason=reason
        )

        if not await mute_utility_obj.is_staff():
            duration_seconds = await mute_utility_obj.mute_user()

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id))
    @app_commands.command(
        name="unmute",
        description="A Command that allows moderators to mute a member")
    @app_commands.describe(member="specify which member to unmute")
    @app_commands.rename(member="member")
    async def unmute_command(        
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        mute_utility_obj = MuteUtility(
            member=member,
            duration=None,
            interaction=interaction,
            time_type=None,
            reason=None
        )

        await interaction.response.send_message(content=f"Unmuted {member.mention}", ephemeral=True)

        await mute_utility_obj.unmute_user()

async def setup(bot):
    await bot.add_cog(ModeratorCommands(bot))