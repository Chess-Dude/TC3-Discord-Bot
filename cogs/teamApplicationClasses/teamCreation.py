import discord
from .teamApplicationDropdown import TournamentDropdownView

class TeamCreation():

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

        view = TournamentDropdownView()
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
