import discord

class ClanDisbandMethods():
    async def delete_clan_role(
        self,
        clan_role,
        role_config_list,
        bot
    ):
        for member in clan_role.members:
            async with bot.pool.acquire() as connection:
                sql = "SELECT * FROM ClanPointTracker WHERE discordUserID = $1"
                member_clan_point_data = await connection.fetch(sql, member.id)

                if len(member_clan_point_data) != 0:
                    sql = "UPDATE ClanPointTracker SET currentClanRoleID = $1, currentClanName = $2 WHERE discordUserID = $3"
                    await connection.execute(sql, 0, "NONE", member.id)
                    await connection.commit()

            for role in role_config_list:
                await member.remove_roles(role)

        await discord.Role.delete(clan_role)
        