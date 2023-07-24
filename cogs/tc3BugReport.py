import discord
from discord import app_commands
from discord.ext import commands
from .tc3BugClasses.bugModal import TC3BugModal


class BugReportTicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji='📩', custom_id="persistent_view:bug_report_system_test")
    async def ticket_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TC3BugModal())
             
class TC3BugCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(350068992045744141)
    @app_commands.command(
        name="create_bug",
        description="A Command that allows you to create a ticket panel!")
    async def create_ticket_bug_panel(
        self,
        interaction:discord.Interaction
    ):
        ticket_embed = discord.Embed(
            title="The Conquerors 3 Bug Report!",
            description="To report a bug, click the button below 📩",
            color=0x2f3136
        )

        await interaction.channel.send(
            embed=ticket_embed,
            view=BugReportTicketPanel()
        )

async def setup(bot):
    await bot.add_cog(TC3BugCommands(bot))
