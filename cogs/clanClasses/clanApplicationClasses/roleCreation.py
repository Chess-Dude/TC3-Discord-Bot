import discord

class RoleCreation():
    async def create_role(
        self, 
        interaction: discord.Interaction, 
        role_name: str, 
        role_colour: discord.Colour, 
        role_divider_id: int
    ): 
        
        TC3_SERVER = interaction.guild
        role_divider = discord.utils.get(
            TC3_SERVER.roles, 
            id=role_divider_id
        )

        await interaction.guild.create_role(
            reason=f"2v2 Tournament Application by {interaction.user.mention}",
            name=role_name
        )

        role = discord.utils.get(
            TC3_SERVER.roles, 
            name=role_name
        )
        await role.edit(position=role_divider.position-1)
        
        return role

    async def assign_roles(
        self, 
        interaction: discord.Interaction, 
        member_roster,
        role, # custom clan role
        leader_role_id, # clan leader
        co_leader_role_id, # clan co-leader,
        ping_role_id 
    ):

        TC3_SERVER = interaction.guild
        leader_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=leader_role_id
        )

        ping_role = discord.utils.get(
            TC3_SERVER.roles,
            id=ping_role_id
        )

        for member in member_roster:
            if member == member_roster[0]:
                await member.add_roles(leader_role)

            elif member == member_roster[1] and co_leader_role_id != None: 
                co_leader_role = discord.utils.get(
                    TC3_SERVER.roles, 
                    id=co_leader_role_id
                )
                await member.add_roles(co_leader_role)

            if member != None:
                await member.add_roles(role)
                await member.add_roles(ping_role)
            