import discord, datetime, pytz
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

    @app_commands.guilds(350068992045744141)
    @app_commands.checks.has_any_role(554152645192056842, 351074813055336458)
    @app_commands.command(
        name="create_event",
        description="A Command that allows you to create a one day event!")
    @app_commands.describe(start_time="mention the start time")
    @app_commands.describe(end_time="mention the end time")
    @app_commands.rename(start_time="start_time")
    @app_commands.rename(end_time="end_time")
            
    async def create_one_day_event(
        self,
        interaction: discord.Interaction,
        start_time: str,
        end_time: str,
    ): 
        # Get the current UTC time
        current_time = discord.utils.utcnow()  # or datetime.datetime.now().astimezone(datetime.timezone.utc)
        
        # Concatenate the date and time strings
        date_string = current_time.strftime("%Y-%m-%d")
        start_datetime_string = f"{date_string} {start_time}"
        end_datetime_string = f"{date_string} {end_time}"
        
        # Convert the datetime strings to datetime objects
        start_dt = datetime.datetime.strptime(start_datetime_string, "%Y-%m-%d %I:%M%p").replace(tzinfo=datetime.timezone.utc)
        end_dt = datetime.datetime.strptime(end_datetime_string, "%Y-%m-%d %I:%M%p").replace(tzinfo=datetime.timezone.utc)

        sign_up_channel = interaction.guild.get_channel(350068992045744143)

        await interaction.guild.create_scheduled_event(
            name="1v1 Tournament - The Conquerors 3",
            start_time=start_dt,
            location=f"{sign_up_channel.mention}",
            end_time=end_dt,
            description="The Conquerors 3 are hosting its first ever 1v1 one-day tournament <t:1687541400:R>!\n\nSign-ups will open at <t:1687541400:t>, and close at <t:1687543200:t>. The tournament will then begin as soon as possible.\n\n__Prizes__\n1st Place: 8, 000 coins & 100 robux\n2nd Place: 6, 000 coins and 80 robux\n3rd Place: 4, 000 coins and 50 robux. \n\nDepending on the amount of sign-ups, we may break brackets down into skill divisions."        )

        await interaction.response.send_message(content="completed")
        
async def setup(bot):
    await bot.add_cog(TournamentSignupCommands(bot))
