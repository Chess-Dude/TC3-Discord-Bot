import discord, json, random
import requests
from bs4 import BeautifulSoup

class MapSelectionUtilityMethods():
    map_data = {}
    available_gamemodes  = {'Conquest':'Conquest', 'Free_for_All':'Free For All', 'King_of_the_Hill':'King Of The Hill', 'Survival':'Survival'}
    gamemodes = ['1v1','2v2','3v3','4v4','5v5','2v2v2','3v3v3', 'FFA3', 'FFA4', 'FFA6', 'Survival']
    lowercase_game_modes = {} # dict mapping for lowercase to normal case
    lowercase_map_names = {} # dict mapping for lowercase to normal case
    #gamemodes.append('game_night_3v3') # add or remove gamemodes etc

    @staticmethod
    def get_map_data():
        for gamemode_page_name in MapSelectionUtilityMethods.available_gamemodes.keys():

            gamemode_map_page = requests.get(f"https://theconquerors.fandom.com/wiki/{gamemode_page_name}")
            soup = BeautifulSoup(gamemode_map_page.content, "html.parser")

            if gamemode_page_name != "Survival":  # different html layout since no tabber
                wds_tabber_wrapper = soup.find('div', class_='wds-tabs__wrapper')
                wds_tabs = wds_tabber_wrapper.find('ul', class_='wds-tabs')
                sub_gamemodes_raw = wds_tabs.find_all('li', class_='wds-tabs__tab')

                sub_gamemodes = []  # gets the sub_gamemodes for the page. Eg 2v2, 3v3, and so on.
                for sub_gamemoode_raw in sub_gamemodes_raw:
                    sub_gamemode = sub_gamemoode_raw['data-hash'].strip().replace('_', '')
                    sub_gamemodes.append(sub_gamemode)

                sub_gamemode_pages = soup.find_all('div', class_='wds-tab__content')

                data = zip(sub_gamemodes, sub_gamemode_pages)
                
                for sub_gamemode_name, sub_gamemode_page in data:
                    
                    if sub_gamemode_name.endswith('FFA'):
                        sub_gamemode_name = 'FFA' + sub_gamemode_name[0]

                    table_rows = sub_gamemode_page.find_all("tr")
                    for row in table_rows[1:]:  # skip header
                        row_data = row.find_all("td")
                        map_name = row_data[0].get_text(strip=True)
                        image_data = row_data[1].find('img')

                        url = image_data.get('data-src', None) or image_data.get('src', None)

                        if map_name not in MapSelectionUtilityMethods.map_data:
                            MapSelectionUtilityMethods.map_data[map_name] = {
                                'max_income': row_data[2].get_text(strip=True),
                                'map_size': row_data[3].get_text(strip=True),
                                'gamemode': {},
                                'image': url
                            }

                        actual_gamemode_name = MapSelectionUtilityMethods.available_gamemodes[gamemode_page_name]
                        if actual_gamemode_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                            MapSelectionUtilityMethods.map_data[map_name]['gamemode'][actual_gamemode_name] = []

                        MapSelectionUtilityMethods.map_data[map_name]['gamemode'][actual_gamemode_name].append(sub_gamemode_name)

            else:
                survival_table = soup.find("tbody")
                table_rows = survival_table.find_all("tr")
                for row in table_rows[1:]:  # skip header
                    row_data = row.find_all("td")
                    map_name = row_data[0].get_text(strip=True)
                    image_data = row_data[1].find('img')

                    url = image_data.get('data-src', None) or image_data.get('src', None) 

                    if map_name not in MapSelectionUtilityMethods.map_data:
                        MapSelectionUtilityMethods.map_data[map_name] = {
                            'max_income': row_data[2].get_text(strip=True),
                            'map_size': row_data[3].get_text(strip=True),
                            'gamemode': {},
                            'image': url
                        }

                    actual_gamemode_name = MapSelectionUtilityMethods.available_gamemodes['Survival']
                    if actual_gamemode_name not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                        MapSelectionUtilityMethods.map_data[map_name]['gamemode'][actual_gamemode_name] = []

                    # In the case of Survival, there are no sub_gamemodes, so we just append the gamemode itself
                    MapSelectionUtilityMethods.map_data[map_name]['gamemode'][actual_gamemode_name].append(actual_gamemode_name)


    @staticmethod
    def update_map_data():
        with open('mapList.json', 'w') as json_file:
            json.dump(MapSelectionUtilityMethods.map_data, json_file, indent=4, sort_keys=True)

    all_map_names = list(map_data.keys())

    def get_map_image():
        maps = {}
        for data in MapSelectionUtilityMethods.items():
            map_name = data[0]
            data = data[1]
            image = data['image']
            maps[map_name] = image
        return maps

    def determine_map_list(game_mode):
            game_mode = game_mode.lower()
            if game_mode == "game_night_3v3":
                maps = ["Basalt Peninsula", "Germany Map", "Lakebed", "Double Mansion", "Fantasy", "Germany vs. France", "Korea",] 
            else:
                maps = []
                for map_data in MapSelectionUtilityMethods.map_data.items():
                    all_types = []
                    map_name = map_data[0]
                    map_data = map_data[1]
                    gamemodes = map_data['gamemode'].values()
                    for types in gamemodes:
                        all_types.extend(list(types))
                    all_types = map(lambda map_type: map_type.lower(), all_types)
                    if game_mode in all_types:
                        maps.append(map_name)
            return maps

    def create_map_embed(self, selected_map, map_type, interaction: discord.Interaction):
        map_embed = discord.Embed(title=f"Randomized {map_type} Map:", 
            description=f"{interaction.user.mention} Your randomized map is: {selected_map}!", 
            color=0x00ffff
            )

        map_data = MapSelectionUtilityMethods.map_data[selected_map]
        cost = map_data['max_income']
        map_size = map_data['map_size']
        map_image = map_data.get('image', None)

        map_embed = discord.Embed(
            title=f"{selected_map} Map Information:",
            description=f"{interaction.user.mention}",
            color=0x00ffff
        )
        if map_image != None:
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

    def random_map_init(self,interaction: discord.Interaction, game_mode: str):
    
        real_name = game_mode
        if game_mode == "1v1":
            real_name = "FFA2"

        maps = MapSelectionUtilityMethods.determine_map_list(
            game_mode=real_name
        )

        map_embed = MapSelectionUtilityMethods.create_map_embed(
            self=self,
            selected_map=random.choice(maps),
            map_type=game_mode,
            interaction=interaction
        )

        return map_embed

def update_load_map_data(): #updates all data and map information
    MapSelectionUtilityMethods.get_map_data()
    MapSelectionUtilityMethods.update_map_data()
    MapSelectionUtilityMethods.lowercase_map_names = {map_name.lower(): map_name for map_name in MapSelectionUtilityMethods.map_data.keys()}
    MapSelectionUtilityMethods.lowercase_game_modes = {gamemode.lower(): gamemode for gamemode in MapSelectionUtilityMethods.gamemodes}
update_load_map_data()
