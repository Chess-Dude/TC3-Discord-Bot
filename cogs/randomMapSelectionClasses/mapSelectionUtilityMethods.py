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

            # Get image - FIXED: safer extraction
            try:
                images = soup.find_all('img')
                if len(images) > 2:
                    current_map['image'] = images[2].get('src', '')
                else:
                    current_map['image'] = ''
            except (IndexError, AttributeError):
                current_map['image'] = ''

            # Extract all text fields
            for field_name, search_text in text_fields.items():
                data = get_text_data(soup, search_text)

                # FIXED: safer string slicing
                if field_name in ['oil_spots', 'total_crystals']:
                    string = data.strip()
                    if len(string) >= 2:
                        data = string[:2]
                    else:
                        data = string

                current_map[field_name] = data

            # Get General section for map types - FIXED: added error handling
            try:
                general_parent = soup.find(string=lambda text: text and "general" in text.lower()).parent.parent
                map_types = get_category_links("Map Type", general_parent)
                current_map['map_types'] = map_types
            except AttributeError:
                current_map['map_types'] = []

            # Get gameplay section for gamemodes and alliances
            try:
                gameplay_parent = soup.find(string=lambda text: text and "gameplay" in text.lower()).parent.parent
                
                # gamemodes
                gamemodes = get_category_links("gamemodes", gameplay_parent)
                
                # FIXED: Check if items exist before removing
                if 'Lightning Conquest' in gamemodes:
                    gamemodes.remove('Lightning Conquest')
                if 'Lightning FFA' in gamemodes:
                    gamemodes.remove('Lightning FFA')
                if 'FFA' in gamemodes:
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
                current_map['gamemode'] = {}
                current_map['alliances'] = []

            # FIXED: Safer alliance processing
            alliances = current_map.get('alliances', [])
            for alliance in alliances:
                if alliance == 'FFA2':
                    if 'Free For All' not in current_map['gamemode']:
                        current_map['gamemode']['Free For All'] = []
                    current_map['gamemode']['Free For All'].append('1v1')
                elif 'AI' in alliance:
                    if 'Survival' not in current_map['gamemode']:
                        current_map['gamemode']['Survival'] = []
                    current_map['gamemode']['Survival'].append(alliance)
                elif 'FFA' in alliance and alliance != 'FFA2':
                    if 'Free For All' not in current_map['gamemode']:
                        current_map['gamemode']['Free For All'] = []
                    current_map['gamemode']['Free For All'].append(alliance)
                elif 'KOTH' in alliance:
                    alliance = alliance.replace(' (KOTH)', '')
                    if 'King Of The Hill' not in current_map['gamemode']:
                        current_map['gamemode']['King Of The Hill'] = []
                    current_map['gamemode']['King Of The Hill'].append(alliance)
                else:
                    if 'Territory Conquest' in current_map['gamemode']:
                        current_map['gamemode']['Territory Conquest'].append(alliance)
                    else:
                        if 'Conquest' not in current_map['gamemode']:
                            current_map['gamemode']['Conquest'] = []
                        current_map['gamemode']['Conquest'].append(alliance)

            # FIXED: Free build logic bug
            if 'Free Build' in current_map['gamemode']:
                if alliances:
                    alliances.sort()
                    highest = alliances[0]
                    if 'FFA' in highest:
                        highest = highest[3] if len(highest) > 3 else "6"
                    elif 'AI' in highest:
                        highest = highest[0] if highest else "6"  # FIXED: was 'alliance[0]'
                    else:
                        try:
                            highest = str(int(highest[0])*2)
                        except (ValueError, IndexError):
                            highest = "6"  # Fallback
                    current_map['gamemode']['Free Build'].append(f'FFA{highest}')

            # Clean up
            if 'alliances' in current_map:
                del current_map['alliances']

            map_data[map_name] = current_map
            time.sleep(0.001)
            bar()

    print(f'Scanned: {len(map_data)} maps.')
    return map_data


def get_all_gamemodes(map_data):
    all_modes = set()
    for map_info in map_data.values():
        for alliances in map_info.get('gamemode', {}).values():
            all_modes.update(alliances)
    return sorted(list(all_modes))

def save_map_data(map_data):
    """Saves map data to a JSON file"""
    try:
        with open('mapList.json', 'w') as json_file:
            json.dump(map_data, json_file, indent=4, sort_keys=True)
        print(f"Map data saved to mapList.json ({len(map_data)} maps)")
        return True
    except Exception as e:
        print(f"Error saving map data: {e}")
        return False
    
def scrape_map_data():
    map_data = get_map_data()
    save_map_data(map_data)
    return map_data

def load_map_data():
    """Loads map data from the JSON file, scrapes if needed"""
    try:
        with open('mapList.json', 'r') as json_file:
            content = json_file.read().strip()
            if not content:
                raise ValueError("Empty JSON file")
            map_data = json.loads(content)
            print(f"Map data file loaded successfully with {len(map_data)} maps.")
            return map_data
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"Map data file not found or invalid: {e}. Will scrape data.")
        return scrape_map_data()


class MapSelectionUtilityMethods():
    map_data = load_map_data()
    all_map_names = list(map_data.keys())
    gamemodes = get_all_gamemodes(map_data)

    @staticmethod
    def determine_map_list(game_mode: str):
        """Returns a list of maps that support the given game mode"""
        game_mode = game_mode.lower()
        if game_mode == "game_night_3v3":
            maps = ["Basalt Peninsula", "Germany Map", "Lakebed", "Double Mansion", "Fantasy", "Germany vs France", "Korea"]
        else:
            maps = []
            for map_name, map_info in MapSelectionUtilityMethods.map_data.items():
                all_types = []
                for types in map_info.get('gamemode', {}).values():
                    all_types.extend(types)

                all_types = [map_type.lower() for map_type in all_types]
                if game_mode in all_types:
                    maps.append(map_name)
        return maps
    
    @staticmethod
    def create_map_embed(selected_map: str, interaction: discord.Interaction):
        map_data = MapSelectionUtilityMethods.map_data[selected_map]

        chokepoints = map_data.get('chokepoints', 'Unknown')
        date_created = map_data.get('date_created', 'Unknown')
        oil_spots = map_data.get('oil_spots', 'Unknown')
        symmetrical = map_data.get('symmetrical', 'Unknown')
        total_crystals = map_data.get('total_crystals', 'Unknown')
        map_types = map_data.get('map_types', [])
        cost = map_data.get('max_income', 'Unknown')
        map_size = map_data.get('map_size', 'Unknown')
        map_image = map_data.get('image')

        map_embed = discord.Embed(
            title=f"{selected_map} Map Information:",
            color=0x00ffff
        )
        
        if map_image:
            map_embed.set_image(url=map_image)

        map_embed.set_author(
            name=f"{interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url)
        
        map_embed.timestamp = interaction.created_at
        
        # Basic map information
        map_embed.add_field(name="Map Size", value=map_size, inline=True)
        map_embed.add_field(name="Max Income", value=cost, inline=True)
        map_embed.add_field(name="Date Created", value=date_created, inline=True)
        
        # Resource information
        map_embed.add_field(name="Oil Spots", value=oil_spots, inline=True)
        map_embed.add_field(name="Total Crystals", value=total_crystals, inline=True)
        map_embed.add_field(name="Symmetrical", value=symmetrical, inline=True)
        
        # Strategic information
        map_embed.add_field(name="Chokepoints", value=chokepoints, inline=True)
        
        # Map types
        if map_types:
            map_types_str = ", ".join(map_types)
            map_embed.add_field(name="Map Types", value=map_types_str, inline=True)
        else:
            map_embed.add_field(name="Map Types", value="Unknown", inline=True)
        
        # Available game modes
        available_modes = []
        for gamemode, alliances in map_data['gamemode'].items():
            if alliances:
                mode_str = f"{gamemode}: {', '.join(alliances)}"
                available_modes.append(mode_str)
                if gamemode == 'Conquest':
                    mode_str = f"Lightning Conquest: {', '.join(alliances)}"
                    available_modes.append(mode_str)
        
        if available_modes:
            modes_text = "\n".join(available_modes)
            map_embed.add_field(name="Available Modes", value=modes_text, inline=False)

        return map_embed
    
    @staticmethod
    def create_random_map_embed(game_mode: str, interaction: discord.Interaction):
        """Creates a Discord embed with map information"""
        maps = MapSelectionUtilityMethods.determine_map_list(game_mode=game_mode)
        if not maps:
            return discord.Embed(title="Error", description=f"No maps found for {game_mode} mode", color=0xff0000)
        selected_map = random.choice(maps)
        map_embed = MapSelectionUtilityMethods.create_map_embed(selected_map, interaction)
        map_embed.description = f"Random {game_mode} map."
        return map_embed
    
    @staticmethod
    def get_available_gamemodes():
        return MapSelectionUtilityMethods.gamemodes
    
    @staticmethod
    def update_map_data():
        """Re-scrape and update map data"""
        print("Scraping new map data from wiki...")
        MapSelectionUtilityMethods.map_data = scrape_map_data()
        MapSelectionUtilityMethods.all_map_names = list(MapSelectionUtilityMethods.map_data.keys())
        MapSelectionUtilityMethods.gamemodes = get_all_gamemodes(MapSelectionUtilityMethods.map_data)
