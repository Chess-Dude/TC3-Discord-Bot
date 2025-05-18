import discord, json, random
import requests
from bs4 import BeautifulSoup

class MapSelectionUtilityMethods():
    map_data = {}
    available_gamemodes = {'Conquest':'Conquest', 'Free_for_All':'Free For All', 'King_of_the_Hill':'King Of The Hill', 'Survival':'Survival'}
    gamemodes = ['1v1','2v2','3v3','4v4','5v5','2v2v2','3v3v3', 'FFA3', 'FFA4', 'FFA6', 'Survival']
    lowercase_game_modes = {}
    lowercase_map_names = {}
    
    @staticmethod
    def load_map_data():
        """Loads map data from the JSON file"""
        try:
            with open('TC3-Discord-Bot/mapList.json', 'r') as json_file:
                MapSelectionUtilityMethods.map_data = json.load(json_file)
                MapSelectionUtilityMethods.lowercase_map_names = {map_name.lower(): map_name for map_name in MapSelectionUtilityMethods.map_data.keys()}
                MapSelectionUtilityMethods.lowercase_game_modes = {gamemode.lower(): gamemode for gamemode in MapSelectionUtilityMethods.gamemodes}
        except FileNotFoundError:
            print("Map data file not found. Initializing with empty data.")
            MapSelectionUtilityMethods.map_data = {}
            MapSelectionUtilityMethods.lowercase_map_names = {}
            MapSelectionUtilityMethods.lowercase_game_modes = {gamemode.lower(): gamemode for gamemode in MapSelectionUtilityMethods.gamemodes}

    @staticmethod
    def get_map_data():
        """Scrapes map data from The Conquerors wiki"""
        MapSelectionUtilityMethods.map_data = {}
        session = requests.Session()
        
        # Process gamemode pages to get map data
        for gamemode_page_name, display_name in MapSelectionUtilityMethods.available_gamemodes.items():
            try:
                response = session.get(f"https://theconquerors.fandom.com/wiki/{gamemode_page_name}")
                if response.status_code != 200:
                    print(f"Failed to retrieve page for {gamemode_page_name}")
                    continue
                    
                soup = BeautifulSoup(response.content, "html.parser")

                if gamemode_page_name != "Survival":
                    wds_tabber_wrapper = soup.find('div', class_='wds-tabs__wrapper')
                    if not wds_tabber_wrapper:
                        continue
                        
                    wds_tabs = wds_tabber_wrapper.find('ul', class_='wds-tabs')
                    if not wds_tabs:
                        continue
                        
                    sub_gamemodes_raw = wds_tabs.find_all('li', class_='wds-tabs__tab')
                    sub_gamemodes = []
                    
                    for sub_gamemode_raw in sub_gamemodes_raw:
                        sub_gamemode = sub_gamemode_raw['data-hash'].strip().replace('_', '')
                        sub_gamemodes.append(sub_gamemode)

                    sub_gamemode_pages = soup.find_all('div', class_='wds-tab__content')
                
                    for sub_gamemode_name, sub_gamemode_page in zip(sub_gamemodes, sub_gamemode_pages):
                        if sub_gamemode_name.endswith('FFA'):
                            sub_gamemode_name = 'FFA' + sub_gamemode_name[0]

                        table_rows = sub_gamemode_page.find_all("tr")
                        for row in table_rows[1:]:
                            row_data = row.find_all("td")
                            if len(row_data) < 4:
                                continue
                                
                            map_name = row_data[0].get_text(strip=True)
                            image_data = row_data[1].find('img')
                            url = image_data.get('data-src', None) or image_data.get('src', None)
                            max_income = row_data[2].get_text(strip=True)
                            map_size = row_data[3].get_text(strip=True)

                            # Create or update map data
                            if map_name not in MapSelectionUtilityMethods.map_data:
                                MapSelectionUtilityMethods.map_data[map_name] = {
                                    'max_income': max_income,
                                    'map_size': map_size,
                                    'gamemode': {},
                                    'image': url
                                }

                            # Add gamemode information
                            if display_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                                MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name] = []

                            # Add sub-gamemode
                            if sub_gamemode_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name]:
                                MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name].append(sub_gamemode_name)

                else:  # Handle Survival mode specifically
                    survival_table = soup.find("tbody")
                    if not survival_table:
                        continue
                        
                    table_rows = survival_table.find_all("tr")
                    for row in table_rows[1:]:
                        row_data = row.find_all("td")
                        if len(row_data) < 4:
                            continue
                            
                        map_name = row_data[0].get_text(strip=True)
                        image_data = row_data[1].find('img')
                        url = image_data.get('data-src', None) or image_data.get('src', None) 
                        max_income = row_data[2].get_text(strip=True)
                        map_size = row_data[3].get_text(strip=True)

                        if map_name not in MapSelectionUtilityMethods.map_data:
                            MapSelectionUtilityMethods.map_data[map_name] = {
                                'max_income': max_income,
                                'map_size': map_size,
                                'gamemode': {},
                                'image': url
                            }

                        # Add survival gamemode information
                        if display_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                            MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name] = []

                        if display_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name]:
                            MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name].append("Survival")
                            
            except Exception as e:
                print(f"Error processing gamemode {gamemode_page_name}: {e}")
                
        MapSelectionUtilityMethods.all_map_names = list(MapSelectionUtilityMethods.map_data.keys())
        
        return MapSelectionUtilityMethods.map_data

    @staticmethod
    def update_map_data():
        """Saves map data to a JSON file"""
        with open('TC3-Discord-Bot\mapList.json', 'w') as json_file:
            json.dump(MapSelectionUtilityMethods.map_data, json_file, indent=4, sort_keys=True)

    @staticmethod
    def get_map_image():
        """Returns a dictionary of map names and their image URLs"""
        maps = {}
        for map_name, data in MapSelectionUtilityMethods.map_data.items():
            maps[map_name] = data.get('image')
        return maps

    @staticmethod
    def determine_map_list(game_mode):
        """Returns a list of maps that support the given game mode"""
        game_mode = game_mode.lower()
        if game_mode == "game_night_3v3":
            maps = ["Basalt Peninsula", "Germany Map", "Lakebed", "Double Mansion", "Fantasy", "Germany vs France", "Korea"]
        else:
            maps = []
            for map_name, map_info in MapSelectionUtilityMethods.map_data.items():
                all_types = []
                for types in map_info['gamemode'].values():
                    all_types.extend(types)
                all_types = [map_type.lower() for map_type in all_types]
                if game_mode in all_types:
                    maps.append(map_name)
        return maps

    @staticmethod
    def create_map_embed(selected_map, map_type, interaction: discord.Interaction):
        map_data = MapSelectionUtilityMethods.map_data[selected_map]
        cost = map_data['max_income']
        map_size = map_data['map_size']
        map_image = map_data.get('image')

        map_embed = discord.Embed(
            title=f"{selected_map} Map Information:",
            description=f"{interaction.user.mention}",
            color=0x00ffff
        )
        
        if map_image:
            map_embed.set_image(url=map_image)

        map_embed.set_author(
            name=f"{interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url)

        map_embed.set_footer(
            text=f"Random {map_type} Map", 
            icon_url=interaction.guild.icon)

        map_embed.timestamp = interaction.created_at
        map_embed.add_field(name="Max Income:", value=cost, inline=True)
        map_embed.add_field(name="Map Size:", value=map_size, inline=True)
        
        return map_embed

    @staticmethod
    def random_map_init(interaction: discord.Interaction, game_mode: str):
        real_name = game_mode
        if game_mode == "1v1":
            real_name = "FFA2"

        maps = MapSelectionUtilityMethods.determine_map_list(game_mode=real_name)
        if not maps:
            return discord.Embed(title="Error", description=f"No maps found for {game_mode} mode", color=0xff0000)
            
        return MapSelectionUtilityMethods.create_map_embed(
            selected_map=random.choice(maps),
            map_type=game_mode,
            interaction=interaction
        )

def update_load_map_data():
    old_count = len(MapSelectionUtilityMethods.map_data)
    MapSelectionUtilityMethods.get_map_data()
    MapSelectionUtilityMethods.update_map_data()
    MapSelectionUtilityMethods.lowercase_map_names = {map_name.lower(): map_name for map_name in MapSelectionUtilityMethods.map_data.keys()}
    MapSelectionUtilityMethods.lowercase_game_modes = {gamemode.lower(): gamemode for gamemode in MapSelectionUtilityMethods.gamemodes}
    return len(MapSelectionUtilityMethods.map_data), old_count
