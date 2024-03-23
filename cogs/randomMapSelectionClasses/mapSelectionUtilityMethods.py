import discord, json, random

class MapSelectionUitilityMethods():
    def load_map_data():
        with open("mapList.json", 'r') as config_reader:
            map_data = json.loads(config_reader.read())
            return map_data
    map_data = load_map_data()

    def get_map_image():
        maps = {}
        for map_data in MapSelectionUitilityMethods.map_data.items():
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
            for map_data in MapSelectionUitilityMethods.map_data.items():
                map_name = map_data[0]
                map_data = map_data[1]
                submodes = list(map_data['gamemode'].values())[0]
                if game_mode in submodes:
                    maps.append(map_name)
        return maps

    def create_map_embed(
        self,
        selected_map,
        map_images,
        map_type, 
        interaction: discord.Interaction
        ):
            map_embed = discord.Embed(
            title=f"Randomized {map_type} Map:", 
            description=f"{interaction.user.mention} Your randomized map is: {selected_map}!", 
            color=0x00ffff
            )
            image = MapSelectionUitilityMethods.map_data[selected_map]['image'] or "N/A"
            map_embed.set_image(url=image)
            
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

        maps = MapSelectionUitilityMethods.determine_map_list(
            self=self,
            game_mode=game_mode
        )
        map_images = MapSelectionUitilityMethods.get_map_image()

        map_embed = MapSelectionUitilityMethods.create_map_embed(
            self=self,
            selected_map=random.choice(maps),
            map_images=map_images,
            map_type=game_mode,
            interaction=interaction
        )

        return map_embed

