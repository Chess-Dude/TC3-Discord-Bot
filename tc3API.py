import os
import psycopg2
from flask import Flask, render_template, request
from dotenv import load_dotenv
from cogs.clanClasses.clanPointClassesREWORKED.clanPointAPIMethods import ClanPointAPIMethods

load_dotenv()

clan_point_api_methods_obj = ClanPointAPIMethods()
mydb = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD")
)

cursor = mydb.cursor()

app = Flask(__name__)

@app.route('/', methods=["POST"])
async def process_request():
    if request.method == "POST":
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            json_data = request.json

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
            
            return json_data
        
        else:
            return "Content-Type not supported!"
   
    else:
        return "This API does not support GET requests"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="1111", debug=False)
