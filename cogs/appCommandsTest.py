import discord
from discord import app_commands
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def testChannel(ctx):
        return ctx.channel.id == 941567353672589322
    
    isTestChannel = app_commands.check(testChannel)
    
    @isTestChannel
    @app_commands.command(name = "test", description = "this is a test command")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"test response")

    @isTestChannel
    @app_commands.command(name = "1v1scrimtest", description = "Run this command to have a competitive 1v1 scrimmage!")
    @app_commands.checks.cooldown(1, 1800.0)
    async def scrim_1v1(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} wants to 1v1 <@&935635762987298836>!")
    
    @isTestChannel
    @app_commands.command(name = "2v2scrimtest", description = "Run this command to have a competitive 2v2 scrimmage!")
    @app_commands.checks.cooldown(1, 1800.0)
    async def scrim_2v2(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} and their team want to 2v2 <@&935635762987298836>!")
    
    @isTestChannel
    @app_commands.command(name = "teamscrimtest", description = "Run this command to have a competitive team scrimmage!")
    @app_commands.checks.cooldown(1, 1800.0)
    async def scrim_team(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} and their team want to <@&935635762987298836>!")

    @isTestChannel
    @app_commands.command(name = "createrole", description = "Run this command to create a role!", )
    @app_commands.choices()
    @app_commands.checks.cooldown(1, 5.0)
    async def create_role(self, interaction: discord.Interaction):
        TCG = self.bot.get_guild(371817692199518240) 
        role_name = None
        await TCG.create_role(name=role_name)
        await interaction.response.send_message(f"Role `{role_name}` has been created")
        

async def setup(bot):
    await bot.add_cog(test(bot))
