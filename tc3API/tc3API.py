import os, json, psycopg2
from dotenv import load_dotenv
from clanPointAPIMethods import ClanPointAPIMethods

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

            end_of_round_bonus_list = clan_point_api_methods_obj.get_player_data(
                raw_player_data=json_data
            )

            if len(end_of_round_bonus_list) != 0:
                total_clan_points = clan_point_api_methods_obj.calculate_total_clan_points(
                    end_of_round_bonus_list=end_of_round_bonus_list
                )

                clan_point_api_methods_obj.add_clan_points(
                    end_of_round_bonus_list=end_of_round_bonus_list,
                    mydb=mydb,
                    cursor=cursor,
                    clan_points_to_add=total_clan_points
                )
                sql = "INSERT INTO ClanPointSubmissionTracker (endOfRoundBonusString) VALUES (%s)"
                val = (str(end_of_round_bonus_list),)
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
