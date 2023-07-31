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
