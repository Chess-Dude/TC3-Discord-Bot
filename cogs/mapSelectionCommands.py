import discord, random, json
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from .mapSelectionClasses.mapSelectionDropdown import RerollDropdown
from .mapSelectionClasses.mapSelectionUtilityMethods import MapSelectionUitilityMethods

class AppCommandsMapSelection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914

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
        Choice(name="FFA4", value=8),
        Choice(name="FFA6", value=9),
        Choice(name="game_night_3v3", value=10)
    ])
    async def random_map(
        self,
        interaction: discord.Interaction,
        game_mode: Choice[int]
    ):

        map_embed = MapSelectionUitilityMethods.random_map_init(
            self=self,
            interaction=interaction,
            game_mode=game_mode.name
        )

        await interaction.response.send_message(
            embed=map_embed, 
            view=RerollDropdown())

async def setup(bot):
    await bot.add_cog(AppCommandsMapSelection(bot))
