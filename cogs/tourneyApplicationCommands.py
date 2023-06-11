import discord, typing
from discord import app_commands
from discord.ext import commands
from .teamApplicationClasses.teamCreation import TeamCreation

class TournamentApplicationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots_or_work_channel(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 896440473659519057 or ctx.channel.id == 351057167706619914

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

                await TeamCreation.application_log_embed(
                    self,
                    interaction=interaction,
                    team_name=team_name,
                    tournament_type="2v2",
                    team_roster=team_roster
                )

                await TeamCreation.success_embed(
                    self,
                    interaction=interaction,
                    description=f"{interaction.user.mention} Thank You For Submitting Your 2v2 Application!"
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

                await TeamCreation.application_log_embed(
                    self,
                    interaction=interaction,
                    team_name=team_name,
                    tournament_type="3v3",
                    team_roster=team_roster
                )

                await TeamCreation.success_embed(
                    self,
                    interaction=interaction,
                    description=f"{interaction.user.mention} Thank You For Submitting Your 3v3 Application!"
                )

async def setup(bot):
    await bot.add_cog(TournamentApplicationCommands(bot))