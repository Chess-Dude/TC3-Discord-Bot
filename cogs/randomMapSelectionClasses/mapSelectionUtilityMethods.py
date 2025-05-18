import discord, json, random
import requests
from bs4 import BeautifulSoup
import time

class MapSelectionUtilityMethods():
    map_data = {}
    available_gamemodes = {'Conquest':'Conquest', 'Free_for_All':'Free For All', 'King_of_the_Hill':'King Of The Hill', 'Survival':'Survival'}
    gamemodes = ['1v1','2v2','3v3','4v4','5v5','2v2v2','3v3v3', 'FFA3', 'FFA4', 'FFA6', 'Survival']
    lowercase_game_modes = {}
    lowercase_map_names = {}
    all_map_names = []
    
    @staticmethod
    def load_map_data():
        """Loads map data from the JSON file"""
        try:
            with open('mapList.json', 'r') as json_file:
                content = json_file.read().strip()
                if not content:
                    raise ValueError("Empty JSON file")
                MapSelectionUtilityMethods.map_data = json.loads(content)
                MapSelectionUtilityMethods.all_map_names = list(MapSelectionUtilityMethods.map_data.keys())
                MapSelectionUtilityMethods.lowercase_map_names = {map_name.lower(): map_name for map_name in MapSelectionUtilityMethods.map_data.keys()}
                MapSelectionUtilityMethods.lowercase_game_modes = {gamemode.lower(): gamemode for gamemode in MapSelectionUtilityMethods.gamemodes}
                print(f"Map data file loaded successfully with {len(MapSelectionUtilityMethods.map_data)} maps.")
                return True
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            print(f"Map data file not found or invalid: {e}. Will need to scrape data.")
            MapSelectionUtilityMethods.map_data = {}
            MapSelectionUtilityMethods.all_map_names = []
            MapSelectionUtilityMethods.lowercase_map_names = {}
            MapSelectionUtilityMethods.lowercase_game_modes = {gamemode.lower(): gamemode for gamemode in MapSelectionUtilityMethods.gamemodes}
            return False

    @staticmethod
    def extract_text_data(soup, data_source):
        div = soup.find('div', class_='pi-item pi-data pi-item-spacing pi-border-color', attrs={'data-source': data_source})
        if div and (value_div := div.find('div', class_='pi-data-value')):
            return value_div.get_text(strip=True)
        return None
    
    @staticmethod
    def get_map_data():
        """Scrapes map data from The Conquerors wiki without threading"""
        print("Starting web scraping for map data...")
        start_time = time.time()
        MapSelectionUtilityMethods.map_data = {}
        session = requests.Session()


        try:
            response = session.get("https://theconquerors.fandom.com/wiki/Category:Maps")
            soup = BeautifulSoup(response.content, "html.parser")
            map_links = soup.find_all('a', class_='category-page__member-link')
            map_names = [link.get_text(strip=True) for link in map_links]
            print(f"Found {len(map_names)} maps in category page")
        except Exception as e:
            print(f"Error retrieving map list: {e}")
            return MapSelectionUtilityMethods.map_data

        for map_name in map_names:
            MapSelectionUtilityMethods.map_data[map_name] = {
                'max_income': None,
                'map_size': None,
                'gamemode': {},
                'image': None
            }

        for map_name in map_names:
            try:
                map_url = f"https://theconquerors.fandom.com/wiki/{map_name.replace(' ', '_')}"
                response = session.get(map_url)
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, "html.parser")
                
                thumbnail = soup.find('img', class_='pi-image-thumbnail')
                if thumbnail:
                    image_url = thumbnail.get('data-src') or thumbnail.get('src')
                    MapSelectionUtilityMethods.map_data[map_name]['image'] = image_url

                MapSelectionUtilityMethods.map_data[map_name]['map_size'] = extract_text_data(soup, 'size')
                MapSelectionUtilityMethods.map_data[map_name]['max_income'] = extract_text_data(soup, 'max_eco')
                
            except Exception as e:
                print(f"Error processing map {map_name}: {e}")

        for gamemode_page_name, display_name in MapSelectionUtilityMethods.available_gamemodes.items():
            try:
                gamemode_url = f"https://theconquerors.fandom.com/wiki/{gamemode_page_name}"
                response = session.get(gamemode_url)
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Skip Survival as it has a different layout
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
                            if not row_data or len(row_data) < 1:
                                continue
                            
                            map_name = row_data[0].get_text(strip=True)
                            
                            if map_name in MapSelectionUtilityMethods.map_data:
                                if display_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                                    MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name] = []
                                
                                if sub_gamemode_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name]:
                                    MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name].append(sub_gamemode_name)
                else:
                    # Handle Survival mode specifically
                    survival_table = soup.find("tbody")
                    if not survival_table:
                        continue
                        
                    table_rows = survival_table.find_all("tr")
                    for row in table_rows[1:]:  # skip header
                        row_data = row.find_all("td")
                        if not row_data or len(row_data) < 1:
                            continue
                        
                        map_name = row_data[0].get_text(strip=True)
                        
                        if map_name in MapSelectionUtilityMethods.map_data:
                            if display_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                                MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name] = []
                            
                            if "Survival" not in MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name]:
                                MapSelectionUtilityMethods.map_data[map_name]['gamemode'][display_name].append("Survival")
            
            except Exception as e:
                print(f"Error processing gamemode {gamemode_page_name}: {e}")
        
        # Step 4: As a fallback, check category pages for each gamemode
        for gamemode in MapSelectionUtilityMethods.gamemodes:
            try:
                category_url = f"https://theconquerors.fandom.com/wiki/Category:{gamemode}"
                response = session.get(category_url)
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, "html.parser")
                map_links = soup.find_all('a', class_='category-page__member-link')
                
                for link in map_links:
                    map_name = link.get_text(strip=True)
                    
                    if map_name in MapSelectionUtilityMethods.map_data:
                        gamemode_type = "Conquest"
                        if "FFA" in gamemode:
                            gamemode_type = "Free For All"
                        elif "Survival" in gamemode:
                            gamemode_type = "Survival"
                        
                        if gamemode_type not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                            MapSelectionUtilityMethods.map_data[map_name]['gamemode'][gamemode_type] = []
                        
                        if gamemode not in MapSelectionUtilityMethods.map_data[map_name]['gamemode'][gamemode_type]:
                            MapSelectionUtilityMethods.map_data[map_name]['gamemode'][gamemode_type].append(gamemode)
                            
            except Exception as e:
                print(f"Error processing gamemode category {gamemode}: {e}")
        
        MapSelectionUtilityMethods.all_map_names = list(MapSelectionUtilityMethods.map_data.keys())
        
        elapsed = time.time() - start_time
        print(f"Web scraping completed in {elapsed:.2f} seconds. Found {len(MapSelectionUtilityMethods.map_data)} maps.")
        return MapSelectionUtilityMethods.map_data

    @staticmethod
    def update_map_data():
        """Saves map data to a JSON file"""
        try:
            with open('mapList.json', 'w') as json_file:
                json.dump(MapSelectionUtilityMethods.map_data, json_file, indent=4, sort_keys=True)
            print(f"Map data saved to mapList.json ({len(MapSelectionUtilityMethods.map_data)} maps)")
            return True
        except Exception as e:
            print(f"Error saving map data: {e}")
            return False

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
        """Creates a Discord embed with map information"""
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
        """Returns a Discord embed with a random map of the given game mode"""
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

def update_load_map_data(force_update=False):
    old_count = len(MapSelectionUtilityMethods.map_data)
    
    if not force_update and MapSelectionUtilityMethods.load_map_data():
        print("Using existing map data from file.")
    else:
        print("Scraping new map data from wiki...")
        MapSelectionUtilityMethods.get_map_data()
        MapSelectionUtilityMethods.update_map_data()
    
    MapSelectionUtilityMethods.lowercase_map_names = {
        map_name.lower(): map_name for map_name in MapSelectionUtilityMethods.map_data.keys()
    }
    MapSelectionUtilityMethods.lowercase_game_modes = {
        gamemode.lower(): gamemode for gamemode in MapSelectionUtilityMethods.gamemodes
    }
    
    new_count = len(MapSelectionUtilityMethods.map_data)
    return new_count, old_count