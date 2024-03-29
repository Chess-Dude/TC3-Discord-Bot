import discord, random
from .mapSelectionUtilityMethods import MapSelectionUtilityMethods

class MapSelectionDropdown(discord.ui.Select):
    def __init__(self):
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
                label="3v3v3", 
                description="Generates A Random 3v3v3 Map"),
                                    
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
                real_name = str(self.values[0])
                if str(self.values[0]) == "1v1":
                    real_name = "FFA2"

                maps = MapSelectionUtilityMethods.determine_map_list(
                    game_mode=real_name
                )

                new_map_embed = MapSelectionUtilityMethods.create_map_embed(
                    self=self,
                    selected_map=random.choice(maps),
                    map_type=real_name,
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
