import discord

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
            discord.SelectOption(
                label="Reject Application",
                description="Reject The Application",
                emoji=None
                )                
            ]

        super().__init__(placeholder="Choose The Team Division...", options=division_list, custom_id="application_commands", min_values=1, max_values=1)


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

    async def callback(
        self, 
        interaction: discord.Interaction,
        ):
        await interaction.response.send_message(f"loading...")

        if self.values[0] != "Reject Application":
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
                # clan_roster_list = [clan_leader, clan_co_leader, clan_member_1, clan_member_2, clan_member_3, clan_member_4]
                # clan_hex_color = discord.Color.from_str(clan_hex_color)

                # clan_role = await ClanRoleCreation.create_role(
                #     self, 
                #     interaction, 
                #     role_name=clan_name, 
                #     colour=clan_hex_color, 
                #     role_divider_id=role_divider_id
                # )

                # await ClanRoleCreation.assign_roles(
                #     self, 
                #     interaction=interaction, 
                #     clan_roster=clan_roster_list, 
                #     clan_role=clan_role,
                #     clan_leader_role_id=clan_leader_role_id, 
                #     clan_co_leader_role_id=clan_co_leader_role_id, 
                # )

                roster_embed = await Dropdown.roster_embed(
                    self,
                    interaction=interaction,
                    team_name=team_name,
                    tournament_type=tournament_type,
                    tournament_division=tournament_division,
                    team_roster=team_roster_list,
                    roster_thread=roster_thread
                )

                roster_embed_message = await roster_thread.send(embed=roster_embed)
                roster_thread_str = "<#1123407962766049340>"


                for member in team_roster_list:
                    await member.add_roles(tournament_division_role)
                    await member.add_roles(tournament_role)
                    try:
                        await member.send(
                            content=f"Your team has been created by {interaction.user.mention}! \nYou can ping you and your teammates in {roster_thread_str} to sign up for a tournament!",
                            embed=roster_embed
                            )
                    except: 
                        pass

                await interaction.channel.send(f"{interaction.user.mention} Created ``{team_name}`` and place them in ``{tournament_division}`` ")

            else:
                await player.add_roles(tournament_division_role)
                await player.add_roles(tournament_role)
                await player.send(content=f"You have been placed in {tournament_division} by {interaction.user.mention}! You can now ping yourself in <#1045927249825775647> to sign up for a tournament!")
                await interaction.channel.send(f"{interaction.user.mention} Placed {player.mention} in {tournament_division}")
        
        else:
            await interaction.channel.send(f"{interaction.user.mention} rejected the application")

        await interaction.message.edit(view=None)


class TournamentDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())
