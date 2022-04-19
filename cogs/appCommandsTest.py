import discord
from discord import app_commands
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def testChannel(ctx):
        return ctx.channel.id == 945417589704781824
    
    isTestChannel = app_commands.check(testChannel)
    
    @isTestChannel
    @app_commands.command(name = "test", description = "this is a test command")
    async def scrim(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"test response")
        
async def setup(bot):
    await bot.add_cog(test(bot), guilds = [discord.Object(id = 945417589235023963)])
