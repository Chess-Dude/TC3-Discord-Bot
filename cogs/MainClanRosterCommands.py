import discord
from discord import app_commands
from discord.ext import commands
from .clanClasses.clanRosterClasses.GenerateClanRoster import GenerateClanRoster

class ClanRosterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    update_group = app_commands.Group(
        name="update", 
        description="A Group Of Commands That Allows You To Manage Server Channels!",
        guild_ids=[350068992045744141]
    )

    roster_group = app_commands.Group(
        name="rosters", 
        parent=update_group, 
        description="A Command That Allows You To Create A Channel!"
    )

    @app_commands.checks.has_any_role(554152645192056842, 743302990001340559, 351074813055336458)
    @roster_group.command(
        name="clan",
        description="A Command That Allows You To Update Clan Rosters!")
    async def update_rosters_clan(        
        self,
        interaction: discord.Interaction,
    ):
        generate_clan_roster_obj = GenerateClanRoster()
        
        await generate_clan_roster_obj.purge_channel_messages(
            interaction=interaction
        )

        clan_list = generate_clan_roster_obj.get_clans(
            interaction=interaction
        )

        for clan_role in clan_list:
            if clan_role != None:
                clan_info_list = generate_clan_roster_obj.get_clan_info(
                    interaction=interaction,
                    clan_role=clan_role
                )

                clan_roster_embed = await generate_clan_roster_obj.send_clan_roster(
                    interaction=interaction,
                    clan_role=clan_role,
                    clan_info_list=clan_info_list
                )

                clan_roster_channel = interaction.guild.get_channel(1101934520212656158)

                await clan_roster_channel.send(
                    embed=clan_roster_embed
                )

                await generate_clan_roster_obj.clan_disband_check(
                    interaction=interaction,
                    clan_role=clan_role
                )

async def setup(bot):
    await bot.add_cog(ClanRosterCommands(bot))