import discord
from discord.ext import commands
from discord import app_commands

class ScrimsAppCommands(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        
    def _1v1_check_in(interaction):
        return interaction.channel.id == 666961021096689694

    def _2v2_check_in(interaction):
        return interaction.channel.id == 666959897979781146

    def _3v3_check_in(interaction):
        return interaction.channel.id == 666957650717835265
    
    def clan_chat(interaction):
        return interaction.channel.id == 707220152625791047
    
    def matchmaking(interaction):
        return interaction.channel.id == 359467053284851712

    def scrim_channels(interaction):
        return interaction.channel.id == 666961021096689694 or interaction.channel.id == 666959897979781146 or interaction.channel.id == 666957650717835265 or interaction.channel.id == 707220152625791047
        
    scrim_group = app_commands.Group(
        name="scrim", 
        description="A Command That Allows You To Notify Players That You Want to Scrimmage!",
        guild_ids=[371817692199518240])
    
    @app_commands.checks.cooldown(1, 1800, key=lambda i: (i.guild_id))
    @scrim_group.command(
        name="1v1",
        description="A Command That Allows You To Request Members For A Competitive Scrimmage!")
    @app_commands.check(_1v1_check_in)
    async def scrim_command_1v1(
        self,
        interaction: discord.Interaction
    ):  
        scrimmage_role = interaction.guild.get_role(935635762987298836) 
        await interaction.channel.send(content=f"{interaction.user.mention} wants to 1v1 {scrimmage_role.mention}!")        

    @app_commands.checks.cooldown(1, 1800, key=lambda i: (i.guild_id))
    @scrim_group.command(
        name="2v2",
        description="A Command That Allows You To Request Members For A Competitive Scrimmage!")
    @app_commands.check(_2v2_check_in)
    async def scrim_command_2v2(
        self,
        interaction: discord.Interaction
    ):  
        scrimmage_role = interaction.guild.get_role(935635762987298836)     
        await interaction.channel.send(content=f"{interaction.user.mention} wants to 2v2 {scrimmage_role.mention}!")        

    @app_commands.checks.cooldown(1, 1800, key=lambda i: (i.guild_id))
    @scrim_group.command(
        name="3v3",
        description="A Command That Allows You To Request Members For A Competitive Scrimmage!")
    @app_commands.checks.check(_3v3_check_in)
    async def scrim_command_3v3(
        self,
        interaction: discord.Interaction
    ):  
        scrimmage_role = interaction.guild.get_role(935635762987298836) 
        await interaction.channel.send(content=f"{interaction.user.mention} wants to 3v3 {scrimmage_role.mention}!")        

    @app_commands.guilds(350068992045744141)
    @app_commands.checks.cooldown(1, 1800, key=lambda i: (i.guild_id))
    @app_commands.command(
        name="play",
        description="A Command That Allows You To Request Members For A Game Of TC3!")
    @app_commands.checks.check(matchmaking)
    async def play_command(
        self,
        interaction: discord.Interaction
    ):  
        game_role = interaction.guild.get_role(356558859260657666)
        await interaction.channel.send(content=f"{interaction.user.mention} is going to play some TC3, come help them rekt some noobs! {game_role.mention}\n\nDon't want to get pinged? Run the command: \n``!!rank game``")        

async def setup(bot):
    await bot.add_cog(ScrimsAppCommands(bot))
