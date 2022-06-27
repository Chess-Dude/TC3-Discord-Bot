import discord, typing, matplotlib
from discord import app_commands, Colour
from discord.ext import commands

class TeamCreation():
    async def create_role(
        self, 
        interaction: discord.Interaction, 
        role_name, 
        colour: discord.Colour, 
        role_divider_id
        ): 
        
        TCG = interaction.guild
        role_divider = discord.utils.get(TCG.roles, id=role_divider_id)
        await TCG.create_role(name=role_name, colour=colour)
        team_role = discord.utils.get(TCG.roles, name=role_name)
        await team_role.edit(position=role_divider.position-1)
        
        return team_role

    async def assign_roles(
        self, 
        interaction: discord.Interaction, 
        team_roster,
        team_role, # custom tournament team role
        tournament_division_role, # x tournaments scout/mid/juggernaut division  
        tournament_type_role_id, # 2v2/3v3/4v4 role divider
        team_captain_role_id, # team captain
        team_co_captain_role_id, # team co captain 
        tournament_type # 2v2/3v3/4v4 str
        ):

        TCG = interaction.guild
        tournament_type_role = discord.utils.get(TCG.roles, id=tournament_type_role_id)
        team_captain_role = discord.utils.get(TCG.roles, id=team_captain_role_id)
        team_co_captain = discord.utils.get(TCG.roles, id=team_co_captain_role_id)

        for member in team_roster:
            if member == team_roster[0]:
                await member.add_roles(team_captain_role)

            if (((tournament_type == "3v3") and 
                (member == team_roster[1])) or 
                ((tournament_type == "4v4") and 
                (member == team_roster[1]))): 
                await member.add_roles(team_co_captain)

            while ((team_role not in member.roles) or 
            (tournament_division_role not in member.roles) or 
            (tournament_type_role not in member.roles)): 
                await member.add_roles(team_role)
                await member.add_roles(tournament_division_role)
                await member.add_roles(tournament_type_role)        
            
class Dropdown(discord.ui.Select):
    def __init__(self):
        division_list = [
            discord.SelectOption(
                label="1v1 Tournaments Scout Division",
                description="The Players's Division is Scout",
                ),
            discord.SelectOption(
                label="1v1 Tournaments Light Soldier Division",
                description="The Players's Division is Light Soldier",
                emoji=None
                ),
            discord.SelectOption(
                label="1v1 Tournaments Heavy Soldier Division",
                description="The Players's Division is Heavy Soldier",
                emoji=None
                ),
            discord.SelectOption(
                label="1v1 Tournaments Juggernaut Division",
                description="The Players's Division is Juggernaut",
                emoji=None
                ),
            discord.SelectOption(
                label="2v2 Tournaments Scout Division",
                description="The 2v2 Teams's Division is Scout",
                emoji=None
                ),
            discord.SelectOption(
                label="2v2 Tournaments Mid Division",
                description="The 2v2 Teams's Division is Mid",
                emoji=None
                ),
            discord.SelectOption(
                label="2v2 Tournaments Juggernaut Division",
                description="The 2v2 Teams's Division is Juggernaut",
                emoji=None
                ),
            discord.SelectOption(
                label="3v3 Tournaments Scout Division",
                description="The 3v3 Teams's Division is Scout",
                emoji=None
                ),                
            discord.SelectOption(
                label="3v3 Tournaments Juggernaut Division",
                description="The 3v3 Teams's Division is Juggernaut",
                emoji=None
                ),                
            ]

        super().__init__(placeholder="Choose The Team Division...", options=division_list, custom_id="application_commands", min_values=1, max_values=1)

    async def callback(
        self, 
        interaction: discord.Interaction,
        ):
        await interaction.response.send_message(f"loading...")

        log_embed_message =  interaction.message
        log_embed = log_embed_message.embeds[0].to_dict()
        log_embed_fields = log_embed['fields']
        create_role_field = log_embed_fields[-1]
        info_str = create_role_field["value"]
        start_index = 0
        end_index = 0
        role_divider_id = int
        team_captain = int
        team_co_captain = int
        team_member_1 = int
        team_member_2 = int
        team_member_3 = int
        team_member_4 = int
        captain_role_id = int 
        co_captain_role_id = int 
        tournament_type_role_id = int
        tournament_division_role = discord.utils.get(interaction.guild.roles, name=self.values[0])
        team_hex_color = str

        if info_str[len("!createrole___ ")] == '"':
            start_index = 1 
            end_index = 1

        tournament_type = info_str[len("!createrole"):len("!createrole") + 3]
        if tournament_type == "1v1":
            player_id = info_str[len("!createrole1v1 "):-len(" '1v1 Tournaments Default Division'")]
            player = interaction.guild.get_member(int(player_id))
            tournament_type_role = interaction.guild.get_role(896542577296306217)
            
            while ((tournament_division_role not in player.roles) or 
            (tournament_type_role not in player.roles)):
                await player.add_roles(tournament_division_role)
                await player.add_roles(tournament_type_role)
            
        elif tournament_type == "2v2":
            team_name = info_str[len("!createrole___ ") + start_index:-len(" 621516858205405197 585991378400706570 585991378400706570 585991378400706570 #36393E '2v2 Tournaments Default Division'") - end_index]
            team_roster_str = info_str[-len("621516858205405197 585991378400706570 585991378400706570 585991378400706570 #36393E '2v2 Tournaments Default Division'") :-len(" #36393E '2v2 Tournaments Default Division'")]
            team_roster_list = team_roster_str.split(' ')
            team_hex_color = info_str[-len("#36393E '2v2 Tournaments Default Division'"):-len(" '2v2 Tournaments Default Division'")]

            team_captain = interaction.guild.get_member(int(team_roster_list[0]))
            team_co_captain = interaction.guild.get_member(int(team_roster_list[1]))            
            team_member_1 = interaction.guild.get_member(int(team_roster_list[2]))            
            team_member_2 = interaction.guild.get_member(int(team_roster_list[3]))            
            team_member_3 = interaction.guild.get_member(int(team_roster_list[3]))            
            team_member_4 = interaction.guild.get_member(int(team_roster_list[3]))
            role_divider_id = 707250483743424683    
            captain_role_id = 896550746475077672 
            co_captain_role_id = 716290546519244850 
            tournament_type_role_id = 896550133309775872

        elif tournament_type == "3v3":
            team_name = info_str[len("!createrole___ ") + start_index:-len(" 621516858205405197 585991378400706570 585991378400706570 585991378400706570 585991378400706570 585991378400706570 #36393E '3v3 Tournaments Default Division'") - end_index]
            team_roster_str = info_str[-len("621516858205405197 585991378400706570 585991378400706570 585991378400706570 585991378400706570 585991378400706570 #36393E '3v3 Tournaments Default Division'") :-len(" #36393E '3v3 Tournaments Default Division'")]            
            team_roster_list = team_roster_str.split(' ')
            team_hex_color = info_str[-len("#36393E '3v3 Tournaments Default Division'"):-len(" '3v3 Tournaments Default Division'")]
            team_captain = interaction.guild.get_member(int(team_roster_list[0]))
            team_co_captain = interaction.guild.get_member(int(team_roster_list[1]))            
            team_member_1 = interaction.guild.get_member(int(team_roster_list[2]))            
            team_member_2 = interaction.guild.get_member(int(team_roster_list[3]))            
            team_member_3 = interaction.guild.get_member(int(team_roster_list[4]))            
            team_member_4 = interaction.guild.get_member(int(team_roster_list[5]))
            role_divider_id = 707250485702426625    
            captain_role_id = 649683977241886730 
            co_captain_role_id = 716290546519244850 
            tournament_type_role_id = 896555065282818079

        if tournament_type != "1v1":    
            team_roster_list = [team_captain, team_co_captain, team_member_1, team_member_2, team_member_3, team_member_4]
            team_hex_color = discord.Color.from_str(team_hex_color)

            team_role = await TeamCreation.create_role(
                self, 
                interaction, 
                team_name, 
                team_hex_color, 
                role_divider_id
                )
        
            await TeamCreation.assign_roles(
                self, 
                interaction=interaction, 
                team_roster=team_roster_list, 
                team_role=team_role,
                tournament_type_role_id=tournament_type_role_id, 
                tournament_division_role=tournament_division_role, 
                team_captain_role_id=captain_role_id, 
                team_co_captain_role_id=co_captain_role_id, 
                tournament_type=tournament_type
                )
        
            await interaction.channel.send(f"{interaction.user.mention} Created {team_role.mention} ")
        
        else:
            await interaction.channel.send(f"{interaction.user.mention} Placed {player.mention} in {tournament_division_role.name}")


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class application_test_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots_or_work_channel(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 408820459279220736 or ctx.channel.id == 896440473659519057

    async def colour_converter(
        self,
        team_color
        ):
        
        try:
            hex_color: Colour = Colour.from_str(team_color)
            hex_color = str(hex_color)
        except ValueError:
            try:
                hex_color = matplotlib.colors.cnames[team_color]
            except KeyError:
                hex_color = "#000000"

        return hex_color 

    async def success_embed(
        self, 
        interaction: discord.Interaction, 
        description
        ):

        success_embed = discord.Embed(
            title="Match Staff Notified!", 
            description=description, 
            color=0xff0000
            )

        await interaction.response.send_message(embed=success_embed)
        
    async def application_log_embed(
        self, 
        interaction: discord.Interaction, 
        team_name,
        team_color,        
        tournament_type, 
        team_roster
        ):
        TCG = interaction.guild
        tournament_applications_channel = TCG.get_channel(896444200432861237)
        ms_role = discord.utils.get(
            TCG.roles, 
            id=935698898251567124
            )
        tms_role = discord.utils.get(
            TCG.roles, 
            id=896440653406433310
            )

        log_embed = discord.Embed(
            title=f"The Conquering Games {tournament_type} Application", 
            color=0xff0000,
            timestamp=interaction.created_at
        )

        log_embed.set_author(
            name=f"Submitted By: {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )

        log_embed.set_footer(
            text=f"The Conquering Games {tournament_type} Application",
            icon_url=interaction.guild.icon
        )

        if tournament_type != "1v1":
            log_embed.add_field(
                name=f"Team Name:",
                value=f"``{team_name}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Team Color:",
                value=f"``{team_color}``",
                inline=False
            )

        team_member_count = 0
        team_members_id = []
        for iteration, player in enumerate(team_roster):
            if player == team_roster[0]:
                log_embed.add_field(
                    name=f"Team Captain:",
                    value=f"{team_roster[0].mention}, ``{team_roster[0].id}``",
                    inline=False
                )
                team_members_id.append(player.id)
                continue

            if tournament_type == "3v3":
                if player == team_roster[1]:
                    log_embed.add_field(
                        name=f"Team Co-Captain:",
                        value=f"{team_roster[1].mention}, ``{team_roster[1].id}``",
                        inline=False
                    )
                    team_members_id.append(player.id)
                    continue
                
            if player != None:
                team_member_count = team_member_count + 1
                log_embed.add_field(
                    name=f"Team Member {team_member_count}:",
                    value=f"{player.mention}, ``{player.id}``",
                    inline=False
                )
                team_members_id.append(player.id)

            else:
                team_members_id.append(team_members_id[iteration-1])
        
        team_members_id = str(team_members_id)[1:-1]
        team_members_id = team_members_id.replace(',', "")
        
        if team_name != None:
            if ' ' in team_name:
                team_name = f'"{team_name}"'                
            log_embed.add_field(
                name="Potential Create Role Command:",
                value=f'!createrole{tournament_type} {team_name} {team_members_id} {team_color} "{tournament_type} Tournaments Default Division"',
                inline=False
            )

        else:
                log_embed.add_field(
                    name="Potential Create Role Command:",
                    value=f'!createrole{tournament_type} {team_members_id} "{tournament_type} Tournaments Default Division"',
                    inline=False
                )            

        view = DropdownView()
        await tournament_applications_channel.send(
            content=f"{ms_role.mention} {tms_role.mention}",
            embed=log_embed,
            view=view
            )

    async def check_verified(
        self, 
        interaction: discord.Interaction, 
        team_roster
        ):
        TCG = interaction.guild
        verified_role = discord.utils.get(
            TCG.roles, 
            id=421100153114722317
            )
        unverified_members = []

        for member in team_roster:
            if member != None:
                if verified_role not in member.roles:
                    unverified_members.append(member.display_name)
        
        if len(unverified_members) > 0:
            unverified_members = (','.join(unverified_members))
            await interaction.response.send_message(f"__The Following Members Are **Unverified**:__\n{unverified_members}\n\nPlease have them run the !verify command in <#408820459279220736>. Once all members are verified, you must redo the application.", ephemeral=True)
        else:
            return True

    group = app_commands.Group(
        name="tournament", 
        description="A Command That Allows You To Submit A Tournament Application!",
        guild_ids=[371817692199518240])
    
    sub_group = app_commands.Group(
        name="application", 
        parent=group, 
        description="A Command That Allows You To Submit A Tournament Application!")
    
    @app_commands.check(bots_or_work_channel)
    @sub_group.command(
        name="1v1",
        description="A Command That Allows You To Submit A 1v1 Tournament Application!")
    @app_commands.describe(player="Ping Yourself Here!")
    @app_commands.rename(player="player")
    async def _1v1_application(        
        self,
        interaction: discord.Interaction,
        player: discord.Member,
        ):
        team_roster = [player]
        
        all_members_verified = await application_test_commands.check_verified(
            self,
            interaction, 
            team_roster
        )

        if all_members_verified:
            await application_test_commands.application_log_embed(
                self,
                interaction,
                None,
                None,
                "1v1",
                team_roster
            )

            await application_test_commands.success_embed(
                self,
                interaction,
                f"{interaction.user.mention} Thank You For Submitting Your 1v1 Application!"
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
            
            all_members_verified = await application_test_commands.check_verified(
                self,
                interaction, 
                team_roster
            )

            if all_members_verified:

                team_color = await application_test_commands.colour_converter(
                self,
                team_color
                )
                
                await application_test_commands.application_log_embed(
                    self,
                    interaction,
                    team_name,
                    team_color,
                    "2v2",
                    team_roster
                )

                await application_test_commands.success_embed(
                    self,
                    interaction,
                    f"{interaction.user.mention} Thank You For Submitting Your 2v2 Application!"
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
            
            all_members_verified = await application_test_commands.check_verified(
                self,
                interaction, 
                team_roster
            )

            if all_members_verified:
                team_color = await application_test_commands.colour_converter(
                    self,
                    team_color
                )

                await application_test_commands.application_log_embed(
                    self,
                    interaction,
                    team_name,
                    str(team_color),
                    "3v3",
                    team_roster
                )

                await application_test_commands.success_embed(
                    self,
                    interaction,
                    f"{interaction.user.mention} Thank You For Submitting Your 3v3 Application!"
                )

async def setup(bot):
    await bot.add_cog(application_test_commands(bot))