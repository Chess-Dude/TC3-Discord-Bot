import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from .randomMapSelectionClasses.mapSelectionDropdown import RerollDropdown
from .mapSelectionUtilityMethods import MapSelectionUtilityMethods

class AppCommandsMapSelection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914
    
    @staticmethod
    def get_game_mode_choices():
        available_modes = MapSelectionUtilityMethods.get_available_gamemodes()
        choices = []
        
        for mode in available_modes:
            choices.append(Choice(name=mode, value=mode))

        if "game_night_3v3" not in available_modes:
            choices.append(Choice(name="Game Night 3v3", value="game_night_3v3"))
        
        return choices[:25]

    group = app_commands.Group(name="random", description="A Command That Randomizes A Game Map!")

    @group.command(
        name="map",
        description="A Command That Randomizes A Game Map!")
    @app_commands.choices(game_mode=get_game_mode_choices())
    async def random_map(
        self,
        interaction: discord.Interaction,
        game_mode: Choice[int]
    ):
        game_mode_name = game_mode.value
        
        if interaction.guild and interaction.guild.id == 350068992045744141 and interaction.channel.id != 351057167706619914:
            await interaction.response.send_message("Please use the designated channel for map randomization.", ephemeral=True)
            return
        
        try:
            maps = MapSelectionUtilityMethods.determine_map_list(game_mode=game_mode_name)
            if not maps:
                await interaction.response.send_message(f"No maps found for {game_mode_name} mode. Please select a different mode or contact an administrator.", ephemeral=True)
                return
            
            map_embed = MapSelectionUtilityMethods.random_map_init(
                interaction=interaction,
                game_mode=game_mode_name
            )
            map_embed.remove_field("Available Modes") # its already known. No point in including it.
            
            await interaction.response.send_message(
                embed=map_embed, 
                view=RerollDropdown()
            )
            
        except Exception as e:
            print(f"Error in random_map command: {str(e)}")
            await interaction.response.send_message(
                f"An error occurred while generating a random map: {str(e)}",
                ephemeral=True
            )

    @group.command(
        name="update_maps",
        description="Update the map database from the wiki (Admin only)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def update_maps(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            old_count = len(MapSelectionUtilityMethods.map_data)
            MapSelectionUtilityMethods.update_map_data()
            new_count = len(MapSelectionUtilityMethods.map_data)
            
            await interaction.followup.send(
                f"✅ Map data updated successfully!\n"
                f"Total maps: {new_count}\n"
                f"Maps changed: {new_count - old_count}",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error updating map data: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(AppCommandsMapSelection(bot))