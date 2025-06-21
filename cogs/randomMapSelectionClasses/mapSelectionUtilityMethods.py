import discord, json, random
import time
import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar

def get_text_data(soup, search_text, child_index=3):
    try:
        parent = soup.find(string=lambda text: text and search_text.lower() in text.lower()).parent.parent
        children = list(parent)
        return children[child_index].get_text(strip=True)
    except (AttributeError, IndexError):
        return "Not found"

def get_category_links(search_text, parent_element):
    try:
        section = parent_element.find(string=lambda text: text and search_text.lower() in text.lower()).parent.parent
        links = section.find_all('a', class_='newcategory')
        return [link.get_text(strip=True) for link in links]
    except AttributeError:
        return []

def get_map_data():
    map_data = {}
    map_names = []

    session = requests.Session()
    
    # Get all map names from category page
    response = session.get(f"https://theconquerors.fandom.com/wiki/Category:Maps")
    if response.status_code != 200:
        print(f"Failed to load page /wiki/Category:Maps")
        return map_data
    
    soup = BeautifulSoup(response.content, "html.parser")
    maps = soup.find_all('a', class_='category-page__member-link')
    
    for link in maps:
        if isinstance(link, str):
            continue
        href = link.get('href')
        index = href.rfind('/') + 1
        map_name = href[index:]
        map_names.append(map_name)

    with alive_bar(len(maps)) as bar:


        text_fields = {
            'map_size': 'size',
            'date_created': 'data created',
            'max_income': 'max eco',
            'oil_spots': 'total oil spots',
            'total_crystals': 'total crystals',
            'chokepoints': 'chokepoints',
            'symmetrical': 'symmetrical'
        }

        # Visit each map page
        for map_name in map_names:
            bar.text = f'Scraping: {map_name}'
            response = requests.get(f"https://theconquerors.fandom.com/wiki/{map_name}")
            
            if response.status_code != 200:
                print(f"Failed to load wiki page for Map Name: {map_name}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
        
            current_map = {
                'gamemode': {},
                'image': '',
                'map_types': [],
                'map_size': '',
                'date_created': '',
                'max_income': '',
                'oil_spots': '',
                'total_crystals': '',
                'chokepoints': '',
                'symmetrical': ''
            }

            # Get image
            try:
                image_data = soup.find_all('img')[2]
                current_map['image'] = image_data.get('src', '')
            except (IndexError, AttributeError):
                current_map['image'] = ''

            # Extract all text fields
            for field_name, search_text in text_fields.items():
                data = get_text_data(soup, search_text)

                # fix formatting
                if field_name in ['oil_spots', 'total_crystals']:
                    string = data.strip()
                    data = string[:2]

                current_map[field_name] = data

            # Get General section for map types
            general_parent = soup.find(string=lambda text: text and "general" in text.lower()).parent.parent
            map_types = get_category_links("Map Type", general_parent)

            current_map['map_types'] = map_types

            # Get gameplay section for gamemodes and alliances
            try:
                gameplay_parent = soup.find(string=lambda text: text and "gameplay" in text.lower()).parent.parent
                
                # gamemodes
                gamemodes = get_category_links("gamemodes", gameplay_parent)
                if 'Conquest' in gamemodes:
                    gamemodes.remove('Lightning Conquest')
                if 'FFA' in gamemodes:
                    gamemodes.remove('Lightning FFA')
                    gamemodes[gamemodes.index('FFA')] = 'Free For All'
                # stupid wiki person named it 'KOTH' instead King Of The Hill
                if 'KOTH' in gamemodes:
                    gamemodes.remove('KOTH')
                    gamemodes.append('King Of The Hill')


                # Convert from list to dict
                gamemodes = {gamemode: [] for gamemode in gamemodes}
                current_map['gamemode'] = gamemodes
                
                # alliances
                current_map['alliances'] = get_category_links("alliance sizes", gameplay_parent)
                
            except AttributeError:
                print(f"Could not find gameplay section for {map_name}")

            # Finicky magic to get the alliances into the gamemode structure. 
            # Edge cases: 
            #             - Survival #vAI
            #             - Free build
            #             - FFA2 (1v1)
            alliances = current_map['alliances']
            for alliance in alliances:
                if alliance == 'FFA2':
                    current_map['gamemode']['Free For All'].append('1v1')
                elif 'AI' in alliance: # Eg: 6vAI for Survival from wiki
                    current_map['gamemode']['Survival'].append(alliance)
                elif 'FFA' in alliance:
                    current_map['gamemode']['Free For All'].append(alliance)
                elif 'KOTH' in alliance: # I hate you wiki person
                    alliance = alliance.replace(' (KOTH)', '')
                    current_map['gamemode']['King Of The Hill'].append(alliance)
                else:
                    # From what ive seen the Territory Conquest maps are seperate.
                    try:
                        if 'Territory Conquest' in current_map['gamemode']:
                            current_map['gamemode']['Territory Conquest'].append(alliance)
                        else:
                            current_map['gamemode']['Conquest'].append(alliance)
                    except Exception as e:
                        print(e, current_map, alliance, map_name)
                        exit()



            # Account for free build alliance size
            if 'Free Build' in current_map['gamemode']:
                # just find the highest gamemode and double it. If it has AI included it it, dont double it
                alliances.sort()
                highest = alliances[0]
                if 'FFA' in highest:
                    highest = highest[3]
                elif 'AI' in highest:
                    highest = alliance[0] # 8vAI
                else:
                    highest = str(int(highest[0])*2) # 4v4  (for example)
                current_map['gamemode']['Free Build'].append(f'FFA{highest}')

            del current_map['alliances']

            map_data[map_name] = current_map
            time.sleep(0.001)
            bar()
    
    return map_data


class MapSelectionUtilityMethods():
    map_data = {} # cache of the map data
    gamemodes = ['1v1','2v2','3v3','4v4','5v5','2v2v2','3v3v3', 'FFA3', 'FFA4', 'FFA6', 'Survival', 'Free Build']
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
                print(f"Map data file loaded successfully with {len(MapSelectionUtilityMethods.map_data)} maps.")
                return True
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            print(f"Map data file not found or invalid: {e}. Will need to scrape data.")
            MapSelectionUtilityMethods.map_data = {}
            MapSelectionUtilityMethods.all_map_names = []
            return False
    
    @staticmethod
    def scrape_map_data():
        t_i = time.time()

        map_data = get_map_data()
        MapSelectionUtilityMethods.map_data = map_data

        t_f = time.time()
        print(f'Scanned: {len(MapSelectionUtilityMethods.map_data)} maps.')
        

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
        MapSelectionUtilityMethods.scrape_map_data()
        MapSelectionUtilityMethods.update_map_data()
    
    new_count = len(MapSelectionUtilityMethods.map_data)
    return new_count, old_count