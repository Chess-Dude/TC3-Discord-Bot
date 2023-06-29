import discord, json, random

class MapSelectionUitilityMethods():
    def get_map_image():
        with open("mapList.json", 'r') as config_reader:
            map_images = json.loads(config_reader.read())
            return map_images

    def determine_map_list(
        self,
        game_mode
    ):
        if game_mode == "1v1":
            maps = [
                "Spain",
                "Arctic Canal Map",
                "Basalt Peninsula",
                "British Isles", 
                "Cave Map", 
                "Cavern",
                "City 3", 
                "City vs. Nature", 
                "Continent", 
                "Desert vs. Grass", 
                "Desert vs. Grass 2", 
                "Desert vs. Grass 3",
                "Desert vs. Grass 4", 
                "Desert vs. Grass 6",
                "Desert vs. Grass Spiral", 
                "Double Mansion", 
                "Eygptian Expedition",  
                "Europe",
                "Fantasy", 
                "Fantasy 2", 
                "France", 
                "Gem Mine", 
                "Germany Map", 
                "Germany vs. France",
                "Golf Course", 
                "Golf Course 2", 
                "Korea", 
                "Lakebed",
                "Lasers",
                "Last Red City", 
                "Long Islands", 
                "Mainland",
                "Mansion", 
                "Mansion: Flooded",
                "Mars", 
                "Medieval Grounds", 
                "Mesa", 
                "Mexico", 
                "Monument Park",
                "Passage", 
                "Point Blank",
                "RETRO: Four Seasons", 
                "RETRO: Six Islands",
                "Ryry's Oil Map", 
                "Sand Bottom Forest", 
                "Sand City",
                "Six Small Islands",
                "Skymap",
                "Soviet Union",
                "Three Corner Cave",
                "Tropical Oasis",
                "Two Cave Map", 
                "Two Islands Map", 
                "USA vs. Russia", 
                "Void Map"
                ]

        elif game_mode == "2v2":
            maps = [
                "Spain",
                "Arctic Canal Map", 
                "Basalt Peninsula", 
                "British Isles", 
                "Cavern", 
                "Continent", 
                "Desert vs. Grass", 
                "Desert vs. Grass 2", 
                "Desert vs. Grass 3", 
                "Desert vs. Grass Spiral", 
                "Desert vs. Grass 6", 
                "Europe", 
                "Fantasy", 
                "Fantasy 2", 
                "France", 
                "Germany Map", 
                "Golf Course", 
                "Ice Catalyst", 
                "Korea", 
                "Lakebed", 
                "Lasers", 
                "Mainland", 
                "Mansion: Flooded", 
                "Mesa", 
                "Mexico", 
                "Passage", 
                "River Banks", 
                "Sandy Floors", 
                "Six Small Islands",
                "Skymap", 
                "Snow Battlefield", 
                "Soviet Union", 
                "USA vs. Russia", 
                "Void Map", 
                "World"
                ]

        if game_mode == "3v3":
            maps = [
                "Spain",
                "Archipelago", 
                "Arctic Canal Map", 
                "Arctic Circle", 
                "Basalt Peninsula", 
                "British Isles", 
                "Cave Map", "Cavern", 
                "City 3", 
                "City vs. Nature", 
                "Continent", 
                "Corners", 
                "Desert vs. Grass", 
                "Desert vs. Grass 2", 
                "Desert vs. Grass 3", 
                "Desert vs. Grass 4", 
                "Desert vs. Grass 6", 
                "Double Mansion", 
                "Europe", 
                "Fantasy", 
                "Fantasy 2", 
                "France", 
                "Frozen River", 
                "Gem Mine", 
                "Germany Map", 
                "Germany vs. France", 
                "Golf Course", 
                "Golf Course 2", 
                "Ice Catalyst", 
                "Igneous Islands/Magma", 
                "Korea", 
                "Lake City Map", 
                "Lakebed", 
                "Lasers", 
                "Long Islands", 
                "Mainland", 
                "Mansion", 
                "Mansion: Flooded", 
                "Mars Canyons", 
                "Mars Tunnels", 
                "Maze", 
                "Mesa", 
                "Mexico", 
                "Moon Surface", 
                "Obsidian Atoll", 
                "Passage", 
                "Point Blank", 
                "RETRO: Cliffs", 
                "RETRO: Four Seasons", 
                "RETRO: Six Islands", 
                "RETRO: The Moon", 
                "River Banks", 
                "Sand Bottom Forest", 
                "Sandy Floors", 
                "Six Small Islands",
                "Skymap", 
                "Snow Battlefield", 
                "Soviet Union", 
                "States", 
                "Symmetry", 
                "Twisting Isles", 
                "Two Islands Map", 
                "USA vs. Russia", 
                "Void Map", 
                "World"
                ]

        elif game_mode == "4v4":
            maps = [
                "Archipelago", 
                "Arctic Canal Map", 
                "Arctic Circle", 
                "Basalt Peninsula", 
                "British Isles", 
                "Cave Map", 
                "Cavern", 
                "Desert vs. Grass", 
                "Desert vs. Grass 2", 
                "Desert vs. Grass 3", 
                "Desert vs. Grass 4", 
                "Desert vs. Grass 6", 
                "Double Mansion", 
                "Europe", 
                "Fantasy", 
                "Fantasy 2", 
                "France", 
                "Gem Mine", 
                "Germany Map", 
                "Germany vs. France", 
                "Golf Course", 
                "Golf Course 2", 
                "Ice Catalyst", 
                "Igneous Islands/Magma", 
                "Korea", 
                "Lakebed", 
                "Lasers", 
                "Long Islands", 
                "Mainland", 
                "Mansion", 
                "Mars 4", 
                "Mars Canyons", 
                "Maze", 
                "Mesa", 
                "Mexico", 
                "Middle East", 
                "Obsidian Atoll", 
                "Passage", 
                "Point Blank", 
                "River Banks", 
                "Sand Bottom Forest", 
                "Sandy Floors", 
                "Six Small Islands", 
                "Skymap",
                "Snow Battlefield", 
                "Soviet Union", 
                "States",
                "Two Cave Map", 
                "USA vs. Russia", 
                "World"
                ]

        elif game_mode == "5v5":
            maps = [
                "Archipelago",
                "Arctic Canal Map",
                "Basalt Peninsula", 
                "Desert vs. Grass", 
                "Desert vs. Grass 2", 
                "Double Mansion",
                "Fantasy",
                "Fantasy 2",
                "Gem Mine", 
                "Germany vs France",
                "Lasers",
                "Mediterranean",
                "Passage", 
                "Skymap",
                "Snow Battlefield", 
                "Soviet Union", 
                "States", 
                "Void City", 
                "World"
                ]

        elif game_mode == "game_night_3v3":
            maps = ["Basalt Peninsula", "Germany Map", "Lakebed", "Double Mansion", "Fantasy", "Germany vs. France", "Korea",]

        elif game_mode == "2v2v2":
            maps = [
                "Arctic Circle",
                "Cave Map",
                "City 3",
                "Continent",
                "Corners",
                "Divided Metropolis",
                "Mansion",
                "Maze",
                "Middle East",
                "Moon Surface",
                "RETRO: Cliffs",
                "RETRO: Four Seasons",
                "RETRO: Six Islands",
                "RETRO: The Moon",
                "Ryry's Oil Map",
                "Six Small Islands",
                "Snowy Islands",
                "Three Corner Cave",
                "Tri Weather Reworked",
                "Twisting Isles",
                "Two Cave Map"
                ]

        elif game_mode == "FFA3":
            maps = [
                "City 3",
                "Dalarna Island",
                "Endceladus",
                "RETRO: Six Islands",
                "Ryry's Oil Map",
                "Snowy Islands",
                "Three Corner Cave",
                "Tri Weather Reworked",
                "Tri Weather Reworked",
                "Tropical Oasis",
                "Two Cave Map",
                "Underground Cog"
            ]

        elif game_mode == "FFA4":
            maps = [
                "Monument Park",
                "Sand City",
                "Six Small Islands",
                "Void [needtitle]"
            ]

        elif game_mode == "FFA6":
            maps = [
                "Frosty Gear",
                "Magma Pools",
                "Sandstone Cog",
                "Tropical Oasis",
                "Sand City",
                "Underground Cog",
            ]

        elif game_mode == "game_night_3v3":
            maps = ["Basalt Peninsula", "Germany Map"]        

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
            
            map_embed.set_image(url=map_images[selected_map])
            
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

