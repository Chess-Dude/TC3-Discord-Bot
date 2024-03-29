import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from .randomMapSelectionClasses.mapSelectionDropdown import RerollDropdown
from .randomMapSelectionClasses.mapSelectionUtilityMethods import MapSelectionUtilityMethods

class AppCommandsMapSelection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914

    group = app_commands.Group(name="random", description="A Command That Randomizes A Game Map!")

    @group.command(
        name="map",
        description="A Command That Randomizes A Game Map!")
    @app_commands.choices(game_mode=[Choice(name=gamemode_name, value=index+1) for index, gamemode_name in enumerate(MapSelectionUtilityMethods.gamemodes)])

    async def random_map(
        self,
        interaction: discord.Interaction,
        game_mode: Choice[str]
    ):
        game_mode = MapSelectionUtilityMethods.lowercase_gamodes.get(game_mode.lower(), None)

        if game_mode is None:
            await interaction.response.send_message("Error: That gamemode was not found! Try again or check the wiki.", ephemeral=True)
            return
        
        if interaction.guild.id == 350068992045744141 and interaction.channel.id != 351057167706619914:
            raise app_commands.errors.CheckFailure
        
        map_embed = MapSelectionUtilityMethods.random_map_init(
            self=self,
            interaction=interaction,
            game_mode=game_mode.name
        )

        await interaction.response.send_message(
            embed=map_embed, 
            view=RerollDropdown())

async def setup(bot):
    await bot.add_cog(AppCommandsMapSelection(bot))
