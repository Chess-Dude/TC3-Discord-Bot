import discord
from .bugModalConfirmPrompt import BugModalConfrimPrompt 

class BugModalReview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.green, emoji='📭', custom_id="persistent_view:close_bug_report")
    async def close_bug_report(self, interaction: discord.Interaction, button: discord.ui.Button):
        ws_role = interaction.guild.get_role(351075254912811020)
        if ws_role in interaction.user.roles:
            
            discord.Embed(
                title="Confirm close ticket?",
                color=0x2f3136
            )

            await interaction.response.send_message(
                content="Confirmation?", 
                ephemeral=True,
                view=BugModalConfrimPrompt()
            )

        else:
            await interaction.response.send_message("Error: You Are Not A Wiki Staff", ephemeral=True)