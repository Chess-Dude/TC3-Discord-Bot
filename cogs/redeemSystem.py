import discord
from discord import app_commands
from discord.ext import commands
from .redeemClasses.RedeemModal import RedeemModal

class RedeemTicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji='📩', custom_id="persistent_view:ticket_system")
    async def ticket_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RedeemModal())
             
class RedeemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(676112926918049813)
    @app_commands.command(
        name="create_ticket",
        description="A Command that allows you to create a ticket panel!")
    async def create_ticket_panel(
        self,
        interaction:discord.Interaction
    ):
        ticket_embed = discord.Embed(
            title="Welcome to The Conquerors 3 Redeem Center!",
            description="To create a ticket, click the button below 📩",
            color=0x00ffff
        )

        await interaction.channel.send(
            embed=ticket_embed,
            view=RedeemTicketPanel()
        )
        
async def setup(bot):
    await bot.add_cog(RedeemCommands(bot))
