import discord, gspread, re, json
from discord import app_commands
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

google_sheet = client.open("The Conquerors 3 Chess Tournament Contestants")
beginner_sheet = google_sheet.worksheet("Beginner")
novice_sheet = google_sheet.worksheet("Novice")
intermediate_sheet = google_sheet.worksheet("Intermediate")
advanced_sheet = google_sheet.worksheet("Advanced")


class InvalidResponse(Exception):
    pass

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

class ChessTournamentModalReview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def get_user(
            self, 
            interaction, 
            message_content
        ):
            user = interaction.guild.get_member(int(message_content.replace("<@", "").replace(">", "")))
            return user

    async def assign_role(
            self,
            interaction,
            user
    ):
        chess_role = interaction.guild.get_role(1035999506950537356)
        await user.add_roles(chess_role)

    async def main(
        self,
        interaction,
        message_content,
        player_category        
    ):
        user = ChessTournamentModalReview.get_user(
            self=self,
            interaction=interaction,
            message_content=message_content
        )     

        await ChessTournamentModalReview.assign_role(
            self,
            interaction=interaction,
            user=user
        )

        if player_category == "Beginner":
            beginner_sheet.insert_row([f"{user.id}", f"{user.name}#{user.discriminator}", f"{user.display_name}"], index=2)    

        elif player_category == "Novice":
            novice_sheet.insert_row([f"{user.id}", f"{user.name}#{user.discriminator}", f"{user.display_name}"], index=2)    

        elif player_category == "Intermediate":
            intermediate_sheet.insert_row([f"{user.id}", f"{user.name}#{user.discriminator}", f"{user.display_name}"], index=2)    

        elif player_category == "Advanced":
            advanced_sheet.insert_row([f"{user.id}", f"{user.name}#{user.discriminator}", f"{user.display_name}"], index=2)    


        success_embed = discord.Embed(
            title=f"Successfully Placed User In {player_category} Category",
            description=f"{interaction.user.display_name} Successfully Placed {user.display_name} in {player_category} Category",
            color=0x00ffff
        )

        await interaction.response.send_message(
            embed=success_embed
        )
        await interaction.message.edit(view=None)


    @discord.ui.button(label="Beginner", style=discord.ButtonStyle.green, custom_id="persistent_view:beginner_button")
    async def beginner_button(
        self, 
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await ChessTournamentModalReview.main(
            self=self,
            interaction=interaction,
            message_content=interaction.message.content,
            player_category="Beginner"
        )

     
    @discord.ui.button(label="Novice", style=discord.ButtonStyle.green, custom_id="persistent_view:novice_button")
    async def novice_button(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        await ChessTournamentModalReview.main(
            self=self,
            interaction=interaction,
            message_content=interaction.message.content,
            player_category="Novice"
        )
    

    @discord.ui.button(label="Intermediate", style=discord.ButtonStyle.green, custom_id="persistent_view:intermediate_button")
    async def intermediate_button(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        await ChessTournamentModalReview.main(
            self=self,
            interaction=interaction,
            message_content=interaction.message.content,
            player_category="Intermediate"
        )

    @discord.ui.button(label="Advanced", style=discord.ButtonStyle.green, custom_id="persistent_view:advanced_button")
    async def advanced_button(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        await ChessTournamentModalReview.main(
            self=self,
            interaction=interaction,
            message_content=interaction.message.content,
            player_category="Advanced"
        )

class ChessTournamentModal(discord.ui.Modal, title="Chess Tournament Sign-up"):
    rating = discord.ui.TextInput(
        label="What is your exact Elo/Rating?",
        style=discord.TextStyle.short,
        placeholder="Elo/Rating Here...",
        required=True,
        min_length=0,
        max_length=5
    )

    basic_rule_set = discord.ui.TextInput(
        label="Aware of the basic rules of the game? (Y/N)",
        style=discord.TextStyle.short,
        placeholder="(Yes/No) Here...",
        required=True,
        min_length=1,
        max_length=3
    )

    time_playing_chess = discord.ui.TextInput(
        label="How long have you been playing chess?",
        style=discord.TextStyle.short,
        placeholder="Time Playing Chess Here...",
        required=True,
        min_length=3,
        max_length=10
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
    ):

        try:
            rating_str = str(self.rating.value)
            rating_str = rating_str.replace(',', '')
            
            for num in rating_str:
                if not num.isdigit():
                    rating_str = rating_str.replace(f"{num}", '')
            
            rating_int = int(rating_str)
            
            acceptable_responses = ["yes", 'y', 'n', "no"]
            if (self.basic_rule_set.value.lower()) not in acceptable_responses:    
                raise InvalidResponse

        
        except ValueError:
            error_embed = discord.Embed(
                title="Error: Your Elo/rating was not a number. Please try again.",
                description="Note: put only a number for your elo/rating for example: 1000",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
        
        except InvalidResponse:
            error_embed = discord.Embed(
                title="Error: Invalid Input. Please try again.",
                description="Your response to the question: ``Aware of the basic rules of the game?`` was invalid. Please answer the question with a ``Yes`` or a ``No``.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
                    
        sign_up_embed = discord.Embed(
            title=f"Chess Tournament Sign-up",
            color=0x00ffff
        )
        
        sign_up_embed.set_author(
            name=f"Submitted by: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )
        
        sign_up_embed.timestamp = interaction.created_at
        
        sign_up_embed.set_footer(
            text=f"The Conquerors 3 Chess Tournament Sign-up",
            icon_url=interaction.guild.icon
        )

        sign_up_embed.set_thumbnail(
            url=interaction.user.avatar.url
        )

        sign_up_embed.add_field(
            name=f"Player Elo/Rating:",
            value=f"``{rating_int}``",
            inline=False
        )

        sign_up_embed.add_field(
            name="Knows ruleset/how to move pieces?",
            value=f"``{self.basic_rule_set.value}``",
            inline=False
        )

        sign_up_embed.add_field(
            name="Playing Chess since:",
            value=f"``{self.time_playing_chess.value}``",
            inline=False
        )

        chess_sign_ups_channel = interaction.guild.get_channel(1035759149021147226)
        await chess_sign_ups_channel.send(
            content=f"{interaction.user.mention}",
            embed=sign_up_embed,
            view=ChessTournamentModalReview()
        )

        approved_embed = discord.Embed(
            title=f"Approved: Event Committee have been notified about your sign-up!",
            color=0x00ffff
        )

        await interaction.response.send_message(
            embed=approved_embed,
            ephemeral=True
        )
             
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
