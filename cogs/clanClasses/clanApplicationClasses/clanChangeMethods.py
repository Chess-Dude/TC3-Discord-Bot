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
        new_clan_member,
        pool
    ):
        for role in roles_to_add:
            await new_clan_member.add_roles(role)

        async with pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointTracker WHERE discordUserID = $1"
            member_clan_point_data = await connection.fetch(sql, new_clan_member.id)

            if len(member_clan_point_data) == 0:
                sql = "INSERT INTO ClanPointTracker (robloxUsername, discordUserID, totalClanPoints, currentClanRoleID, currentClanName) VALUES ($1, $2, $3, $4, $5)"
                values = (new_clan_member.nick, new_clan_member.id, 0, roles_to_add[0].id, roles_to_add[0].name)
                await connection.execute(sql, *values)
            else:
                sql = "UPDATE ClanPointTracker SET currentClanRoleID = $1, currentClanName = $2 WHERE discordUserID = $3"
                values = (roles_to_add[0].id, roles_to_add[0].name, new_clan_member.id)
                await connection.execute(sql, *values)
        

    async def remove_clan_member(
        self,
        interaction: discord.Interaction,
        roles_to_remove,
        remove_clan_member,
        pool
    ):

        for role in roles_to_remove:
            await remove_clan_member.remove_roles(role)              


        async with pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointTracker WHERE discordUserID = $1"
            member_clan_point_data = await connection.fetch(sql, remove_clan_member.id)

            if len(member_clan_point_data) != 0:
                sql = "UPDATE ClanPointTracker SET currentClanRoleID = $1, currentClanName = $2 WHERE discordUserID = $3"
                await connection.execute(sql, 0, "NONE", remove_clan_member.id)

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

    