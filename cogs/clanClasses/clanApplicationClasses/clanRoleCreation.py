import discord

class ClanRoleCreation():
    async def create_role(
        self, 
        interaction: discord.Interaction, 
        role_name, 
        colour: discord.Colour, 
        role_divider_id
    ): 
        
        TC3_SERVER = interaction.guild
        role_divider = discord.utils.get(
            TC3_SERVER.roles, 
            id=role_divider_id
        )
        await TC3_SERVER.create_role(
            name=role_name, 
            colour=colour
        )
        team_role = discord.utils.get(
            TC3_SERVER.roles, 
            name=role_name
        )
        await team_role.edit(position=role_divider.position-1)
        
        return team_role

    async def assign_roles(
        self, 
        interaction: discord.Interaction, 
        clan_roster,
        clan_role, # custom clan role
        clan_leader_role_id, # clan leader
        clan_co_leader_role_id # clan co-leader 
    ):

        TC3_SERVER = interaction.guild
        clan_leader_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=clan_leader_role_id
        )
        clan_co_leader_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=clan_co_leader_role_id
        )

        clans_role_ping = discord.utils.get(
            TC3_SERVER.roles,
            id=1057043814797295646
        )

        for member in clan_roster:
            if member == clan_roster[0]:
                await member.add_roles(clan_leader_role)

            if member == clan_roster[1]: 
                await member.add_roles(clan_co_leader_role)

            if member != None:
                await member.add_roles(clan_role)
                await member.add_roles(clans_role_ping)
            