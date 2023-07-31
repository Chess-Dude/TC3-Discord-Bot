import discord

class ParentStoryGameView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Decisions & Points", style=discord.ButtonStyle.blurple, emoji='🤔', custom_id="persistent_view:decisions_and_points_view")
    async def info_decisions_and_points(self, interaction: discord.Interaction, button: discord.ui.Button):        
        information_embed = discord.Embed(
            title=f"Story Game | Decision & Points",
            description=f"> • Readers are only allowed to **Pick only 1 of the 3-6 decisions** provided per entry. If readers reacted to two decisions they will be disqualified from the story game until a it's conclusion\n\n > • The decision with the most votes will be adopted as the official choice moving forward\n\n > • Readers are still encouraged to pick the right choice regardless of the number of votes. Since they will accumulate points  if they picked good choices.\n\n > • There are 4 types of decisions. Here are the points/outcome for each:  ``+500 normal good: Something positive happens to the protagonist``, ``-1000 normal bad: Something negative happens to the protagonist``, ``+2000 Critical good: Something really good happens to the protagonist that may result in a good ending.`` or ``-1500 Critical bad: Something really bad happens to the protagonist that may result in a bad ending``",
            color=0x00ffff
        )

        await interaction.response.send_message(embed=information_embed, ephemeral=True)

    @discord.ui.button(label="Getting Extra Points", style=discord.ButtonStyle.blurple, emoji='📈', custom_id="persistent_view:getting_points_view")
    async def info_clans(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"Story Game | Getting Extra Points",
            description=f"> • Ending the story game on a good ending will grant everyone +5000 points (When the Protagonist achieves his/her goal)\n\n > • Ending the story on a bad ending will grant no additional points (When the Protagonist dies suffers a horrible fate or fails to achieve his/her goals)\n\n > • Staying on a 5 vote streak regardless of what decision you pick will grant you +2000 points\n\n > • Voting on every decision from start to finish will grant you +3,000 - +7,000 points determined by how long the story lasts (is only apply when the story is at least 7 weeks/ 7entries long)",
            color=0x00ffff
        )

        await interaction.response.send_message(embed=information_embed, ephemeral=True)

    @discord.ui.button(label="Awards", style=discord.ButtonStyle.blurple, emoji='🏆', custom_id="persistent_view:awards_info_view")
    async def info_story_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"Story Game | Awards",
            description=f"At the end of each story game. Who ever, has scored past the threshold for each of the tiers are entitled to the following awards\n\n🏆 MPS: Player with most points scored!🏆:\n💰20k-10k coins, ( :Robux~1:200-100 robux and 💵30 AUD💵  at least 🗓️ 10 weeks/ 10entries long)\n\n💎Tier Diamond:\nThreshold 8k-10k points💰10k-5k coins, ( :Robux~1:100-50 robux and 💵10 AUD💵 at least 🗓️ 10 weeks/ 10entries long)\n\n🥇Tier Gold:\nThreshold 6k-7.5k points 💰7k-5k coins and :Robux~1:50 robux\n\n🥈Tier Silver:\nThreshold 4k-5k points\n\n💰5k-3k coins and :Robux~1:25 robux\n\n🥉Tier Bronze:\nThreshold 2.5k-3k points 💰3k-1k coins",
            color=0x00ffff
        )

        await interaction.response.send_message(embed=information_embed, ephemeral=True)
