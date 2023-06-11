import discord, typing
from discord import app_commands
from discord.ext import commands
from cogs.mapSelectionCommands import AppCommandsMapSelection

class ChannelUtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    channel_command_group = app_commands.Group(
        name="channel", 
        description="A Group Of Commands That Allows You To Manage Server Channels!",
        guild_ids=[350068992045744141]
    )

    create_command_group = app_commands.Group(
        name="create", 
        parent=channel_command_group, 
        description="A Command That Allows You To Create A Channel!"
    )
    
    delete_command_group = app_commands.Group(
        name="delete", 
        parent=channel_command_group, 
        description="A Command That Allows You To Delete A Channel!"
    )

    @app_commands.checks.has_any_role(554152645192056842, 743302990001340559, 351074813055336458)
    @create_command_group.command(
        name="game_night",
        description="A Command That Allows You To Create A Server Channel!")
    @app_commands.describe(role_1="P1`ing a role to be added to the channel here!")
    @app_commands.describe(role_2="Ping a role to be added to the channel here!")
    @app_commands.rename(role_1="role_1")
    @app_commands.rename(role_2="role_2")
    async def channel_create_game_night(        
        self,
        interaction: discord.Interaction,
        role_1: discord.Role,
        role_2: typing.Optional[discord.Role]
    ):
        ec_role = interaction.guild.get_role(475669961990471680)
        mod_role = interaction.guild.get_role(351166789700550679)
        mit_role = interaction.guild.get_role(363125947635073025)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            role_1: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            role_2: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ec_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            mod_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            mit_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }

        category = discord.utils.get(
            interaction.guild.categories, 
            id=695665409361182861
        )

        new_channel = await interaction.guild.create_text_channel(
            name=f"{role_1.name}-vs-{role_2.name}", 
            overwrites=overwrites, 
            category=category
        )

        await interaction.response.send_message(f"created {new_channel.mention}")
        await new_channel.send(f"{role_1.mention} vs {role_2.mention} Please Join the lobby and create a party. Here is the map you will play:")
        
        map_embed = AppCommandsMapSelection.random_map_init(
            self=self,
            interaction=interaction,
            game_mode="game_night_3v3"
        )
        await new_channel.send(embed=map_embed)

    @app_commands.checks.has_any_role(554152645192056842, 351074813055336458)
    @create_command_group.command(
        name="contest",
        description="A Command That Allows You To Create A Contest Channel!")
    @app_commands.describe(channel_name="Put the channel name here!")
    @app_commands.rename(channel_name="channel_name")
    async def channel_create_contest(        
        self,
        interaction: discord.Interaction,
        channel_name: str
    ):
        EC_ROLE = interaction.guild.get_role(475669961990471680)
        MOD_ROLE = interaction.guild.get_role(351166789700550679)
        MIT_ROLE = interaction.guild.get_role(363125947635073025)
        CONQUEROR_ROLE = interaction.guild.get_role(365244875861393408)
        MUTED_ROLE = interaction.guild.get_role(351091626950787084)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            MUTED_ROLE: discord.PermissionOverwrite(view_channel=True, manage_channels=False, manage_permissions=False, manage_webhooks=False, send_messages=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False, embed_links=False, attach_files=False, add_reactions=False, use_external_emojis=False, use_external_stickers=False, mention_everyone=False, manage_messages=False, manage_threads=False, read_message_history=True, send_tts_messages=False, use_application_commands=False),
            CONQUEROR_ROLE: discord.PermissionOverwrite(view_channel=True, manage_channels=False, manage_permissions=False, manage_webhooks=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False, embed_links=True, attach_files=True, add_reactions=False, use_external_emojis=False, use_external_stickers=False, mention_everyone=False, manage_messages=False, manage_threads=False, read_message_history=True, send_tts_messages=False, use_application_commands=False), # left send_messages=UNSPECIFIED due to discord perms, 
            EC_ROLE: discord.PermissionOverwrite(view_channel=True, manage_channels=False, manage_permissions=False, manage_webhooks=False, send_messages=True, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False, embed_links=True, attach_files=True, add_reactions=True, use_external_emojis=True, use_external_stickers=False, mention_everyone=False, manage_messages=False, manage_threads=False, read_message_history=True, send_tts_messages=False, use_application_commands=False),
            MOD_ROLE: discord.PermissionOverwrite(view_channel=True, manage_channels=False, manage_permissions=False, manage_webhooks=False, send_messages=True, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False, embed_links=True, attach_files=True, add_reactions=False, use_external_emojis=False, use_external_stickers=False, mention_everyone=False, manage_messages=True, manage_threads=True, read_message_history=True, send_tts_messages=False, use_application_commands=True),
            MIT_ROLE: discord.PermissionOverwrite(view_channel=True, manage_channels=False, manage_permissions=False, manage_webhooks=False, send_messages=True, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False, embed_links=True, attach_files=True, add_reactions=False, use_external_emojis=False, use_external_stickers=False, mention_everyone=False, manage_messages=True, manage_threads=True, read_message_history=True, send_tts_messages=False, use_application_commands=True)
        }

        category = discord.utils.get(
            interaction.guild.categories, 
            id=684145320372076583
        )

        new_channel = await interaction.guild.create_text_channel(
            name=f"{channel_name}", 
            overwrites=overwrites, 
            category=category
        )

        await interaction.response.send_message(f"created {new_channel.mention}")
        warning_message = await new_channel.send(f"<:octagonal_sign:1047306960657199114> **__REMINDER__** that talking in this channel will result in a __10 minute mute__ <:octagonal_sign:1047306960657199114>")
        await warning_message.pin(reason="Pins the '<:octagonal_sign:1047306960657199114> **__REMINDER__** that talking in this channel will result in a __10 minute mute__ <:octagonal_sign:1047306960657199114>' message")

    @app_commands.checks.has_permissions(administrator=True)
    @delete_command_group.command(
        name="admin_delete",
        description="A Command That Allows You To Delete A Server Channel!")
    @app_commands.describe(channel_1="mention a channel to be deleted")
    @app_commands.describe(channel_2="mention a channel to be deleted")
    @app_commands.describe(channel_3="mention a channel to be deleted")
    @app_commands.describe(channel_4="mention a channel to be deleted")
    @app_commands.describe(channel_5="mention a channel to be deleted")            
    @app_commands.rename(channel_1="channel_1")
    @app_commands.rename(channel_2="channel_2")
    @app_commands.rename(channel_3="channel_3")
    @app_commands.rename(channel_4="channel_4")
    @app_commands.rename(channel_5="channel_5")            
    async def channel_admin_delete(
        self,
        interaction: discord.Interaction,
        channel_1: discord.TextChannel,
        channel_2: typing.Optional[discord.TextChannel],
        channel_3: typing.Optional[discord.TextChannel],
        channel_4: typing.Optional[discord.TextChannel],
        channel_5: typing.Optional[discord.TextChannel]         
    ): 
        channel_list = [channel_1, channel_2, channel_3, channel_4, channel_5]
        for channel in channel_list: 
            if channel != None:
                await channel.delete()
            else:
                break
        
        await interaction.response.send_message("All channels deleted successfully!")


    @app_commands.checks.has_any_role(554152645192056842, 351074813055336458)
    @delete_command_group.command(
        name="contest",
        description="A Command That Allows You To Delete A Server Channel!")
    @app_commands.describe(channel_1="mention a channel to be deleted")
    @app_commands.describe(channel_2="mention a channel to be deleted")
    @app_commands.describe(channel_3="mention a channel to be deleted")
    @app_commands.describe(channel_4="mention a channel to be deleted")
    @app_commands.describe(channel_5="mention a channel to be deleted")            
    @app_commands.rename(channel_1="channel_1")
    @app_commands.rename(channel_2="channel_2")
    @app_commands.rename(channel_3="channel_3")
    @app_commands.rename(channel_4="channel_4")
    @app_commands.rename(channel_5="channel_5")            
    async def channel_delete_contest(
        self,
        interaction: discord.Interaction,
        channel_1: discord.TextChannel,
        channel_2: typing.Optional[discord.TextChannel],
        channel_3: typing.Optional[discord.TextChannel],
        channel_4: typing.Optional[discord.TextChannel],
        channel_5: typing.Optional[discord.TextChannel]         
    ): 
        channel_list = [channel_1, channel_2, channel_3, channel_4, channel_5]
        contest_category = discord.utils.get(
            interaction.guild.categories, 
            id=684145320372076583
        )        
        for channel in channel_list: 
            if channel != None:
                if channel.category == contest_category:  
                    await channel.delete()
                
                else:
                    await interaction.channel.send(f"Could not delete {channel} as it does not belong in the 'weekly contests' category.")
            else:
                break
        
        await interaction.response.send_message("All channels deleted successfully!")
async def setup(bot):
    await bot.add_cog(ChannelUtilityCommands(bot))