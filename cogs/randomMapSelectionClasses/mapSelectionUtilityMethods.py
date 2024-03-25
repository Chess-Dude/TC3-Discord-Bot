import discord, json, random
import requests
from bs4 import BeautifulSoup

class MapSelectionUtilityMethods():
    @staticmethod
    def get_all_maps() -> list:
        page = requests.get("https://theconquerors.fandom.com/wiki/Maps")
        soup = BeautifulSoup(page.content, "html.parser")

        table = soup.find('table', class_='wikitable')
        table_rows = table.findAll('tr')

        maps = []
        for row in table_rows:
            table_data = row.find_all('td')
            if table_data:
                map_name = table_data[0].get_text(strip=True)
                maps.append(map_name)

        return maps


    all_map_names = get_all_maps()
    map_data = {}
    gamemode_mappings = {
        1: {"type": "2v2", "gamemode": "Conquest & Lightning"},
        2: {"type": "3v3", "gamemode": "Conquest & Lightning"},
        3: {"type": "4v4", "gamemode": "Conquest & Lightning"},
        4: {"type": "5v5", "gamemode": "Conquest & Lightning"},
        5: {"type": "2v2v2", "gamemode": "Conquest & Lightning"},
        6: {"type": "3v3v3", "gamemode": "Conquest & Lightning"},
        # 0 and 5 are for some reason, the same index in the HTML. Unknown reason for duplicate tab index.
        8: {"type": "2FFA", "gamemode": "FFA & Lightning FFA"},
        9: {"type": "3FFA", "gamemode": "FFA & Lightning FFA"},
        10: {"type": "4FFA", "gamemode": "FFA & Lightning FFA"},
        11: {"type": "6FFA", "gamemode": "FFA & Lightning FFA"},
        # 12 is for Survival
        14: {"type": "3v3", "gamemode": "Territory Conquest"},
        15: {"type": "2v2v2", "gamemode": "Territory Conquest"},
        # Random missing gap in the index, reason unknown.
        17: {"type": "3v3", "gamemode": "King of the Hill"},
        18: {"type": "2v2v2", "gamemode": "King of the Hill"},
        # 19 is for 'all maps' tab
    }

    @staticmethod
    def get_map_data():
        gamemode_map_page = requests.get("https://theconquerors.fandom.com/wiki/Gamemodes_%26_Maps")
        soup = BeautifulSoup(gamemode_map_page.content, "html.parser")

        tabber_wrapper = soup.find('div', class_='tabber')  # annoying tabber moment
        tab_contents = tabber_wrapper.find_all('div', class_='wds-tab__content')

        for index, mapping in MapSelectionUtilityMethods.gamemode_mappings.items():
            data = tab_contents[index]
            table_rows = data.find_all("tr")
            for row in table_rows:
                row_data = row.find_all("td")
                if row_data:
                    map_name = row_data[0].get_text(strip=True)
                    if map_name in MapSelectionUtilityMethods.all_map_names:
                        if map_name not in MapSelectionUtilityMethods.map_data:
                            image_data = row_data[1].find('img')
                            url = image_data.get('data-src', None)
                            
                            MapSelectionUtilityMethods.map_data[map_name] = {
                                'max_income': row_data[2].get_text(strip=True),
                                'map_size': row_data[3].get_text(strip=True),
                                'gamemode': {},
                                'image':url
                            }
                        gamemode = mapping['gamemode']  # Eg: Conquest etc
                        sub_gamemode = mapping['type']  # Eg: 2v2v2

                        if gamemode not in MapSelectionUtilityMethods.map_data[map_name]['gamemode']:
                            MapSelectionUtilityMethods.map_data[map_name]['gamemode'][gamemode] = []
                        MapSelectionUtilityMethods.map_data[map_name]['gamemode'][gamemode].append(sub_gamemode)

    @staticmethod
    def update_map_data():
        MapSelectionUtilityMethods.get_map_data()
        with open('mapList.json', 'w') as json_file:
            json.dump(MapSelectionUtilityMethods.map_data, json_file, indent=4, sort_keys=True)

    def get_map_image():
        maps = {}
        for map_data in MapSelectionUtilityMethods.map_data.items():
            map_name = map_data[0]
            map_data = map_data[1]
            image = map_data['image']
            maps[map_name] = image
        return maps

    def determine_map_list(self, game_mode):

        if game_mode == "game_night_3v3":
            maps = ["Basalt Peninsula", "Germany Map", "Lakebed", "Double Mansion", "Fantasy", "Germany vs. France", "Korea",] 
        else:
            maps = []
            for map_data in MapSelectionUtilityMethods.map_data.items():
                map_name = map_data[0]
                map_data = map_data[1]
                all_types = []
                for gamemode, types in map_data['gamemode'].items():
                    all_types.extend(types)
                if game_mode in all_types:
                    maps.append(map_name)
        return maps

    def create_map_embed(
        self,
        selected_map,
        map_type, 
        interaction: discord.Interaction
        ):
            map_embed = discord.Embed(
            title=f"Randomized {map_type} Map:", 
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
                icon_url=interaction.user.display_avatar.url
            )

            map_embed.set_footer(
                text=f"{selected_map} Map Information",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )

            map_embed.timestamp = interaction.created_at
            map_embed.add_field(name="Max Income:", value=cost, inline=True)
            map_embed.add_field(name="Map Size:", value=map_size, inline=True)
            
            map_embed.set_author(
                name=f"{interaction.user.display_name}", 
                icon_url=interaction.user.display_avatar.url)
            
            map_embed.set_footer(
                text=f"Random {map_type} Map", 
                icon_url=interaction.guild.icon)
            
            map_embed.timestamp = interaction.created_at

            return map_embed

    def random_map_init(
        self,
        interaction: discord.Interaction,
        game_mode
    ):

        maps = MapSelectionUtilityMethods.determine_map_list(
            self=self,
            game_mode=game_mode
        )

        map_embed = MapSelectionUtilityMethods.create_map_embed(
            self=self,
            selected_map=random.choice(maps),
            map_type=game_mode,
            interaction=interaction
        )

        return map_embed
    
    get_map_data() # startup grab data from wiki
    update_map_data()

