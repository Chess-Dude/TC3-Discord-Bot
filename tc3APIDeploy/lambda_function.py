import os, json
import psycopg2
from dotenv import load_dotenv

class ClanPointAPIMethods():
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

        print(f"The Game mode: {game_mode}, type: {type(game_mode)}")
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

        elif ((game_mode.lower() == "freeforall")  
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
   

    def add_clan_points(
        self,
        end_of_round_bonus_dict,
        mydb,
        cursor,
        clan_points_to_add
    ):
        sql = "SELECT * FROM ClanPointTracker WHERE robloxUsername = %s"
        cursor.execute(sql, (end_of_round_bonus_dict["robloxUsername"],))
        user_clan_point_data = cursor.fetchall()

        if len(user_clan_point_data) != 0:
            sql = "UPDATE ClanPointTracker SET totalClanPoints = totalClanPoints + %s WHERE robloxUsername = %s"
            cursor.execute(sql, (clan_points_to_add, end_of_round_bonus_dict["robloxUsername"]))

            user_clan_name = user_clan_point_data[0][-1]

            if user_clan_name != "None":
                sql = "UPDATE ClanPointLeaderboard SET weeklyClanPoints = weeklyClanPoints + %s, yearlyClanPoints = yearlyClanPoints + %s WHERE clanName = %s"
                cursor.execute(sql, (clan_points_to_add, clan_points_to_add, user_clan_name))

            mydb.commit()


load_dotenv()

clan_point_api_methods_obj = ClanPointAPIMethods()
mydb = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=str(os.getenv("DB_PORT")),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD")
)
cursor = mydb.cursor()
def process_request(event, context):
    if event["httpMethod"] == "POST":
        content_type = event["headers"].get("Content-Type")
        if content_type == "application/json":
            json_data = json.loads(event["body"])

            if len(json_data) != 0:
                total_clan_points = clan_point_api_methods_obj.calculate_total_clan_points(
                    end_of_round_bonus_dict=json_data
                )

                clan_point_api_methods_obj.add_clan_points(
                    end_of_round_bonus_dict=json_data,
                    mydb=mydb,
                    cursor=cursor,
                    clan_points_to_add=total_clan_points
                )

                sql = "INSERT INTO ClanPointSubmissionTracker (endOfRoundBonusString) VALUES (%s)"
                val = (str(json_data),)
                cursor.execute(sql, val)
                mydb.commit()
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(json_data)
            }
        else:
            return {
                "statusCode": 400,
                "body": "Content-Type not supported!"
            }
    else:
        return {
            "statusCode": 405,
            "body": "This API does not support GET requests"
        }
