import discord, typing
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from cogs.appCommandsTest import application_test_commands

class TournamentChangeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots_or_work_channel(interaction: discord.Interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 408820459279220736 or interaction.channel.id == 896440473659519057
    
    def test_channel(interaction: discord.Interaction):
        return interaction.channel.id == 941567353672589322 #or interaction.channel.id == 408820459279220736 or interaction.channel.id == 896440473659519057

    team_group = app_commands.Group(
        name="team", 
        description="A Command That Allows You To Make Changes To Your Tournament Team!",
        guild_ids=[371817692199518240])
    change_group = app_commands.Group(
        name="change", 
        parent=team_group, 
        description="A Command That Allows You To Make Changes To Your Tournament Team!")

    async def get_tournament_team(
        self,
        interaction: discord.Interaction,
        top_role_divider,
        bottom_role_divider,
        ):
            for role_position in range(top_role_divider.position - 1, bottom_role_divider.position, - 1):
                tournament_team_role = discord.utils.get(interaction.guild.roles, position=role_position)
                if tournament_team_role in interaction.user.roles:
                    return tournament_team_role
                
                else:
                    continue

    async def get_tournament_team_division(
        self, 
        interaction: discord.Interaction,
        top_role_divider,
        bottom_role_divider
        ):
            for role_position in range(top_role_divider.position - 1, bottom_role_divider.position, - 1):
                tournament_team_division_role = discord.utils.get(interaction.guild.roles, position=role_position)
                if tournament_team_division_role in interaction.user.roles:
                    return tournament_team_division_role
                
                else:
                    continue

    async def disband_tournament_team(
        self,
        tournament_team_role,
        team_captain_role,
        team_co_captain_role,
        tournament_team_division_role,
        tournament_type_role,
        rover_bypass_role
        ):
            for member in tournament_team_role.members:
                while ((tournament_team_division_role in member.roles) or 
                (tournament_type_role in member.roles) or 
                (team_captain_role in member.roles) or
                (team_captain_role in member.roles) or
                (rover_bypass_role in member.roles)):
                    await member.remove_roles(team_captain_role)
                    await member.remove_roles(team_co_captain_role)
                    await member.remove_roles(tournament_team_division_role)
                    await member.remove_roles(tournament_type_role)
                    await member.remove_roles(rover_bypass_role)
                                    
                if " | Team Captain" in member.display_name:
                    await member.edit(nick=member.display_name[:-len(" | Team Captain")])
                
                if " | Team Co-Captain" in member.display_name:
                    await member.edit(nick=member.display_name[:-len(" | Team Co-Captain")])
                                                                                            
            await discord.Role.delete(tournament_team_role)

    async def disband_log_embed(
        self,
        interaction: discord.Interaction,
        tournament_type,
        tournament_team_division_role, 
        tournament_team_role
        ):
            tournament_changes_channel = discord.utils.get(interaction.guild.channels, id=896479412617359361)
            log_embed = discord.Embed(
            title=f"The Conquering Games {tournament_type} Team Disbanded Log", 
            color=0xff0000,
            timestamp=interaction.created_at
            )

            log_embed.set_author(
                name=f"Submitted By: {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url
            )

            log_embed.set_footer(
                text=f"The Conquering Games {tournament_type} Disband Log",
                icon_url=interaction.guild.icon
            )

            log_embed.add_field(
                name=f"{tournament_type} Team Name", 
                value=f"``{tournament_team_role.name}``",
                inline=False
                )
            
            log_embed.add_field(
                name=f"{tournament_type} Team Color:",
                value=f"``{tournament_team_role.color}``",
                inline=False
            )

            log_embed.add_field(
                name=f"{tournament_type} Team Division:",
                value=f"``{tournament_team_division_role.name}``"
            )

            team_member_count = 0
            for iteration, player in enumerate(tournament_team_role.members):
                if player == tournament_team_role.members[0]:
                    log_embed.add_field(
                        name=f"Team Captain:",
                        value=f"{tournament_team_role.members[0].mention}, ``{tournament_team_role.members[0].id}``",
                        inline=False
                    )
                    continue

                if tournament_type == "3v3":
                    if player == tournament_team_role.members[1]:
                        log_embed.add_field(
                            name=f"Team Co-Captain:",
                            value=f"{tournament_team_role.members[1].mention}, ``{tournament_team_role.members[1].id}``",
                            inline=False
                        )
                        continue
                    
                if player != None:
                    team_member_count = team_member_count + 1
                    log_embed.add_field(
                        name=f"Team Member {team_member_count}:",
                        value=f"{player.mention}, ``{player.id}``",
                        inline=False
                    )
            
            await tournament_changes_channel.send(embed=log_embed)

    async def success_embed(
        self,
        interaction: discord.Interaction,
        title,
        description
        ):
            success_embed = discord.Embed(
                title=title,
                description=f"{interaction.user.mention} {description}",
                color=0xff0000
                )
            await interaction.response.send_message(embed=success_embed)

    @app_commands.checks.has_any_role(
        896550746475077672, 
        649683977241886730, 
        716290546519244850)
    @app_commands.check(bots_or_work_channel)
    @change_group.command(
        name="disband",
        description="A Command That Disbands Your Team!")
    @app_commands.choices(tournament_type=[
        Choice(name="2v2", value=1),
        Choice(name="3v3", value=2)
    ])
    async def disband_team_2(
        self,
        interaction: discord.Interaction,
        tournament_type: Choice[int],
    ):        
        await TournamentChangeCommands.success_embed(
            self=self,
            interaction=interaction,
            title="Team Has Been Disbanded Successfully!",
            description="Your Team Has Been Disbanded Successfully!"
            )
    
        if tournament_type.value == 1:
            team_captain_role = interaction.guild.get_role(896550746475077672)
            
            if team_captain_role in interaction.user.roles: 
                tournament_team_role = await TournamentChangeCommands.get_tournament_team(
                    self=self,
                    interaction=interaction,
                    top_role_divider=interaction.guild.get_role(707250483743424683),
                    bottom_role_divider=interaction.guild.get_role(665667383184326657)
                )
                
                tournament_team_division_role = await TournamentChangeCommands.get_tournament_team_division(
                    self=self,
                    interaction=interaction,
                    top_role_divider=interaction.guild.get_role(896550133309775872),
                    bottom_role_divider=interaction.guild.get_role(649685824492929034),
                    )
                
                await TournamentChangeCommands.disband_log_embed(
                    self=self,
                    interaction=interaction,
                    tournament_type=tournament_type.name,
                    tournament_team_division_role=tournament_team_division_role,
                    tournament_team_role=tournament_team_role
                )
                
                await TournamentChangeCommands.disband_tournament_team(
                    self=self,
                    tournament_team_role=tournament_team_role,
                    team_captain_role=team_captain_role,
                    team_co_captain_role=interaction.guild.get_role(896550746475077672),
                    tournament_team_division_role=tournament_team_division_role,
                    tournament_type_role=interaction.guild.get_role(896550133309775872),
                    rover_bypass_role=interaction.guild.get_role(896476284220223499)
                    )

        elif tournament_type.value == 2:
            team_captain_role = interaction.guild.get_role(649683977241886730)
            team_co_captain_role = interaction.guild.get_role(716290546519244850)
            if ((team_captain_role in interaction.user.roles) or 
                (team_co_captain_role in interaction.user.roles)): 
                tournament_team_role = await TournamentChangeCommands.get_tournament_team(
                    self=self,
                    interaction=interaction,
                    top_role_divider=interaction.guild.get_role(707250485702426625),
                    bottom_role_divider=interaction.guild.get_role(707250483743424683)
                )
                print(tournament_team_role.mention)
                tournament_team_division_role = await TournamentChangeCommands.get_tournament_team_division(
                    self=self,
                    interaction=interaction,
                    top_role_divider=interaction.guild.get_role(896555065282818079),
                    bottom_role_divider=interaction.guild.get_role(896550746475077672),
                    )
                
                await TournamentChangeCommands.disband_log_embed(
                    self=self,
                    interaction=interaction,
                    tournament_type=tournament_type.name,
                    tournament_team_division_role=tournament_team_division_role,
                    tournament_team_role=tournament_team_role
                )
                
                await TournamentChangeCommands.disband_tournament_team(
                    self=self,
                    tournament_team_role=tournament_team_role,
                    team_captain_role=team_captain_role,
                    team_co_captain_role=team_co_captain_role,
                    tournament_team_division_role=tournament_team_division_role,
                    tournament_type_role=interaction.guild.get_role(896555065282818079),
                    rover_bypass_role=interaction.guild.get_role(896476284220223499)
                    )

    async def update_team_name(
        self,
        tournament_team_role,
        new_tournament_team_name
        ):
            while new_tournament_team_name != tournament_team_role.name:
                print("update team name")
                await tournament_team_role.edit(name=new_tournament_team_name)

                if new_tournament_team_name == tournament_team_role.name:
                    break

    async def update_team_hex_color(
        self,
        tournament_team_role,
        new_tournament_team_hex_color
    ):
        while tournament_team_role.color != new_tournament_team_hex_color:
            print("update team hex color")
            await tournament_team_role.edit(color=new_tournament_team_hex_color)

            if tournament_team_role.color == new_tournament_team_hex_color:
                break

    async def update_team_captain(
        self,
        interaction,
        roles_to_config,
        new_team_captain
    ):
            for role in roles_to_config:                
                await new_team_captain.add_roles(role)
                await interaction.user.remove_roles(role)

            if " | Team Captain" in interaction.user.display_name:
                await interaction.user.edit(nick=interaction.user.display_name[:-len(" | Team Captain")])

            if " | Team Co-Captain" in interaction.user.display_name:
                await interaction.user.edit(nick=interaction.user.display_name[:-len(" | Team Co-Captain")])

            try:
                await new_team_captain.edit(nick=f"{new_team_captain.display_name} | Team Captain")

            except:
                pass
    
    async def update_team_co_captain(
        self,
        roles_to_add,
        new_team_co_captain
    ):
        for role in roles_to_add:
            await new_team_co_captain.add_roles(role)

        try:
            await new_team_co_captain.edit(nick=f"{new_team_co_captain.display_name} | Team Co-Captain")

        except:
            pass
        
    async def add_team_member(
        self,
        roles_to_add,
        new_team_member
    ):
        for role in roles_to_add:
            await new_team_member.add_roles(role)

    async def remove_team_member_(
        self,
        interaction: discord.Interaction,
        roles_to_remove,
        remove_team_member
    ):
        if roles_to_remove[-1] not in interaction.user.roles:
            for role in roles_to_remove:
                await interaction.user.remove_roles(role)              

        else:
            for role in roles_to_remove:
                await remove_team_member.remove_roles(role)              

            if " | Team Captain" in remove_team_member.display_name:
                await remove_team_member.edit(nick=remove_team_member.display_name[:-len(" | Team Captain")])

            if " | Team Co-Captain" in remove_team_member.display_name:
                    await remove_team_member.edit(nick=remove_team_member.display_name[:-len(" | Team Co-Captain")])
        
    @app_commands.check(bots_or_work_channel)
    @change_group.command(
        name="2v2",
        description="A Command That Alows You To Make Changes To Your Team!")
    @app_commands.describe(new_team_name="Put Your New Team Name Here!")
    @app_commands.describe(new_team_hex_color="Put Your New Team Hex Color Here!")
    @app_commands.describe(new_team_captain="Ping Your New Team Captain Here!")
    @app_commands.describe(new_team_member="Ping A Member You Would Like To Add To Your Team!")
    @app_commands.describe(remove_team_member="Ping A Member You Would Like To Remove From Your Team")    
    @app_commands.rename(new_team_name="new_team_name")
    @app_commands.rename(new_team_hex_color="new_team_hex_color")
    @app_commands.rename(new_team_captain="new_team_captain")
    @app_commands.rename(new_team_member="new_team_member")
    @app_commands.rename(remove_team_member="remove_team_member")
    async def tournament_2v2_team_change(
        self,
        interaction: discord.Interaction,
        new_team_name: typing.Optional[str],
        new_team_hex_color: typing.Optional[str],
        new_team_captain: typing.Optional[discord.Member],
        new_team_member: typing.Optional[discord.Member],
        remove_team_member: typing.Optional[discord.Member]
    ):    
        await TournamentChangeCommands.success_embed(
            self=self,
            interaction=interaction,
            title="Your 2v2 Team Has Been Updated",
            description="Your 2v2 Team Has Been Updated With The According Changes"
        )

        tournament_team_role = await TournamentChangeCommands.get_tournament_team(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(707250483743424683),
            bottom_role_divider=interaction.guild.get_role(665667383184326657)
        )

        tournament_team_division_role = await TournamentChangeCommands.get_tournament_team_division(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(896550133309775872),
            bottom_role_divider=interaction.guild.get_role(649685824492929034),
            )
        
        team_captain_role = interaction.guild.get_role(896550746475077672)
        if team_captain_role in interaction.user.roles:
            if new_team_name != None:
                print("new_team_name ran")
                await TournamentChangeCommands.update_team_name(
                    self=self,
                    tournament_team_role=tournament_team_role,
                    new_tournament_team_name=new_team_name
                )

            if new_team_hex_color != None:
                print("new_team_hex_color ran")            
                new_team_hex_color = await application_test_commands.colour_converter(
                    self=self,
                    team_color=new_team_hex_color
                )

                await TournamentChangeCommands.update_team_hex_color(
                    self=self,
                    tournament_team_role=tournament_team_role,
                    new_tournament_team_hex_color=discord.Color.from_str(new_team_hex_color)
                )
        
            if new_team_captain != None:
                tournament_type_role = interaction.guild.get_role(896550133309775872)
                rover_bypass_role = interaction.guild.get_role(896476284220223499)
                team_captain_role=interaction.guild.get_role(896550746475077672)
                roles_to_config = [tournament_team_role, tournament_team_division_role, tournament_type_role, team_captain_role, rover_bypass_role, team_captain_role]            
                
                await TournamentChangeCommands.update_team_captain(
                    self=self,
                    interaction=interaction,
                    roles_to_config=roles_to_config,
                    new_team_captain=new_team_captain,
                )
            
            if new_team_member != None:
                tournament_type_role = interaction.guild.get_role(896550133309775872)
                roles_to_add = [tournament_team_role, tournament_team_division_role, tournament_type_role]
                await TournamentChangeCommands.add_team_member(
                    self=self,
                    roles_to_add=roles_to_add,
                    new_team_member=new_team_member
                )

        if remove_team_member != None:
            tournament_type_role = interaction.guild.get_role(896550133309775872)
            team_captain_role = interaction.guild.get_role(896550746475077672)
            rover_bypass_role = interaction.guild.get_role(896476284220223499)
            roles_to_remove = [tournament_team_role, tournament_team_division_role, tournament_type_role, team_captain_role, rover_bypass_role]            
            await TournamentChangeCommands.remove_team_member_(
                self=self,
                interaction=interaction,
                roles_to_remove=roles_to_remove,
                remove_team_member=remove_team_member
            )

    @app_commands.check(bots_or_work_channel)
    @change_group.command(
        name="3v3",
        description="A Command That Alows You To Make Changes To Your Team!")
    @app_commands.describe(new_team_name="Put Your New Team Name Here!")
    @app_commands.describe(new_team_hex_color="Put Your New Team Hex Color Here!")
    @app_commands.describe(new_team_captain="Ping Your New Team Captain Here!")
    @app_commands.describe(new_team_co_captain="Ping Your New Team Co-Captain Here!")
    @app_commands.describe(new_team_member="Ping A Member You Would Like To Add To Your Team!")
    @app_commands.describe(remove_team_member="Ping A Member You Would Like To Remove From Your Team")    
    @app_commands.rename(new_team_name="new_team_name")
    @app_commands.rename(new_team_hex_color="new_team_hex_color")
    @app_commands.rename(new_team_captain="new_team_captain")
    @app_commands.rename(new_team_co_captain="new_team_co_captain")
    @app_commands.rename(new_team_member="new_team_member")
    @app_commands.rename(remove_team_member="remove_team_member")
    async def tournament_3v3_team_change(
        self,
        interaction: discord.Interaction,
        new_team_name: typing.Optional[str],
        new_team_hex_color: typing.Optional[str],
        new_team_captain: typing.Optional[discord.Member],
        new_team_co_captain: typing.Optional[discord.Member],
        new_team_member: typing.Optional[discord.Member],
        remove_team_member: typing.Optional[discord.Member]
    ):    
        await TournamentChangeCommands.success_embed(
            self=self,
            interaction=interaction,
            title="Your 3v3 Team Has Been Updated",
            description="Your 3v3 Team Has Been Updated With The According Changes"
        )

        tournament_team_role = await TournamentChangeCommands.get_tournament_team(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(707250485702426625),
            bottom_role_divider=interaction.guild.get_role(707250483743424683)
        )

        tournament_team_division_role = await TournamentChangeCommands.get_tournament_team_division(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(896555065282818079),
            bottom_role_divider=interaction.guild.get_role(896550746475077672),
            )
                    
        team_captain_role = interaction.guild.get_role(649683977241886730) 
        team_co_captain_role = interaction.guild.get_role(716290546519244850)
        if ((team_captain_role in interaction.user.roles) or 
        (team_co_captain_role in interaction.user.roles)):
            if new_team_name != None:
                await TournamentChangeCommands.update_team_name(
                    self=self,
                    tournament_team_role=tournament_team_role,
                    new_tournament_team_name=new_team_name
                )

            if new_team_hex_color != None:            
                new_team_hex_color = await application_test_commands.colour_converter(
                    self=self,
                    team_color=new_team_hex_color
                )

                await TournamentChangeCommands.update_team_hex_color(
                    self=self,
                    tournament_team_role=tournament_team_role,
                    new_tournament_team_hex_color=discord.Color.from_str(new_team_hex_color)
                )
        
            if new_team_captain != None:
                tournament_type_role = interaction.guild.get_role(896555065282818079)
                rover_bypass_role = interaction.guild.get_role(896476284220223499)
                roles_to_config = [tournament_team_role, tournament_team_division_role, tournament_type_role, team_captain_role, rover_bypass_role]            
                
                await TournamentChangeCommands.update_team_captain(
                    self=self,
                    interaction=interaction,
                    roles_to_config=roles_to_config,
                    new_team_captain=new_team_captain,
                )
            
            if new_team_co_captain != None:
                tournament_type_role = interaction.guild.get_role(896555065282818079)          
                rover_bypass_role = interaction.guild.get_role(896476284220223499)
                roles_to_add = [tournament_team_role, tournament_team_division_role, tournament_type_role, team_co_captain_role, rover_bypass_role, team_captain_role]            

                await TournamentChangeCommands.update_team_co_captain(
                    self=self,
                    roles_to_add=roles_to_add,
                    new_team_co_captain=new_team_co_captain,
                )

            if new_team_member != None:
                tournament_type_role = interaction.guild.get_role(896555065282818079)
                roles_to_add = [tournament_team_role, tournament_team_division_role, tournament_type_role]
                await TournamentChangeCommands.add_team_member(
                    self=self,
                    roles_to_add=roles_to_add,
                    new_team_member=new_team_member
                )

        if remove_team_member != None:
            tournament_type_role = interaction.guild.get_role(896555065282818079)
            team_captain_role = interaction.guild.get_role(649683977241886730)
            team_co_captain_role = interaction.guild.get_role(716290546519244850)
            rover_bypass_role = interaction.guild.get_role(896476284220223499)
            roles_to_remove = [tournament_team_role, tournament_team_division_role, tournament_type_role, team_captain_role, team_co_captain_role, rover_bypass_role]            
            await TournamentChangeCommands.remove_team_member_(
                self=self,
                interaction=interaction,
                roles_to_remove=roles_to_remove,
                remove_team_member=remove_team_member
            )

async def setup(bot):
    await bot.add_cog(TournamentChangeCommands(bot))