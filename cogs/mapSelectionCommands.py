import discord, random, json
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class MapSelectionDropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        map_types = [
            discord.SelectOption(
                label="1v1", 
                description="Generates A Random 1v1 Map"),
            
            discord.SelectOption(
                label="2v2", 
                description="Generates A Random 2v2 Map"),

            discord.SelectOption(
                label="3v3", 
                description="Generates A Random 3v3 Map"),

            discord.SelectOption(
                label="4v4", 
                description="Generates A Random 4v4 Map"),

            discord.SelectOption(
                label="5v5", 
                description="Generates A Random 5v5 Map"),
            
            discord.SelectOption(
                label="2v2v2", 
                description="Generates A Random 2v2v2 Map"),
            
            discord.SelectOption(
                label="FFA3", 
                description="Generates A Random FFA3 Map"),
            
            discord.SelectOption(
                label="FFA4", 
                description="Generates A Random FFA4 Map"),
            
            discord.SelectOption(
                label="FFA6", 
                description="Generates A Random FFA6 Map")]

        super().__init__(
            placeholder="Choose a different map type to randomize...", 
            min_values=1, 
            max_values=1, 
            options=map_types,
            custom_id="map_change_dropdown")

    async def callback(
        self, 
        interaction: discord.Interaction
        ):
            map_embed = interaction.message.embeds[0].to_dict()
            map_embed_author = map_embed['author']
            map_embed_author_name = map_embed_author['name']

            if map_embed_author_name == interaction.user.display_name:

                maps = AppCommandsMapSelection.determine_map_list(
                    self=self,
                    game_mode=str(self.values[0])
                )
                map_images = AppCommandsMapSelection.get_map_image()

                new_map_embed = AppCommandsMapSelection.create_map_embed(
                    self=self,
                    selected_map=random.choice(maps),
                    map_images=map_images,
                    map_type=str(self.values[0]),
                    interaction=interaction
                )
                await interaction.response.send_message(
                    embed=new_map_embed, 
                    view=RerollDropdown())

            else: 
                await interaction.response.send_message(
                content=f"You may not change another members' map type. Please run your own ``/random map`` command in order to reroll a map.", 
                ephemeral=True)

class RerollDropdown(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MapSelectionDropdown())

class AppCommandsMapSelection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_map_image():
        with open("mapList.json", 'r') as config_reader:
            map_images = json.loads(config_reader.read())
            return map_images
    
    def bots(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914

    def determine_map_list(
        self,
        game_mode
    ):
        if game_mode == "1v1":
            maps = [
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
                "Point blank",
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
                "Point blank", 
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
                "Point blank", 
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

        maps = AppCommandsMapSelection.determine_map_list(
            self=self,
            game_mode=game_mode
        )
        map_images = AppCommandsMapSelection.get_map_image()

        map_embed = AppCommandsMapSelection.create_map_embed(
            self=self,
            selected_map=random.choice(maps),
            map_images=map_images,
            map_type=game_mode,
            interaction=interaction
        )

        return map_embed


    group = app_commands.Group(name="random", description="A Command That Randomizes A Game Map!")

    @group.command(
        name="map",
        description="A Command That Randomizes A Game Map!")
    @app_commands.check(bots)
    @app_commands.choices(game_mode=[
        Choice(name="1v1", value=1),
        Choice(name="2v2", value=2),
        Choice(name="3v3", value=3),
        Choice(name="4v4", value=4),
        Choice(name="5v5", value=5),
        Choice(name="2v2v2", value=6),
        Choice(name="FFA3", value=7),
        Choice(name="FFA4", value=7),
        Choice(name="FFA6", value=8),
        Choice(name="game_night_3v3", value=9)
    ])
    async def random_map(
        self,
        interaction: discord.Interaction,
        game_mode: Choice[int]
    ):

        map_embed = AppCommandsMapSelection.random_map_init(
            self=self,
            interaction=interaction,
            game_mode=game_mode.name
        )

        await interaction.response.send_message(
            embed=map_embed, 
            view=RerollDropdown())

async def setup(bot):
    await bot.add_cog(AppCommandsMapSelection(bot))
