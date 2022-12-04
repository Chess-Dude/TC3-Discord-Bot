import discord, typing, asyncio, datetime
from discord import app_commands
from discord.ext import commands

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
            colour=0x00FF00
        )
        
        success_message = await interaction.channel.send(embed=response_embed)

        log_channel = self.bot.get_channel(1028869177798295632)
        
        log_embed = discord.Embed(
            color=0xff0000, 
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
    
        await log_channel.send(embed=log_embed)

    async def time_type_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        time_type_list = ["minutes", "hours"]
        return [
            app_commands.Choice(name=time_type, value=time_type)
            for time_type in time_type_list if current.lower() in time_type.lower()
        ]

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id))
    @app_commands.command(
        name="mute",
        description="A Command that allows moderators to mute a member")
    @app_commands.describe(member="specify which member to mute")
    @app_commands.describe(duration="specify mute duration")
    @app_commands.autocomplete(time_type=time_type_autocomplete)
    @app_commands.describe(reason="specify reason of mute")
    @app_commands.rename(member="member")
    @app_commands.rename(duration="duration")
    @app_commands.rename(time_type="time_type")
    @app_commands.rename(reason="reason")
    async def mute_command(        
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: int,
        time_type: str,
        reason: str
    ):
        muted_role = interaction.guild.get_role(351091626950787084)

        await member.add_roles(muted_role)
        
        response_embed = discord.Embed(
            description=f"✅ {member.display_name}#{member.discriminator} has been muted for {duration} {time_type} | {reason}", 
            colour=0x00FF00
        )
        
        success_message = await interaction.channel.send(embed=response_embed)

        log_channel = self.bot.get_channel(1028869177798295632)
        
        log_embed = discord.Embed(
            color=0xff0000, 
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
            name="Member Muted",
            value=f"{member.mention}, ``{member.id}``",
            inline=False
        )           

        log_embed.add_field(
            name="Reason Of Mute",
            value=f"``{reason}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Duration Of Mute",
            value=f"``{duration} {time_type}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Jump", 
            value = f"[Go to message!]({success_message.jump_url})",
            inline=False
        )
    
        log_embed_message = await log_channel.send(embed=log_embed)
        
        try:
            await member.send(
                content=f"You have been muted. You may appeal this mute here: https://goo.gl/forms/40zjxwBgD9RaV4Lh1",
                embed=log_embed
            )
        except:
            pass

        time_now = datetime.datetime.now()

        if time_type == "minutes":
            time_duration = datetime.timedelta(minutes=duration)
            duration_seconds = duration * 60


        elif time_type == "hours":
            time_duration = datetime.timedelta(hours=duration)
            duration_seconds = duration * 3600

        unmute_time = time_now + time_duration

        await member.timeout(time_duration)
        await member.add_roles(muted_role)

        await asyncio.sleep(duration_seconds)

        await member.remove_roles(muted_role)

        unmute_log_embed = discord.Embed(
            color=0xff0000, 
            timestamp=interaction.created_at
        )

        unmute_log_embed.set_author(
            name=f"{interaction.guild.name}",
            icon_url=f"{interaction.guild.icon}"
        )

        unmute_log_embed.add_field(
            name="Member Unmuted",
            value=f"{member.mention}, ``{member.id}``",
            inline=False
        )           
                
        await member.send(
            content="You have been unmuted.",
            embed=unmute_log_embed
        )

        unmute_log_embed.add_field(
            name="Jump", 
            value = f"[Go to message!]({log_embed_message.jump_url})",
            inline=False
        )       

        await log_channel.send(embed=unmute_log_embed)

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
        muted_role = interaction.guild.get_role(351091626950787084)
        
        await member.remove_roles(muted_role)
        
        response_embed = discord.Embed(
            description=f"✅ {member.display_name}#{member.discriminator} has been unmuted", 
            colour=0x00FF00
        )
        
        success_message = await interaction.channel.send(embed=response_embed)

        log_channel = self.bot.get_channel(1028869177798295632)
        
        log_embed = discord.Embed(
            color=0xff0000, 
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
            name="Member Unmuted",
            value=f"{member.mention}, ``{member.id}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Jump", 
            value = f"[Go to message!]({success_message.jump_url})",
            inline=False
        )
    
        await log_channel.send(embed=log_embed)
        
        try:
            await member.send(
                content=f"You have been Unmuted.",
                embed=log_embed
            )
        except:
            pass


    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id))
    @app_commands.command(
        name="ban",
        description="A Command that allows moderators to ban a member")
    @app_commands.describe(member="specify which member to ban")
    @app_commands.describe(reason="specify reason of ban")
    @app_commands.rename(member="member")
    @app_commands.rename(reason="reason")
    async def ban_command(        
        self,
        interaction: discord.Interaction,
        member: discord.User,
        reason: str
    ):
        response_embed = discord.Embed(
            description=f"✅ {member.display_name}#{member.discriminator} has been banned | {reason}", 
            colour=0xff0000
        )
        
        success_message = await interaction.channel.send(embed=response_embed)

        log_channel = self.bot.get_channel(1028869177798295632)
        log_embed = discord.Embed(color=0xff0000, timestamp=interaction.created_at)
        
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
            name="Member Banned",
            value=f"{member.mention}, ``{member.id}``",
            inline=False
        )           

        log_embed.add_field(
            name="Reason Of Ban",
            value=f"``{reason}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Jump", 
            value = f"[Go to message!]({success_message.jump_url})",
            inline=False
        )
    
        await log_channel.send(embed=log_embed)

        try:
            await member.send(
                content="You have been banned. You may appeal this ban here: https://goo.gl/forms/40zjxwBgD9RaV4Lh1.",
                embed=log_embed
            )
        except:
            pass

        await interaction.guild.ban(user=member, reason=reason)       

async def setup(bot):
    await bot.add_cog(ModeratorCommands(bot))