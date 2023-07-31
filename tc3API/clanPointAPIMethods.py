class ClanPointAPIMethods():
    def get_player_data(
        self,
        raw_player_data
    ):
        
        order = [
            "robloxUsername",
            "victoryBonus",
            "damageDealtBonus",
            "damageHealedBonus",
            "stayedFromBeginningBonus",
            "goodStayingRecordBonus",
            "objectiveCompletedBonus",
            "wavesSurvivedBonus",
            "gameMode",
            "endTime"
        ]

        end_of_round_bonus_list = [raw_player_data[key] for key in order]
        print(end_of_round_bonus_list)
        return end_of_round_bonus_list


    def calculate_total_clan_points(
        self,
        end_of_round_bonus_list
    ):
        victory_bonus = int(end_of_round_bonus_list[1])
        damage_dealt_bonus = int(end_of_round_bonus_list[2])
        damage_healed_bonus = int(end_of_round_bonus_list[3])
        waves_survived_bonus = int(end_of_round_bonus_list[7])
        game_mode = end_of_round_bonus_list[8]
        end_time = int(end_of_round_bonus_list[9])
        game_mode_multiplier = 0

        print(f"The Game mode: {game_mode}, type: {type(game_mode)}")
        if ((game_mode.lower() == "conquest") and 
            (end_time >=20)):
                print("game mode is conquest")
                game_mode_multiplier = 2
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

        elif ((game_mode.lower() == "lightning conquest") and 
            (end_time >=15)):
                game_mode_multiplier = 1.5
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15


        elif ((game_mode.lower() == "territory conquest") or 
            (game_mode.lower() == "tc") and 
            (end_time >= 20)):
                game_mode_multiplier = 1
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

        elif ((game_mode.lower() == "survival") and 
            (end_time >= 20)):
                game_mode_multiplier = 1
                game_mode_cap = 250

        elif ((game_mode.lower() == "king of the hill") or 
            (game_mode.lower() == "koth") and 
            (end_time >= 20)):
                game_mode_multiplier = 1.5
                game_mode_cap = 90

        elif ((game_mode.lower() == "free for all")  
            (game_mode.lower() == "ffa") and 
            (end_time >= 20)):
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
   

    def add_clan_points(
        self,
        end_of_round_bonus_list,
        mydb,
        cursor,
        clan_points_to_add
    ):
        sql = "SELECT * FROM ClanPointTracker WHERE robloxUsername = %s"
        cursor.execute(sql, (end_of_round_bonus_list[0],))
        user_clan_point_data = cursor.fetchall()

        if len(user_clan_point_data) != 0:
            sql = "UPDATE ClanPointTracker SET totalClanPoints = totalClanPoints + %s WHERE robloxUsername = %s"
            cursor.execute(sql, (clan_points_to_add, end_of_round_bonus_list[0]))

            sql = "SELECT * FROM ClanPointTracker WHERE robloxUsername = %s"
            cursor.execute(sql, (end_of_round_bonus_list[0],))
            user_clan_point_data = cursor.fetchall()
            user_clan_name = user_clan_point_data[0][-1]

            sql = "UPDATE ClanPointLeaderboard SET weeklyClanPoints = weeklyClanPoints + %s, yearlyClanPoints = yearlyClanPoints + %s WHERE clanName = %s"
            cursor.execute(sql, (clan_points_to_add, clan_points_to_add, user_clan_name))

            mydb.commit()
