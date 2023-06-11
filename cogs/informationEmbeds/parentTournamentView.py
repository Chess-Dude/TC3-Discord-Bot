import discord
from .childTournamentView import ChildTournamentInformationViews

class ParentTournamentInformationViews(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="1v1 Tournament Info", style=discord.ButtonStyle.blurple, custom_id="persistent_view:1v1_Tournaments")
    async def info_1v1(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"What 1v1 tournament information would you like to know more about?",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)

    @discord.ui.button(label="2v2 Tournament Info", style=discord.ButtonStyle.blurple, custom_id="persistent_view:2v2_Tournaments")
    async def info_2v2(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"What 2v2 tournament information would you like to know more about?",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)

    @discord.ui.button(label="3v3 Tournament Info", style=discord.ButtonStyle.blurple, custom_id="persistent_view:3v3_Tournaments")
    async def info_3v3(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"What 3v3 tournament information would you like to know more about?",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)
