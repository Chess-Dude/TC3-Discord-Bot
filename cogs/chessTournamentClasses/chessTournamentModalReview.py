import discord, gspread, re, json 
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

google_sheet = client.open("The Conquerors 3 Chess Tournament Contestants")
beginner_sheet = google_sheet.worksheet("Beginner")
novice_sheet = google_sheet.worksheet("Novice")
intermediate_sheet = google_sheet.worksheet("Intermediate")
advanced_sheet = google_sheet.worksheet("Advanced")


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
