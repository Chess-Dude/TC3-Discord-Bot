import discord, random
from ..mapSelectionUtilityMethods import MapSelectionUtilityMethods

class MapSelectionDropdown(discord.ui.Select):
    def __init__(self):
        map_types = [
            discord.SelectOption(
                label=gamemode_name, 
                description=f"Generates A Random {gamemode_name} Map"
            ) for gamemode_name in MapSelectionUtilityMethods.gamemodes
        ]

        super().__init__(
            placeholder="Choose a different map type to randomize...", 
            min_values=1, 
            max_values=1, 
            options=map_types,
            custom_id="map_change_dropdown"
        )

    async def callback(self, interaction: discord.Interaction):
        # Get the current embed and check author permissions
        map_embed = interaction.message.embeds[0].to_dict()
        map_embed_author = map_embed['author']
        map_embed_author_name = map_embed_author['name']

        if map_embed_author_name == interaction.user.display_name:
            selected_mode = str(self.values[0])
            maps = MapSelectionUtilityMethods.determine_map_list(game_mode=selected_mode)
        
            if not maps:
                await interaction.response.send_message(
                    content=f"No maps found for {selected_mode} mode. Please select a different mode.",
                    ephemeral=True
                )
                return
                
            new_map_embed = MapSelectionUtilityMethods.create_map_embed(
                selected_map=random.choice(maps),
                map_type=selected_mode,
                interaction=interaction
            )
            
            await interaction.response.send_message(
                embed=new_map_embed, 
                view=RerollDropdown()
            )
        else: 
            await interaction.response.send_message(
                content=f"You may not change another members' map type. Please run your own ``/random map`` command in order to reroll a map.", 
                ephemeral=True
            )

class RerollDropdown(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MapSelectionDropdown())