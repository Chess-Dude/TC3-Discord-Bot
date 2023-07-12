from .clanRoleCreation import ClanRoleCreation
import discord, re


class ReviewClanApplication(discord.ui.View):
    def __init__(
        self, 
        pool
    ):
        self.pool = pool
        super().__init__(timeout=None)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji='✅', custom_id="persistent_view:approve_clan_app")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"loading...")

        log_embed_message =  interaction.message
        log_embed = log_embed_message.embeds[0].to_dict()
        log_embed_fields = log_embed['fields']
        create_role_field = log_embed_fields[-1]
        info_str = create_role_field["value"]

        clan_name = info_str.split('"')[1]
        copy_info_str = info_str.replace(clan_name, '', 1)
        clan_roster_str = re.sub(r'[^\d\s]+', '', copy_info_str)
        clan_roster_str = clan_roster_str.strip()
        clan_roster_list = clan_roster_str.split(' ')
        del clan_roster_list[-1]

        clan_hex_color = info_str[-len("#36393E"):-1]

        clan_leader = interaction.guild.get_member(int(clan_roster_list[0]))
        clan_co_leader = interaction.guild.get_member(int(clan_roster_list[1]))            
        clan_member_1 = interaction.guild.get_member(int(clan_roster_list[2]))            
        clan_member_2 = interaction.guild.get_member(int(clan_roster_list[3]))            
        clan_member_3 = interaction.guild.get_member(int(clan_roster_list[4]))            
        clan_member_4 = interaction.guild.get_member(int(clan_roster_list[5]))
        role_divider_id = 1053050572296704000    
        clan_leader_role_id = 1054999374993817700 
        clan_co_leader_role_id = 1054999381029429349 

        async with self.pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointLeaderboard WHERE clanName = $1"
            clan_name_data = await connection.fetch(sql, clan_name)

            if len(clan_name_data) == 0:            
                clan_roster_list = [clan_leader, clan_co_leader, clan_member_1, clan_member_2, clan_member_3, clan_member_4]
                clan_hex_color = discord.Color.from_str(clan_hex_color)

                clan_role = await ClanRoleCreation.create_role(
                    self, 
                    interaction, 
                    role_name=clan_name, 
                    colour=clan_hex_color, 
                    role_divider_id=role_divider_id
                )

                await ClanRoleCreation.assign_roles(
                    self, 
                    interaction=interaction, 
                    clan_roster=clan_roster_list, 
                    clan_role=clan_role,
                    clan_leader_role_id=clan_leader_role_id, 
                    clan_co_leader_role_id=clan_co_leader_role_id, 
                )

                sql = "INSERT INTO ClanPointLeaderboard (clanName, clanRoleID, weeklyClanPoints, yearlyClanPoints) VALUES ($1, $2, $3, $4)"
                values = (clan_role.name, int(clan_role.id), 0, 0)
                await connection.execute(sql, *values)

                await interaction.channel.send(f"{interaction.user.mention} Created ``{clan_role.mention}``")

                for clan_member in clan_roster_list:
                    sql = "SELECT * FROM ClanPointTracker WHERE discordUserID = $1"
                    member_clan_point_data = await connection.fetch(sql, clan_member.id)

                    if len(member_clan_point_data) == 0:
                        sql = "INSERT INTO ClanPointTracker (robloxUsername, discordUserID, totalClanPoints, currentClanRoleID, currentClanName) VALUES ($1, $2, $3, $4, $5)"
                        values = (clan_member.nick, clan_member.id, 0, clan_role.id, clan_role.name)
                        inserted_row = await connection.execute(sql, *values)

                    else:
                        sql = "UPDATE ClanPointTracker SET currentClanRoleID = $1, currentClanName = $2 WHERE discordUserID = $3"
                        values = (clan_role.id, clan_role.name, clan_member.id)
                        await connection.execute(sql, *values)

            else:
                response_embed = discord.Embed(
                    title=f"{clan_name} already exists. Ask the applicant to choose another name.",
                    color=0x00ffff
                )
                await interaction.channel.send(
                    embed=response_embed
                )    

        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='❌', custom_id="persistent_view:reject_clan_app")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message(content=f"Rejected by: {interaction.user.mention}")
