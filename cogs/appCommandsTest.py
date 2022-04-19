import discord
from discord import app_commands
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "test", description = "this is a test command")
    async def scrim(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"test response")
        
async def setup(bot):
    await bot.add_cog(test(bot), guilds = [discord.Object(id = 371817692199518240)])
