import discord 

class BugModalConfrimPrompt(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.green, emoji='📭', custom_id="persistent_view:close_bug_report")
    async def confirm_close_bug_report(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()