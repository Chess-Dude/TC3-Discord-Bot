import discord
from ...informationChannels import InformationEmbeds
from ..storyGameEmbed.parentStoryGameView import ParentStoryGameView

class ParentWelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Tournaments", style=discord.ButtonStyle.blurple, custom_id="persistent_view:tournament_info_view")
    async def info_tournaments(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="There are different types of tournaments. From special one-day tournaments, to our daily 1v1, 2v2, and 3v3 tournaments. Maps are randomized and players are put into seperate skill divisions to ensure fair play.", ephemeral=True)
        await InformationEmbeds.tournament_embed_info(
            self=self,
            interaction=interaction
        )

    @discord.ui.button(label="Clans (Casual)", style=discord.ButtonStyle.blurple, custom_id="persistent_view:clans_info_view")
    async def info_clans(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Unlike other games, TC3 clans are based off of TC3 play time (end of round bonuses). These end of round bonuses are automatically tracked by me (The TC3 Bot) and help contribute to a weekly and yearly leaderboard. At the end of each week, the top 3 clans recieve in game coins. **To join a clan**, DM a clan leader from <#1121271059761602722>", ephemeral=True)
        await InformationEmbeds.send_clan_embed_info(
            self=self, 
            interaction=interaction
        )

    @discord.ui.button(label="Story Game", style=discord.ButtonStyle.blurple, custom_id="persistent_view:story_info_view")
    async def info_story_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        story_information_embed = discord.Embed(
            title=f"The Conquerors 3 Community | Story Info",
            description=f"Story Game is a activity that all members may partake in!",
            color=0x00ffff
        )

        await interaction.response.send_message(
            content="Story Game is a activity that all members may partake in!",
            embed=story_information_embed,
            view=ParentStoryGameView(),
            ephemeral=True
        )

    @discord.ui.button(label="Contests", style=discord.ButtonStyle.blurple, custom_id="persistent_view:contests_info_view")
    async def info_contests(self, interaction: discord.Interaction, button: discord.ui.Button):
        contest_information_embed = discord.Embed(
            title=f"The Conquerors 3 Community | Contests",
            description=f"Our Beloved ❤️ Event Committee also host weekly/monthly contests! Ranging from Base building, Survival challenge, art/story design contests and meme design contest etc. Come and participate for some big coin/robux prizes and discord roles like @contest winner @memelord @artist etc...",
            color=0x00ffff
        )

        await interaction.response.send_message(
            embed=contest_information_embed,
            ephemeral=True
        )

    @discord.ui.button(label="Game Night & Events", style=discord.ButtonStyle.blurple, custom_id="persistent_view:events_info_view")
    async def info_events(self, interaction: discord.Interaction, button: discord.ui.Button):
        events_information_embed = discord.Embed(
            title=f"The Conquerors 3 Community | Game Night & Events",
            description=f"Our Beloved ❤️ Event Committee host weekly/bi weekly events from game nights to trivia, chess and map guesser for Big coins/robux prizes. Usually from Fridays to Weekends EST 🌎",
            color=0x00ffff
        )

        await interaction.response.send_message(
            embed=events_information_embed,
            ephemeral=True
        )
