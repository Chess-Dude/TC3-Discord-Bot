import discord, typing
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from .teamApplicationClasses.teamCreation import TeamCreation
from .clanClasses.clanApplicationClasses.roleCreation import RoleCreation
from .clanClasses.clanApplicationClasses.clanCreationMethods import ClanCreationMethods
from .clanClasses.clanApplicationClasses.clanChangeMethods import ClanChangesMethods

class TournamentApplicationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots_or_work_channel(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 896440473659519057 or ctx.channel.id == 351057167706619914 or ctx.channel.id == 442447501325369345

    group = app_commands.Group(
        name="tournament", 
        description="A Command That Allows You To Submit A Tournament Application!",
        guild_ids=[350068992045744141])
    
    sub_group = app_commands.Group(
        name="application", 
        parent=group, 
        description="A Command That Allows You To Submit A Tournament Application!")
    
    @app_commands.check(bots_or_work_channel)
    @sub_group.command(
        name="1v1",
        description="A Command That Allows You To Submit A 1v1 Tournament Application!")
    async def _1v1_application(        
        self,
        interaction: discord.Interaction,
    ):
        team_roster = [interaction.user]
        
        all_members_verified = await TeamCreation.check_verified(
            self,
            interaction=interaction, 
            team_roster=team_roster
        )

        if all_members_verified:

            await TeamCreation.application_log_embed(
                self,
                interaction=interaction,
                team_name=None,
                tournament_type="1v1",
                team_roster=team_roster
            )

            await TeamCreation.success_embed(
                self,
                interaction=interaction,
                description=f"{interaction.user.mention} Thank You For Submitting Your 1v1 Application!"
            )


    @app_commands.check(bots_or_work_channel)
    @sub_group.command(
        name="2v2",
        description="A Command That Allows You To Submit A 2v2 Tournament Application!")
    @app_commands.describe(team_captain="Ping Your Team Captain Here!")
    @app_commands.describe(team_member_1="Ping Your 1st Team Member Here!")
    @app_commands.describe(team_member_2="Ping Your 2nd Team Member Here!")
    @app_commands.describe(team_member_3="Ping Your 3rd Team Member Here!")
    @app_commands.rename(team_captain="2v2_team_captain")
    @app_commands.rename(team_member_1="2v2_team_member_1")
    @app_commands.rename(team_member_2="2v2_team_member_2")
    @app_commands.rename(team_member_3="2v2_team_member_3")
    async def _2v2_application(        
        self,
        interaction: discord.Interaction,
        team_name: str,
        team_color: str,
        team_captain: discord.Member,
        team_member_1: discord.Member,
        team_member_2: typing.Optional[discord.Member],
        team_member_3: typing.Optional[discord.Member]
        ):
  
            team_roster = [team_captain, team_member_1, team_member_2, team_member_3]
            
            all_members_verified = await TeamCreation.check_verified(
                self,
                interaction=interaction, 
                team_roster=team_roster
            )

            if all_members_verified:

                role = discord.utils.get(interaction.guild.roles, name=team_name)
                
                if role is not None:
                    await interaction.response.send_message(content="Error: a team with this name alreday exists. Try a different name.")
                    return
                
                else:                

                    await TeamCreation.success_embed(
                        self,
                        interaction=interaction,
                        description=f"{interaction.user.mention} Thank You For Submitting Your 2v2 Application!"
                    )

                    new_hex_color = await ClanCreationMethods.colour_converter(
                        self=self,
                        clan_color=team_color
                    )

                    team_role = await RoleCreation.create_role(
                        self,
                        interaction=interaction,
                        role_name=team_name,
                        role_colour=new_hex_color,
                        role_divider_id=1127036811030581378
                    )

                    await RoleCreation.assign_roles(
                        self,
                        interaction=interaction,
                        member_roster=team_roster,
                        role=team_role,
                        leader_role_id=1127037883195334666,
                        co_leader_role_id=None,
                        ping_role_id=1047716260185653298
                    )

                    await TeamCreation.application_log_embed(
                        self,
                        interaction=interaction,
                        team_name=team_name,
                        tournament_type="2v2",
                        team_roster=team_roster
                    )


    @app_commands.check(bots_or_work_channel)
    @sub_group.command(
        name="3v3",
        description="A Command That Allows You To Submit A 3v3 Tournament Application!")
    @app_commands.describe(team_captain="Ping Your Team Captain Here!")
    @app_commands.describe(team_co_captain="Ping Your Team Co-Captain Here!")
    @app_commands.describe(team_member_1="Ping Your 1st Team Member Here!")
    @app_commands.describe(team_member_2="Ping Your 2nd Team Member Here!")
    @app_commands.describe(team_member_3="Ping Your 3rd Team Member Here!")
    @app_commands.describe(team_member_4="Ping Your 4th Team Member Here!")
    @app_commands.rename(team_captain="3v3_team_captain")
    @app_commands.rename(team_co_captain="3v3_team_co_captain")
    @app_commands.rename(team_member_1="3v3_team_member_1")
    @app_commands.rename(team_member_2="3v3_team_member_2")
    @app_commands.rename(team_member_3="3v3_team_member_3")
    @app_commands.rename(team_member_4="3v3_team_member_4")    
    async def _3v3_application(        
        self,
        interaction: discord.Interaction,
        team_name: str,
        team_color: str,
        team_captain: discord.Member,
        team_co_captain: discord.Member,
        team_member_1: discord.Member,
        team_member_2: typing.Optional[discord.Member],
        team_member_3: typing.Optional[discord.Member],
        team_member_4: typing.Optional[discord.Member]
    ):
        team_roster = [team_captain, team_co_captain, team_member_1, team_member_2, team_member_3, team_member_4]
        
        all_members_verified = await TeamCreation.check_verified(
            self,
            interaction=interaction, 
            team_roster=team_roster
        )

        if all_members_verified:
            role = discord.utils.get(interaction.guild.roles, name=team_name)
            
            if role is not None:
                await interaction.response.send_message(content="Error: a team with this name alreday exists. Try a different name.")
                return
            
            else:                        
                await TeamCreation.success_embed(
                    self,
                    interaction=interaction,
                    description=f"{interaction.user.mention} Thank You For Submitting Your 3v3 Application!"
                )
                                
                new_hex_color = await ClanCreationMethods.colour_converter(
                    self=self,
                    clan_color=team_color
                )

                team_role = await RoleCreation.create_role(  
                    self,
                    interaction=interaction,
                    role_name=team_name,
                    role_colour=new_hex_color,
                    role_divider_id=1127036934691233964
                )

                await RoleCreation.assign_roles(
                    self,
                    interaction=interaction,
                    member_roster=[team_captain, team_member_1, team_member_2, team_member_3],
                    role=team_role,
                    leader_role_id=1127082375420059719,
                    co_leader_role_id=1127082480894230618,
                    ping_role_id=1047716260185653298
                )

                await TeamCreation.application_log_embed(
                    self,
                    interaction=interaction,
                    team_name=team_name,
                    tournament_type="3v3",
                    team_roster=team_roster
                )


    async def disband_log_embed(
        self,
        interaction: discord.Interaction,
        tournament_type,
        tournament_team_name
        ):
            tournament_applications_channel = discord.utils.get(
                interaction.guild.channels, 
                id=1043644487949357157
            )

            log_embed = discord.Embed(
            title=f"The Conquering Games {tournament_type} Team Disband Application", 
            color=0x00ffff,
            timestamp=interaction.created_at
            )

            log_embed.set_author(
                name=f"Submitted By: {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url
            )

            log_embed.set_footer(
                text=f"The Conquering 3 • {tournament_type} Disband Application",
                icon_url=interaction.guild.icon
            )

            log_embed.add_field(
                name=f"{tournament_type} Team Name", 
                value=f"``{tournament_team_name}``",
                inline=False
                )

            await tournament_applications_channel.send(
                content=f"``<@711003479430266972>, <@768259026084429896>, <@282761998326824961>``",
                embed=log_embed
            )


    @app_commands.checks.has_any_role(1127037883195334666, 1127082375420059719, 1127082480894230618)
    @app_commands.check(bots_or_work_channel)
    @group.command(
        name="disband",
        description="A Command That Disbands Your Tournament Team")
    @app_commands.choices(game_mode=[
        Choice(name="2v2", value=1),
        Choice(name="3v3", value=2),
    ])    
    async def disband_team(
        self,
        interaction: discord.Interaction,
        game_mode: Choice[int]
    ):      
        success_embed = discord.Embed(
            title="Match Staff Have Been Notified That You Disbanded Your Team!",
            description=f"We're sad to see you go 😢",
            color=0x00ffff
        )

        await interaction.response.send_message(embed=success_embed)            
    
        co_leader_role_id = None
        if game_mode.name == "2v2":
            top_role_divider_id = 1127036811030581378
            bottom_role_divider_id = 1127036934691233964
            leader_role_id = 1127037883195334666
            division_role = await ClanChangesMethods.get_clan_role(
                self=self,
                interaction=interaction,
                top_role_divider=interaction.guild.get_role(1127037883195334666),
                bottom_role_divider=interaction.guild.get_role(1127082375420059719)
            )

        elif game_mode.name == "3v3":
            top_role_divider_id = 1127036934691233964
            bottom_role_divider_id = 1047715900515700847
            leader_role_id = 1127082375420059719
            co_leader_role_id = 1127082480894230618
            division_role = await ClanChangesMethods.get_clan_role(
                self=self,
                interaction=interaction,
                top_role_divider=interaction.guild.get_role(1127082480894230618),
                bottom_role_divider=interaction.guild.get_role(1048286357858046003)
            )

        else:
            print("Error occured. Could not identify the game_mode.")

        team_role = await ClanChangesMethods.get_clan_role(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(top_role_divider_id),
            bottom_role_divider=interaction.guild.get_role(bottom_role_divider_id)
        )

        role_config_list = [team_role, division_role, interaction.guild.get_role(leader_role_id)]
        if game_mode.name == "3v3":
            role_config_list.append(interaction.guild.get_role(co_leader_role_id))

        for member in team_role.members:
            for role in role_config_list:
                await member.remove_roles(role)

        await team_role.delete()

        await TournamentApplicationCommands.disband_log_embed(
            self=self,
            interaction=interaction,
            tournament_type=type,
            tournament_team_name=team_role.name
        )


async def setup(bot):
    await bot.add_cog(TournamentApplicationCommands(bot))