import discord
from discord import app_commands
from discord.ext import commands
from .suggestionClasses.suggestionModal import SuggestionModal

class SuggestionCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def bots_channels(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914

    is_bots = app_commands.check(bots_channels)

    @is_bots
    @app_commands.guilds(350068992045744141)
    @app_commands.command(
        name="suggest",
        description="A Command that allows you to suggest concepts!")
    async def suggest(
        self,
        interaction:discord.Interaction
    ):
        await interaction.response.send_modal(SuggestionModal())

async def setup(bot):
    await bot.add_cog(SuggestionCommands(bot))
