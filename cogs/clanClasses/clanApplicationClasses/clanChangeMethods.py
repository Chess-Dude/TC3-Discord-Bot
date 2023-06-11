import discord 

class ClanChangesMethods():
    
    async def update_clan_hex_color(
        self,
        clan_role,
        new_tournament_team_hex_color
    ):
        if clan_role.color != new_tournament_team_hex_color:
            await clan_role.edit(color=new_tournament_team_hex_color)

    async def update_clan_leader(
        self,
        interaction,
        roles_to_config,
        new_clan_leader
    ):
            for role in roles_to_config:                
                await new_clan_leader.add_roles(role)
                await interaction.user.remove_roles(role)
    
    async def update_clan_co_leader(
        self,
        roles_to_add,
        new_clan_co_leader
    ):
        for role in roles_to_add:
            await new_clan_co_leader.add_roles(role)
        
    async def add_clan_member(
        self,
        roles_to_add,
        new_clan_member
    ):
        for role in roles_to_add:
            await new_clan_member.add_roles(role)
            

    async def remove_clan_member(
        self,
        interaction: discord.Interaction,
        roles_to_remove,
        remove_clan_member
    ):
        if roles_to_remove[-1] not in interaction.user.roles:
            for role in roles_to_remove:
                await interaction.user.remove_roles(role)              

        else:
            for role in roles_to_remove:
                await remove_clan_member.remove_roles(role)              

    async def get_clan_role(
        self,
        interaction: discord.Interaction,
        top_role_divider,
        bottom_role_divider,
        ):
            for role_position in range(top_role_divider.position - 1, bottom_role_divider.position, - 1):
                clan_role = discord.utils.get(interaction.guild.roles, position=role_position)
                if clan_role in interaction.user.roles:
                    return clan_role
                
                else:
                    continue
