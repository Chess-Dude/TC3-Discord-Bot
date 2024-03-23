import discord

class ClanPointBotMethods():
    def calculate_total_clan_points(
        self,
        end_of_round_bonus_dict
    ):
        victory_bonus = int(end_of_round_bonus_dict["victoryBonus"])
        damage_dealt_bonus = int(end_of_round_bonus_dict["damageDealtBonus"])
        damage_healed_bonus = int(end_of_round_bonus_dict["damageHealedBonus"])
        waves_survived_bonus = int(end_of_round_bonus_dict["wavesSurvivedBonus"])
        game_mode = end_of_round_bonus_dict["gameMode"]
        end_time = int(end_of_round_bonus_dict["endTime"])
        game_mode_multiplier = 0

        if ((game_mode.lower() == "conquest") and 
            (end_time >= 1200)):
                game_mode_multiplier = 2
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

        elif ((game_mode.lower() == "lightningconquest") and 
            (end_time >= 900)):
                game_mode_multiplier = 1.5
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15


        elif ((game_mode.lower() == "territoryconquest") or 
            (game_mode.lower() == "tc") and 
            (end_time >= 1200)):
                game_mode_multiplier = 1
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

        elif ((game_mode.lower() == "survival") and 
            (end_time >= 1200)):
                game_mode_multiplier = 1
                game_mode_cap = 250

        elif ((game_mode.lower() == "kingofthehill") or 
            (game_mode.lower() == "koth") and 
            (end_time >= 1200)):
                game_mode_multiplier = 1.5
                game_mode_cap = 90

        elif ((game_mode.lower() == "free for all")  
            (game_mode.lower() == "ffa") and 
            (end_time >= 1200)):
                game_mode_multiplier = 2
                game_mode_cap = 300

        else:
            print("Following game mode not handled:")
            print(game_mode)

        total_clan_points = 0
        if game_mode_multiplier != 0:
            total_clan_points = damage_dealt_bonus + damage_healed_bonus + victory_bonus + waves_survived_bonus
                        
            total_clan_points = int(total_clan_points) * int(game_mode_multiplier)

            if (int(total_clan_points) > int(game_mode_cap)):
                total_clan_points = game_mode_cap

        return total_clan_points

    async def get_updated_leaderboards(
        self, 
        bot
    ):
        async with bot.pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointLeaderboard ORDER BY weeklyClanPoints DESC"
            clan_leaderboard_rows = await connection.fetch(sql)
            weekly_lb_desc = ''

            for clan_row in clan_leaderboard_rows:
                if int(clan_row[3]) != 0:
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
                if int(clan_row[3]) != 0:
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

    async def get_user_clan_point_data(
        self,
        bot,
        end_of_round_bonus_dict
    ):
        async with bot.pool.acquire() as connection:
            sql = "SELECT * FROM ClanPointTracker WHERE robloxUsername = $1"
            user_clan_point_data = await connection.fetch(sql, end_of_round_bonus_dict["robloxUsername"]) # "YoItzSamBoi" replace this with the end_of_round_bonus_list[0] for testing purposes

            return user_clan_point_data

    async def send_log_embed(
        self,
        end_of_round_bonus_dict,
        bot,
        total_clan_points,
        user_clan_point_data,
        channel_id
    ):
        TC3_SERVER = bot.get_guild(350068992045744141)
        clan_point_subs_channel = bot.get_channel(channel_id)

        if (len(user_clan_point_data) != 0) and (str(user_clan_point_data[0][5]) != "None"):
            clan_member = bot.get_user(user_clan_point_data[0][2])
            log_embed = discord.Embed(
                title=f"{user_clan_point_data[0][1]} Clan Point Submission",
                description="Submission originates from in-game",
                color=0x2f3136
            )
            try:    
                log_embed.set_author(
                    name=f"{user_clan_point_data[0][2]}",
                    icon_url=clan_member.display_avatar.url
                )
            except:
                pass

            log_embed.add_field(
                name=f"Clan Of Member:",
                value=f"``{user_clan_point_data[0][5]}``",
                inline=False
            )

        else:
            log_embed = discord.Embed(
                title=f"TC3 Game Submission",
                description="Submission originates from in-game",
                color=0x2f3136
            )

            value = end_of_round_bonus_dict["robloxUsername"]
            
            log_embed.set_author(
                name=f"{value}",
                icon_url=TC3_SERVER.icon
            )

            log_embed.add_field(
                name=f"Clan Of Member:",
                value=f"``NO CLAN``",
                inline=False
            )

        log_embed.set_footer(
            text=f"The Conquerors 3 • Clan Point Submission",
            icon_url=TC3_SERVER.icon
        )

        value = end_of_round_bonus_dict["damageDealtBonus"]
        log_embed.add_field(
            name=f"Total Damage Dealt Bonus:",
            value=f"``{value}``",
            inline=False
        )

        value = end_of_round_bonus_dict["damageHealedBonus"]

        log_embed.add_field(
            name=f"Total Damage Healed Bonus:",
            value=f"``{value}``",
            inline=False
        )
        value = end_of_round_bonus_dict["wavesSurvivedBonus"]
        if end_of_round_bonus_dict["gameMode"].lower() == "survival":
            log_embed.add_field(
                name=f"Total Waves Survived Bonus:",
                value=f"``{value}``",
                inline=False
            )

        value = end_of_round_bonus_dict["victoryBonus"]

        log_embed.add_field(
            name=f"Total Victory Bonus:",
            value=f"``{value}``",
            inline=False
        )

        value = end_of_round_bonus_dict["gameMode"]

        log_embed.add_field(
            name=f"Game Mode:",
            value=f"``{value}``",
            inline=False
        )

        value = end_of_round_bonus_dict["endTime"]

        log_embed.add_field(
            name=f"End Timer (Seconds):",
            value=f"``{value}``",
            inline=False
        )

        log_embed.add_field(
            name=f"Total Clan Points:",
            value=f"``{total_clan_points}``",
            inline=False
        )

        await clan_point_subs_channel.send(embed=log_embed)