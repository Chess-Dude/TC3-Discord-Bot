import discord
from discord import app_commands
from discord.ext import commands
from .signupClasses.tournamentSignupModal import TournamentSignupModal

class TournamentTicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Sign-up", style=discord.ButtonStyle.green, emoji='📩', custom_id="persistent_view:sign_up_button")
    async def ticket_panel(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(TournamentSignupModal())

             
class TournamentSignupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(350068992045744141)
    @app_commands.command(
        name="create_sign_ups",
        description="A Command that allows you to create a sign-up panel!")
    async def create_ticket_panel(
        self,
        interaction:discord.Interaction
    ):
        ticket_embed = discord.Embed(
            title="Welcome to The Conquerors 3 One-Day Tournament!",
            description="To sign-up, click the button below 📩",
            color=0x00ffff
        )

        await interaction.channel.send(
            embed=ticket_embed,
            view=TournamentTicketPanel()
        )

async def setup(bot):
    await bot.add_cog(TournamentSignupCommands(bot))
