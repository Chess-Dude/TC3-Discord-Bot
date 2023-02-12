import discord, typing
from discord import app_commands
from discord.ext import commands

class TeamCreation():
            
    async def roster_embed(
        self, 
        interaction: discord.Interaction, 
        team_name,        
        tournament_type, 
        team_roster,
        tournament_division,
        roster_thread
    ):
        
        roster_embed = discord.Embed(
            title=f"{team_name}'s Roster", 
            color=0x00ffff,
            timestamp=interaction.created_at
        )

        roster_embed.set_footer(
            text=f"The Conquerors 3 • {tournament_type} Tournaments",
            icon_url=interaction.guild.icon
        )

        roster_embed.add_field(
            name=f"Team Name:",
            value=f"``{team_name}``",
            inline=False
        )
        roster_embed.add_field(
            name=f"Team Division:",
            value=f"``{tournament_division}``",
            inline=False
        )

        team_member_count = 0
        for iteration, player in enumerate(team_roster):
            if player == team_roster[0]:
                roster_embed.add_field(
                    name=f"Team Captain:",
                    value=f"{team_roster[0].mention}, ``{team_roster[0].id}``",
                    inline=False
                )
                continue

            if tournament_type == "3v3":
                if player == team_roster[1]:
                    roster_embed.add_field(
                        name=f"Team Co-Captain:",
                        value=f"{team_roster[1].mention}, ``{team_roster[1].id}``",
                        inline=False
                    )
                    continue
                
            if player != team_roster[iteration-1]:
                team_member_count = team_member_count + 1
                roster_embed.add_field(
                    name=f"Team Member {team_member_count}:",
                    value=f"{player.mention}, ``{player.id}``",
                    inline=False
                )
                
        return roster_embed

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
        team_name_field = log_embed_fields[0]
        team_name = team_name_field["value"]
        team_name = team_name.replace('`', '')
        info_field = log_embed_fields[-1]
        info_str = info_field["value"]
        tournament_division = self.values[0]
        tournament_division_role = discord.utils.get(interaction.guild.roles, name=f"{tournament_division}")

        team_roster_list = []
        id_list = []
        word_list = info_str.split(' ')
        tournament_type = info_str[0:3]
        if tournament_type == "1v1":
            for word in word_list:
                try:
                    player_id = int(word)
                    player = interaction.guild.get_member(player_id)
                    break

                except ValueError:
                    continue 

        elif tournament_type == "2v2":
            for word in word_list:
                try:
                    id = int(word)
                    id_list.append(id)
                
                except ValueError:
                    continue

            for member_id in id_list:
                team_member = interaction.guild.get_member(int(member_id))
                team_roster_list.append(team_member)
            roster_thread = interaction.guild.get_channel_or_thread(1041094878232330320)

        elif tournament_type == "3v3":
            for word in word_list:
                try:
                    id = int(word)
                    id_list.append(id)
                
                except ValueError:
                    continue

            for member_id in id_list:
                team_member = interaction.guild.get_member(int(member_id))
                team_roster_list.append(team_member)

            roster_thread = interaction.guild.get_channel_or_thread(1041094879180243024)

        tournament_role = interaction.guild.get_role(1047716260185653298)

        if tournament_type != "1v1":    
            roster_embed = await TeamCreation.roster_embed(
                self,
                interaction=interaction,
                team_name=team_name,
                tournament_type=tournament_type,
                tournament_division=tournament_division,
                team_roster=team_roster_list,
                roster_thread=roster_thread
            )

            roster_embed_message = await roster_thread.send(embed=roster_embed)
            if tournament_type == "2v2":
                roster_thread_str = "<#1045927311842750486>"
            else:
                roster_thread_str = "<#1045927352187752548>"

            for member in team_roster_list:
                await member.add_roles(tournament_division_role)
                await member.add_roles(tournament_role)
                await member.send(
                    content=f"Your team has been created by {interaction.user.mention}! \n{roster_embed_message.jump_url}\n\nYou can ping you and your teammates in {roster_thread_str} to sign up for a tournament!",
                    embed=roster_embed
                    )
    
            await interaction.channel.send(f"{interaction.user.mention} Created ``{team_name}`` and place them in ``{tournament_division}`` ")

        else:
            await player.add_roles(tournament_division_role)
            await player.add_roles(tournament_role)
            await player.send(content=f"You have been placed in {tournament_division} by {interaction.user.mention}! You can now ping yourself in <#1045927249825775647> to sign up for a tournament!")
            await interaction.channel.send(f"{interaction.user.mention} Placed {player.mention} in {tournament_division}")
        
        await interaction.message.edit(view=None)


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class tournament_application_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots_or_work_channel(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 896440473659519057 or ctx.channel.id == 351057167706619914

    async def success_embed(
        self, 
        interaction: discord.Interaction, 
        description
    ):

        success_embed = discord.Embed(
            title="Match Staff Notified!", 
            description=description, 
            color=0x00ffff
            )

        await interaction.response.send_message(embed=success_embed)
        
    async def application_log_embed(
        self, 
        interaction: discord.Interaction, 
        team_name,
        tournament_type, 
        team_roster
    ):
        server = interaction.guild
        tournament_applications_channel = server.get_channel(1043644487949357157)

        log_embed = discord.Embed(
            title=f"{tournament_type} Tournament Application", 
            color=0xff0000,
            timestamp=interaction.created_at
        )

        log_embed.set_author(
            name=f"Submitted By: {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )

        log_embed.set_footer(
            text=f"The Conquerors 3 • {tournament_type} Tournament Application",
            icon_url=interaction.guild.icon
        )

        if tournament_type != "1v1":
            log_embed.add_field(
                name=f"Team Name:",
                value=f"``{team_name}``",
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

        team_members_id = str(team_members_id)[1:-1]
        team_members_id = team_members_id.replace(',', "")

        if team_name != None:
            if ' ' in team_name:
                team_name = f'"{team_name}"'                
            log_embed.add_field(
                name="Bot Information:",
                value=f"{tournament_type} {team_members_id}",
                inline=False
            )

        else:
                log_embed.add_field(
                    name="Bot Information:",
                    value=f"{tournament_type} {team_members_id}",
                    inline=False
                )            

        view = DropdownView()
        await tournament_applications_channel.send(
            content=f"<@650847350042132514>, <@818729621029388338>, <@319573094731874304>, <@198273107205685248>, <@711003479430266972>, <@768259026084429896>, <@820952452739891281>, <@282761998326824961>",
            embed=log_embed,
            view=view
            )

    async def check_verified(
        self, 
        interaction: discord.Interaction, 
        team_roster
    ):
        
        verified_role = interaction.guild.get_role(365244875861393408)

        unverified_members = []

        for member in team_roster:
            if member != None:
                if verified_role not in member.roles:
                    unverified_members.append(member.display_name)
        
        if len(unverified_members) > 0:
            unverified_members = (','.join(unverified_members))
            await interaction.response.send_message(f"__The Following Members Are **Unverified**:__\n{unverified_members}\n\nPlease have them run the ``/verify`` command in <#351057167706619914>. Once all members are verified, you must redo the application.", ephemeral=True)
        else:
            return True

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
        
        all_members_verified = await tournament_application_commands.check_verified(
            self,
            interaction=interaction, 
            team_roster=team_roster
        )

        if all_members_verified:

            await tournament_application_commands.application_log_embed(
                self,
                interaction=interaction,
                team_name=None,
                tournament_type="1v1",
                team_roster=team_roster
            )

            await tournament_application_commands.success_embed(
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
            
            all_members_verified = await tournament_application_commands.check_verified(
                self,
                interaction=interaction, 
                team_roster=team_roster
            )

            if all_members_verified:

                await tournament_application_commands.application_log_embed(
                    self,
                    interaction=interaction,
                    team_name=team_name,
                    tournament_type="2v2",
                    team_roster=team_roster
                )

                await tournament_application_commands.success_embed(
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
            
            all_members_verified = await tournament_application_commands.check_verified(
                self,
                interaction=interaction, 
                team_roster=team_roster
            )

            if all_members_verified:

                await tournament_application_commands.application_log_embed(
                    self,
                    interaction=interaction,
                    team_name=team_name,
                    tournament_type="3v3",
                    team_roster=team_roster
                )

                await tournament_application_commands.success_embed(
                    self,
                    interaction=interaction,
                    description=f"{interaction.user.mention} Thank You For Submitting Your 3v3 Application!"
                )

async def setup(bot):
    await bot.add_cog(tournament_application_commands(bot))