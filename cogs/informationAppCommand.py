import discord, gspread, json, typing, requests
from oauth2client.service_account import ServiceAccountCredentials
from discord import Member, app_commands
from discord.app_commands import Choice
from discord.ext import commands
from cogs.informationChannels import InformationEmbeds
from .mapSelectionClasses.mapSelectionUtilityMethods import MapSelectionUitilityMethods
from bs4 import BeautifulSoup

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Copy of TC3 Unit Information").sheet1

class InformationAppCommands(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    def bots_channels(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914

    is_bots = app_commands.check(bots_channels)
    
    info_group = app_commands.Group(
        name="info",
        description="A Command That Allows You To Get Information On A Certain Object!")

    @info_group.command(
        name="one_day_sign_up", 
        description="A Command That Allows You To Get Information On the One-Day Tournament!")
    async def info_one_day_tournament(
        self, 
        interaction: discord.Interaction, 
    ):      


        message = """
        
__🛑 Rules and Guidelines:__
https://docs.google.com/document/d/1e0JkxBFhv55TkJxCLWxVVBxQByblbZV7Ryw95ILqpCE/edit?usp=sharing\n\n
__🔢 To sign-up for the one-day tournament please follow the steps below:__
1. Verify your roblox account by going to <#351057167706619914> and typing ``/verify``
2. Ping yourself yourself in <#1015670142656581742> (when signups open)
3. Ensure that your level roles are all up to date (use the ``/verify`` command)
"""            
        await interaction.response.send_message(
            content=message
        )

    @is_bots
    @info_group.command(
        name="unit", 
        description="A Command That Allows You To Get Information On A Certain TC3 Unit!!")
    @app_commands.describe(unit="Type The Unit You Would Like Info on...")
    @app_commands.rename(unit="unit")
    async def info_unit(
        self, 
        interaction: discord.Interaction, 
        unit: str
        ):         
            if unit != None:
                input_unit = unit
                data = sheet.get_all_records()
                result_entry = None

                for entry in data:
                    if input_unit.lower() == entry["Unit"].lower() or input_unit.lower() == entry["Unit"].lower().replace(" ", ""):
                        result_entry = entry
                
                if result_entry == None:
                    await interaction.response.send_message(content=f"Error: You did not provide a valid unit. Please try again.", ephemeral=True)

                else:            
                    unit_stats = ["Type", "Produced in", "Cost", "Build Time", "Health", "Damage (DPS)", "Speed", "Range", "Garrisonable", "Garrisons", "Researchable", "Produces", "Unit Slots", "Wiki Link", "Image Link"]
                    info_embed = discord.Embed(
                        title=f'{result_entry["Unit"]}', 
                        description=f'Unit Stats for the {result_entry["Unit"]}', 
                        color=0x00ffff)

                    info_embed.set_author(
                        name=f"{interaction.user.display_name}", 
                        icon_url=f"{interaction.user.display_avatar.url}")

                    info_embed.set_thumbnail(url=f'{result_entry["Image Link"]}')

                    for stat in unit_stats:
                        info_embed.add_field(
                            name=stat, 
                            value = f'{result_entry[stat]}')
                    
                    info_embed.set_footer(
                        text=f"The Conquerors 3 • {input_unit} information",
                        icon_url=interaction.guild.icon
                    )
                    
                    info_embed.timestamp = interaction.created_at
                    
                    await interaction.response.send_message(embed=info_embed)
            
            else:
                await interaction.response.send_message(ephemeral="Please enter a valid unit!")

    @info_unit.autocomplete("unit")
    async def info_unit_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        unit = [
                "Scout",
                "Light Soldier",
                "Heavy Soldier",
                "Repairman",
                "Construction Soldier",
                "Engineer",
                "Anti Air Soldier",
                "Medic",
                "Sniper",
                "Juggernaut",
                "Light Tank", 
                "Heavy Tank",
                "Anti Air Tank",
                "Explosive Tank",
                "Artillery",
                "Light Plane",
                "Heavy Plane",
                "Helicopter",
                "Stealth Bomber",
                "Transport Plane",
                "Space Fighter",
                "Mothership",
                "Gunboat",
                "Destroyer",
                "Battleship",
                "Submarine",
                "Aircraft Carrier",
                "Oil Ship",
                "Transport Ship",
                "Nuclear Missile",
                "Fire Missile",
                "Missile",
                "Medi Truck",
                "Jeep",
                "Humvee",
                "General",
                "Hovercraft",
                "Power Plant",
                "Nuclear Plant",
                "Oil Rig",
                "Barracks",
                "Tank Factory",
                "Airport",
                "Space Link",
                "Naval Shipyard",
                "Nuclear Silo",
                "Fort",
                "Turret",
                "Anti Air Turret",
                "Command Center",
                "Headquarters",
                "Walls",
                "Shield Generator",
                "Landmine",
                "Watermine",
                "Soldier House",
                "Tank House",
                "Plane House",
                "Naval House",
                "Bunker",
                "Construction Yard",
                "Hospital",
                "Research Center",
                "Super Heavy Soldier",
                "Super Heavy Tank",
                "Super Heavy Juggernaut",
                "Super Heavy Plane",
                "Super Mothership",
                "Super Juggernaut"
                ]
        return [
            app_commands.Choice(name=selected_unit, value=selected_unit)
            for selected_unit in unit if current.lower() in selected_unit.lower()
        ][:25]
        
    @is_bots   
    @info_group.command(
        name="map",
        description="Get a map radar")
    @app_commands.describe(map="Pick a map you would like information on!")
    @app_commands.rename(map="map")    
    async def map(
        self, 
        interaction: discord.Interaction,
        map: str
    ):  

        map = map.title()
        map = map.replace(" Vs ", " vs. ")
        map = map.replace(" Vs. ", " vs. ")
        page = requests.get("https://theconquerors.fandom.com/wiki/Category:Maps")

        soup = BeautifulSoup(page.content, "html.parser")
        no = soup.findAll('table', class_="article-table")[0].findAll('tr')
        map_info_dict = {}

        for i in range(len(no)): 
            c = no[i].find_all("th")
            map_info_dict[c[0].text] = []
            for z in range(len(c)):
                map_info_dict[c[0].text].append(c[z].text)

        map_info_list = [] 
        for cur_map in map_info_dict:
            cur_map_name = cur_map.replace("\n", '')
            cur_map_name = cur_map_name.title()
            cur_map_name = cur_map_name.replace(" Vs ", " vs. ")
            cur_map_name = cur_map_name.replace(" Vs. ", " vs. ")
            if ((cur_map_name == map) or 
                (cur_map_name.lower() == map)):
                for value in map_info_dict[cur_map]:
                    value = value.replace("\n", ' ')
                    map_info_list.append(value)

        map_images = MapSelectionUitilityMethods.get_map_image()

        map_embed = discord.Embed(
            title=f"{map} Map Information:", 
            description=f"{interaction.user.mention}", 
            color=0x00ffff
        )
        
        try:
            map_embed.set_image(url=map_images[map.title()])
        
        except KeyError:
            map_embed.set_image(url=map_images[map])
                
        map_embed.set_author(
            name=f"{interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url)
        
        map_embed.set_footer(
            text=f"{map} Map Information", 
            icon_url=interaction.guild.icon)

        map_embed.timestamp = interaction.created_at
        try:
            map_embed.add_field(
                name=f"Mode:",
                value=f"{map_info_list[2]}",
                inline=True
            )

            map_embed.add_field(
                name=f"Map Type:",
                value=f"{map_info_list[3]}",
                inline=True
            )

            map_embed.add_field(
                name=f"Max Income:",
                value=f"{map_info_list[4]}",
                inline=True
            )

            map_embed.add_field(
                name=f"Number Of Crystals:",
                value=f"{map_info_list[5]}",
                inline=True
            )

            map_embed.add_field(
                name=f"Number Of Oil Spots:",
                value=f"{map_info_list[6]}",
                inline=True
            )
            map_embed.add_field(
                name=f"Playable?",
                value=f"{map_info_list[7]}",
                inline=True
            )

        except IndexError:
            map_embed.add_field(
                name=f"Data Unavailable",
                value=f"The TC3 Wiki is out of date. Please check back later.",
                inline=True
            )

        await interaction.response.send_message(
            embed=map_embed
        )

    @map.autocomplete("map")
    async def map_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        map = MapSelectionUitilityMethods.get_map_image()
        map = list(map)
        return [
            app_commands.Choice(name=map_image, value=map_image)
            for map_image in map if current.lower() in map_image.lower()
        ][:25]

    @is_bots
    @info_group.command(
        name="user", 
        description="A Command That Allows You To Get Info On A Discord Member!")
    @app_commands.describe(user="Ping The Member That You Would Like Info On!")
    @app_commands.rename(user="member")    
    async def user(
        self, 
        interaction: discord.Interaction,
        user: discord.Member
        ):
            member = user
            roles = [role for role in member.roles]
            embed = discord.Embed(
                title=f"{member}", 
                colour=0x00ffff, 
                timestamp=interaction.created_at)
            
            embed.set_author(
                name=f"{member.display_name}", 
                icon_url=f"{member.avatar.url}")
            
            embed.set_thumbnail(url=member.avatar.url)
        
            embed.add_field(
                name="Created Account On:", 
                value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(
                name="Joined Server On:", 
                value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(
                name="Roles:", 
                value="".join([role.mention for role in roles[1: ]]), inline=False)
            
            embed.set_footer(
                text=f"User ID: {member.id}")
            
            await interaction.response.send_message(embed=embed)

    @is_bots
    @app_commands.command(
        name="link",
        description="A Command That Allows You To Get A Link To A Site!"
    )
    @app_commands.choices(resource=[
        Choice(name="tc1", value=1),
        Choice(name="tc2", value=2),
        Choice(name="tc3", value=3),
        Choice(name="wiki", value=4),
        Choice(name="twitter", value=5)
    ])    
    async def link_resource(
        self,
        interaction: discord.Interaction,
        resource: Choice[int]
    ):
        if resource.name == "tc1":
            await interaction.response.send_message(content="https://www.roblox.com/games/172585743/")

        elif resource.name == "tc2":
            await interaction.response.send_message(content="https://www.roblox.com/games/13149917/")

        elif resource.name == "tc3":
            await interaction.response.send_message(content="https://www.roblox.com/games/8377997/")

        elif resource.name == "wiki":
            await interaction.response.send_message(content="http://theofficialconquerorswikia.wikia.com/wiki/The_official_conquerors_wiki")

        elif resource.name == "twitter":
            await interaction.response.send_message(content="https://twitter.com/BrokenBoneRBLX\nhttps://twitter.com/ConquerorsRBLX")

    @info_group.command(
        name="matchmaking", 
        description="A Command That Allows You To Get Info On The Matchmaking Channel!")    
    async def matchmaking(
        self, 
        interaction: discord.Interaction
        ):
            await interaction.response.send_message("If you wish to find another member to play TC3 with, please run the ``!!rank game`` command in <#351057167706619914>. This will give you access to the matchmaking channel. Upon gaining access, you may run the ``/play`` command (in the matchmaking channel) to find a fellow player!")

    @info_group.command(
        name="game_night", 
        description="A Command That Allows You To Get Info On The Game Night Tournament!")    
    async def one_day_info(
        self, 
        interaction: discord.Interaction
        ):
            await interaction.response.send_message("__To sign-up for the one-day tournament please follow the steps below:__\n1. Join The Conquering 3 (https://discord.gg/tc3).\n2.Verify your roblox account by going to <#351057167706619914> and typing ``/verify`` (or hitting the 'update my roles' button in <#1026328773341216808>)\n3. Ping yourself in <#1015670142656581742>\n\nPing a event committee member if you need help or have any questions!")

    @info_group.command(
        name="tournaments", 
        description="A Command That Allows You To Get Info On Tournaments!")    
    async def tournament_info(
        self, 
        interaction: discord.Interaction
        ):
            await InformationEmbeds.tournament_embed_info(
                self, 
                interaction
            )

async def setup(bot):
    await bot.add_cog(InformationAppCommands(bot))