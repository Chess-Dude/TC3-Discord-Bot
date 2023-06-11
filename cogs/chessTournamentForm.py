import discord
from discord import app_commands
from discord.ext import commands
from .chessTournamentClasses.chessTournamentModal import ChessTournamentModal

class ChessTournamentTicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
            label="Click This To Sign-Up!", 
            style=discord.ButtonStyle.green, emoji='📩', 
            custom_id="persistent_view:chess_tournament_ticket_system"
    )
    async def ticket_panel(
        self, interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(ChessTournamentModal())

          
class ChessTournamentCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(350068992045744141)
    @app_commands.command(
        name="create_chess_panel",
        description="A Command that allows you to create a chess tournament ticket panel!")
    async def create_ticket_panel(
        self,
        interaction:discord.Interaction
    ):
        ticket_embed = discord.Embed(
            title="Welcome to The Conquerors 3 Chess Tournament!",
            description="To sign-up, click the button below 📩",
            color=0x00ffff
        )

        await interaction.channel.send(
            embed=ticket_embed,
            view=ChessTournamentTicketPanel()
        )

async def setup(bot):
    await bot.add_cog(ChessTournamentCommands(bot))
