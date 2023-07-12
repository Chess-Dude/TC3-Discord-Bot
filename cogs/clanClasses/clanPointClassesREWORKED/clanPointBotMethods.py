import discord

class ClanPointBotMethods():
     
    async def get_updated_leaderboards(
        self, 
        bot
    ):
        async with bot.pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointLeaderboard ORDER BY weeklyClanPoints DESC"
            clan_leaderboard_rows = await connection.fetch(sql)
            weekly_lb_desc = ''

            for clan_row in clan_leaderboard_rows:
                weekly_lb_desc += f"**{clan_row[1]}** - ``{clan_row[3]}``\n"

            weekly_lb_embed = discord.Embed(
                title="Weekly Leaderboard",
                description=weekly_lb_desc,
                color=0x2f3136
            )

            sql = "SELECT * FROM ClanPointLeaderboard ORDER BY yearlyClanPoints DESC"
            clan_leaderboard_rows = await connection.fetch(sql)
            yearly_lb_desc = ''
            for clan_row in clan_leaderboard_rows:
                yearly_lb_desc += f"**{clan_row[1]}** - ``{clan_row[4]}``\n"

            yearly_lb_embed = discord.Embed(
                title="Yearly Leaderboard",
                description=yearly_lb_desc,
                color=0x2f3136
            )

            embeds_list = [weekly_lb_embed, yearly_lb_embed]
            return embeds_list


    async def get_end_of_round_bonus(
        self,
        bot
    ):
        async with bot.pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointSubmissionTracker"
            results = await connection.fetch(sql)

            delete_sql = "DELETE FROM ClanPointSubmissionTracker"
            await connection.execute(delete_sql)

        return results


    async def send_log_embed(
        self,
        end_of_round_bonus_list,
        bot,
        total_clan_points
    ):
        async with bot.pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointTracker WHERE robloxUsername = $1"
            user_clan_point_data = await connection.fetch(sql, end_of_round_bonus_list[0]) # "YoItzSamBoi" replace this with the end_of_round_bonus_list[0] for testing purposes
            print(user_clan_point_data)
            print(user_clan_point_data[0][1])
            clan_member = bot.get_user(user_clan_point_data[0][2])
            TC3_SERVER = bot.get_guild(350068992045744141)
            clan_point_subs_channel = bot.get_channel(1122622489974034434)

            log_embed = discord.Embed(
                title=f"{user_clan_point_data[0][1]} Clan Point Submission",
                description="Submission originates from in-game",
                color=0x2f3136
            )
            
            log_embed.set_author(
                name=f"{user_clan_point_data[0][2]}",
                icon_url=clan_member.display_avatar.url
            )

            log_embed.set_footer(
                text=f"The Conquerors 3 • Clan Point Submission",
                icon_url=TC3_SERVER.icon
            )

            log_embed.add_field(
                name=f"Clan Of Member:",
                value=f"``{user_clan_point_data[0][5]}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Total Damage Dealt Bonus:",
                value=f"``{end_of_round_bonus_list[3]}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Total Damage Healed Bonus:",
                value=f"``{end_of_round_bonus_list[4]}``",
                inline=False
            )

            if end_of_round_bonus_list[-2].lower() == "survival":
                log_embed.add_field(
                    name=f"Total Waves Survived Bonus:",
                    value=f"``{end_of_round_bonus_list[-3]}``",
                    inline=False
                )

            log_embed.add_field(
                name=f"Total Victory Bonus:",
                value=f"``{end_of_round_bonus_list[2]}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Game Mode:",
                value=f"``{end_of_round_bonus_list[-2]}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Total Clan Points:",
                value=f"``{total_clan_points}``",
                inline=False
            )

            await clan_point_subs_channel.send(embed=log_embed)