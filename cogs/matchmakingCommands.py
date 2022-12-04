import discord
from discord.ext import commands
from discord import app_commands

class ScrimsAppCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    def matchmaking(interaction):
        return interaction.channel.id == 359467053284851712

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
        await interaction.response.send_message(
            content="Task Completed",
            ephemeral=True
        )
        
        await interaction.channel.send(content=f"{interaction.user.mention} is going to play some TC3, come help them rekt some noobs! {game_role.mention}\n\nDon't want to get pinged? Run the command: \n``!!rank game``")        

async def setup(bot):
    await bot.add_cog(ScrimsAppCommands(bot))
